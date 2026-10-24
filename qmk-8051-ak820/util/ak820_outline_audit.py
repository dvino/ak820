#!/usr/bin/env python3
"""Audit repeated straight-line 8051 instructions in a linked AK820 build.

The default is read-only. --outline-dir creates a separate ASM tree for an
EXPERIMENTAL relink; it never edits the input build or a firmware source file.
Exact outlining preserves the original instructions and their register effects.
One extra LCALL/RET adds two stack bytes. This tool is not hardware validation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import heapq
import json
from pathlib import Path
import re
import shutil

LISTED = re.compile(r"^\s*([0-9A-F]{6})\s+((?:[rstup*]?[0-9A-F]{2}\s*)+)\[[\d ]+\]\s*(\d+)\s+(\w+)\s*(.*?)\s*$")
SYMBOL = re.compile(r"(?<![\w$])(_[A-Za-z_$][\w$]*)(?![\w$])")
SAFE_OPS = {"mov", "movx", "movc", "inc", "dec", "add", "addc", "subb", "clr", "cpl", "anl", "orl", "xrl", "rl", "rr", "rlc", "rrc", "swap", "mul", "div", "xch"}
REGS = {"a", "b", "c", "dpl", "dph", "dptr", "ab", *[f"r{i}" for i in range(8)], *[f"ar{i}" for i in range(8)]}

# A finite search changes only the order of choosing exact, disjoint sequences.
# Each score is saving**4 * body_bytes**body_power / sites**site_power.
# Integer powers and rational comparison keep ties reproducible. Site powers
# are at most four: because saving=(body_bytes-3)*sites-body_bytes-1, a score
# cannot increase when occupied intervals remove sites. This is the upper-bound
# property used by the lazy queue below. The original greedy order is retained
# as a candidate, so the selected nominal saving cannot be worse.
SELECTION_STRATEGIES = (
    ("saving", 0, 0),
    ("long-body", 4, 2),
    ("balanced-body", 2, 2),
    ("site-balance", 0, 2),
    ("density-quarter", -1, 4),
    ("density-half", -2, 4),
    ("density-three-quarters", -3, 4),
    ("density", -4, 4),
)


# Additional foreground modules. None admits every CSEG function in that
# module; a set admits only those named functions. Actual IAP, delay, board IRQ
# and USB control/interrupt code remain outside this explicit scope.
FOREGROUND_MODULES = {
    "protocol/report.asm": None,
    "protocol/host.asm": None,
    "keyboards/ajazz/ak820/ak820_rgb.asm": None,
    # Foreground action engines; USB/timer/LED IRQ closures cannot reach them.
    "ak820_tapping.asm": None,
    "ak820_combo.asm": None,
    "ak820_tap_dance.asm": None,
    "ak820_key_override.asm": None,
    "ak820_settings.asm": None,
    "ak820_board.asm": frozenset({
        "ak820_set_slot_rgb", "ak820_rgb_init", "ak820_rgb_set_color",
        "ak820_rgb_set_color_all", "ak820_rgb_flush",
    }),
    "ak820_nvm.asm": None,
    "eeprom_driver.asm": None,
    "protocol/ch555/usb_ak820.asm": frozenset({
        "ak820_usb_raw_task", "ak820_usb_raw_send",
        "raw_request_is_nonpersistent", "ak820_usb_take_keyboard_reset",
    }),
}


def eligible_module(module: str, function: str) -> bool:
    if module.startswith("quantum/"):
        return True
    return module in FOREGROUND_MODULES and (
        FOREGROUND_MODULES[module] is None or function in FOREGROUND_MODULES[module])


@dataclass(frozen=True)
class Instruction:
    module: str
    function: str
    line: int
    address: int
    data: bytes
    opcode: str
    operands: str
    private_refs: tuple[str, ...]

    @property
    def assembly(self):
        return self.opcode + ("\t" + self.operands if self.operands else "")

    @property
    def exact(self):
        # Equal spelling of private symbols from different modules is not
        # identity. Keep their helper in their owning assembler module.
        return self.assembly, self.module if self.private_refs else ""


def allowed(opcode: str, operands: str) -> bool:
    if opcode not in SAFE_OPS or re.search(r"\b(?:sp|psw|pc)\b|@r[01]|\b\d+\$|(?<![\w.])\.(?![\w.])", operands, re.I):
        return False
    if opcode == "movc":
        # DPTR addresses absolute CODE. The PC-relative form changes when the
        # instructions move to a helper and must remain excluded.
        return operands == "a,@a+dptr"
    for operand in operands.split(","):
        if operand.startswith("#") or operand == "@dptr" or operand in REGS:
            continue
        # Exclude direct memory/SFR/bit accesses. All accepted non-immediate
        # operands are architectural registers or external RAM through DPTR.
        return False
    return True


def parse_dce(dce: Path, listing_suffix=".rst"):
    blocks, rejected = [], defaultdict(int)
    listings = sorted(dce.rglob("*" + listing_suffix))
    if not listings:
        raise ValueError(f"No {listing_suffix} assembler listings under {dce}")
    for listing in listings:
        module = listing.relative_to(dce).with_suffix(".asm").as_posix()
        assembly = dce / module
        source = assembly.read_text().splitlines()
        externals = {m[1] for line in source if (m := re.match(r"\s*\.globl\s+(\S+)", line))}
        aliases = [(int(m[1]), int(m[2], 0)) for line in source
                   if (m := re.fullmatch(r"\s*ar([0-7])\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*", line))]
        bank_zero_aliases = all(register == address for register,address in aliases)
        alias_names = {f"ar{register}" for register,address in aliases}
        by_line = {}
        for line in listing.read_text().splitlines():
            match = LISTED.match(line)
            if match:
                encoded = bytes.fromhex(re.sub(r"[rstup*]", "", match[2]))
                by_line[int(match[3]) - 1] = (int(match[1], 16), encoded, match[4].lower(), re.sub(r"\s+", "", match[5].split(";",1)[0]))
        area, function, current = "", "", []
        for number, original in enumerate(source):
            text = original.split(";",1)[0].strip()
            fn = re.match(r";\s*function\s+(\w+)\s*$", original.strip())
            if fn:
                function = fn[1]
            if text.startswith(".area"):
                area = text.split()[1]
            if not text:
                continue
            instruction = by_line.get(number)
            if instruction is None:
                # Labels and directives are entry/section boundaries. Comments
                # are harmless, but no candidate may swallow a branch target.
                if current: blocks.append(current); current = []
                continue
            address, data, opcode, operands = instruction
            valid_aliases = all(name in alias_names for name in re.findall(r"\bar[0-7]\b", operands))
            module_is_eligible = eligible_module(module, function) and area == "CSEG" and bank_zero_aliases and valid_aliases
            if not module_is_eligible or not allowed(opcode, operands):
                rejected["ineligible_module_or_non_cseg" if not module_is_eligible else opcode] += 1
                if current: blocks.append(current); current = []
                continue
            # Verify source/listing alignment before using listing byte sizes.
            pieces = text.split(None, 1)
            source_opcode, source_operands = pieces[0], pieces[1] if len(pieces) == 2 else ""
            if source_opcode.lower() != opcode or re.sub(r"\s+", "", source_operands) != operands:
                raise ValueError(f"ASM/RST mismatch {module}:{number + 1}")
            private = tuple(sorted(set(SYMBOL.findall(operands)) - externals))
            current.append(Instruction(module,function,number,address,data,opcode,operands,private))
        if current: blocks.append(current)
    return blocks, dict(rejected)


def parse(build: Path, listing_suffix=".rst"):
    return parse_dce(build / "dce", listing_suffix)


def normalized(sequence):
    symbols, registers, literals = {}, {}, {}
    result = []
    for insn in sequence:
        operand = SYMBOL.sub(lambda m: symbols.setdefault(m[0], f"$S{len(symbols)}"), insn.operands)
        operand = re.sub(r"\b(?:ar|r)([0-7])\b", lambda m: registers.setdefault(m[1], f"$R{len(registers)}"), operand)
        operand = re.sub(r"#(?:0x[0-9a-fA-F]+|\d+)\b", lambda m: literals.setdefault(m[0], f"#$I{len(literals)}"), operand)
        result.append(insn.opcode + ("\t" + operand if operand else ""))
    return tuple(result)


def sequence_matches(blocks, min_instructions=2, max_instructions=40, normalize=False):
    found = defaultdict(list)
    for block in blocks:
        exact = [i.exact for i in block]
        for start in range(len(block)):
            for length in range(min_instructions, min(max_instructions, len(block)-start) + 1):
                sequence = block[start:start+length]
                size = sum(len(i.data) for i in sequence)
                if size < 4:
                    continue
                key = normalized(sequence) if normalize else tuple(exact[start:start+length])
                found[key].append(sequence)
    return found


def candidate(key, matches, used=frozenset()):
    if len(matches) < 2:
        return None
    distinct, occupied = [], set()
    for seq in matches:
        cells = {(i.module, i.line) for i in seq}
        if cells & used or cells & occupied:
            continue
        occupied.update(cells)
        distinct.append(seq)
    if len(distinct) < 2:
        return None
    size = sum(len(i.data) for i in distinct[0])
    # No added argument setup for exact sequences: architectural register
    # state at each replacement is exactly the original input state.
    saving = (len(distinct)-1)*size - 3*len(distinct) - 1
    return (saving, size, key, distinct) if saving > 0 else None


def occurrences(blocks, min_instructions=2, max_instructions=40, used=frozenset(), normalize=False):
    candidates = []
    for key, matches in sequence_matches(blocks, min_instructions, max_instructions, normalize).items():
        choice = candidate(key, matches, used)
        if choice:
            candidates.append(choice)
    return sorted(candidates,key=lambda c:(-c[0],-c[1],repr(c[2])))


def describe(candidate):
    saving,size,key,matches = candidate
    return {"occurrences":len(matches),"body_bytes":size,"call_bytes_per_site":3,"return_bytes":1,
            "nominal_net_bytes":saving,"body":[i.assembly for i in matches[0]],
            "instruction_bytes":[i.data.hex() for i in matches[0]],
            "locations":[{"module":s[0].module,"function":s[0].function,"line":s[0].line+1,"address":s[0].address} for s in matches]}


def select_matches(matches, max_helpers, min_saving, strategy):
    # Enumerate instruction windows once. Each exact sequence has a fixed
    # length; its matches occur in source order, so greedily retaining the
    # first nonoverlapping interval gives the maximum match count. Removing
    # occupied intervals can only lower that count. An old heap priority is
    # therefore an upper bound; refresh only candidates that reach the top.
    # Keep the original saving/size/key tie order and all overlapping matches:
    # a previously rejected overlap may become eligible after another choice.
    _, body_power, site_power = strategy

    def priority(choice):
        saving, size, key, sites = choice
        numerator = saving ** 4 * size ** max(0, body_power)
        denominator = len(sites) ** site_power * size ** max(0, -body_power)
        return (-Fraction(numerator, denominator), -saving, -size, repr(key), key)

    queue = []
    for key, found in matches.items():
        choice = candidate(key, found)
        if choice:
            heapq.heappush(queue, priority(choice))
    selected, used = [], set()
    while queue and len(selected) < max_helpers:
        previous = heapq.heappop(queue)
        key = previous[-1]
        choice = candidate(key, matches[key], used)
        if not choice or choice[0] < min_saving:
            continue
        current = priority(choice)
        if current != previous:
            heapq.heappush(queue, current)
            continue
        selected.append(choice)
        used.update((i.module, i.line) for seq in choice[3] for i in seq)
    return selected


def select(blocks, max_helpers=200, min_saving=1):
    """The original greedy selection, retained for controls and comparisons."""
    return select_matches(sequence_matches(blocks), max_helpers, min_saving, SELECTION_STRATEGIES[0])


def select_compact(blocks, max_helpers=200, min_saving=1):
    """Pick the largest measured nominal saving from fixed exact strategies.

    Every choice uses the same instruction eligibility, helper cap and two-byte
    stack cost. Equal savings prefer fewer replacements, then fewer helpers.
    This bounded heuristic search is not a proof of globally optimal packing.
    The real memory windows must still be checked after the full link.
    """
    matches = sequence_matches(blocks)
    best, objective, chosen, trials = [], (-1, 0, 0), None, []
    for strategy in SELECTION_STRATEGIES:
        selected = select_matches(matches, max_helpers, min_saving, strategy)
        saving = sum(c[0] for c in selected)
        sites = sum(len(c[3]) for c in selected)
        row = {"strategy": strategy[0], "body_power": strategy[1], "site_power": strategy[2],
               "nominal_net_bytes": saving, "helpers": len(selected), "replacement_sites": sites}
        trials.append(row)
        score = (saving, -sites, -len(selected))
        if score > objective:
            best, objective, chosen = selected, score, strategy[0]
    return best, {"selected_strategy": chosen, "strategies": trials}


def outline_dce(source: Path, target: Path, selected):
    if any("_ak820_outline_" in p.read_text() for p in source.rglob("*.asm")):
        raise ValueError("Refusing an already outlined input: helpers must never nest")
    if target.exists(): raise ValueError(f"Refusing existing outline directory: {target}")
    if target.resolve().is_relative_to(source.resolve()):
        raise ValueError("Outline output must not be inside the input tree")
    shutil.copytree(source,target,ignore=shutil.ignore_patterns("*.rel","*.lst","*.rst","*.sym"))
    edits, helpers, imports = defaultdict(dict), defaultdict(list), defaultdict(set)
    for index,candidate in enumerate(selected):
        _,_,_,matches = candidate
        name = f"_ak820_outline_{index:04d}"
        owner = matches[0][0].module
        body = [i.assembly for i in matches[0]]
        helpers[owner].append((name,body))
        for sequence in matches:
            module = sequence[0].module
            imports[module].add(name)
            for instruction in sequence:
                edits[module][instruction.line] = ""
            edits[module][sequence[0].line] = "\tlcall\t" + name + "\n"
    for module in sorted(edits):
        path = target / module
        original = path.read_text().splitlines(keepends=True)
        result = "".join(edits[module].get(number,line) for number,line in enumerate(original))
        result += "\n; Experimental exact instruction outlining.\n"
        result += "".join("\t.globl " + name + "\n" for name in sorted(imports[module]))
        for name,body in helpers[module]:
            result += "\n\t.area CSEG (CODE)\n; function " + name[1:] + "\n" + name + ":\n"
            result += "".join("\t"+line+"\n" for line in body) + "\tret\n"
        path.write_text(result)


def outline_assembled(source_dce: Path, output_dce: Path, *, max_helpers=200, min_saving=1):
    """Factor freshly assembled DCE ASM, before the final firmware link.

    The builder must assemble source_dce first (producing .lst), then assemble
    the returned output_dce and link it through its normal bounded pipeline.
    This function never mutates the input tree. Extra live stack is two bytes;
    helpers contain no calls and cannot nest. No hardware validation is implied.
    """
    source_dce, output_dce = Path(source_dce).resolve(), Path(output_dce).resolve()
    if any("_ak820_outline_" in p.read_text() for p in source_dce.rglob("*.asm")):
        raise ValueError("Refusing an already outlined input: helpers must never nest")
    blocks,rejected = parse_dce(source_dce, ".lst")
    selected, selection = select_compact(blocks, max_helpers, min_saving)
    report = {"algorithm": "exact-foreground-register-xdata-code-v4", "listing_suffix": ".lst",
              "selection": selection,
              "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_asm_sha256": {p.relative_to(source_dce).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in sorted(source_dce.rglob("*.asm"))},
              "max_helpers": max_helpers, "min_saving": min_saving,
              "min_instructions": 2, "max_instructions": 40, "min_body_bytes": 4,
              "foreground_modules": {name: None if functions is None else sorted(functions)
                                     for name, functions in FOREGROUND_MODULES.items()},
              "safe_blocks": len(blocks), "rejected_instructions": rejected,
              "selected_exact": [describe(c) for c in selected],
              "selected_nominal_net_bytes": sum(c[0] for c in selected),
              "extra_stack_bytes": 2 if selected else 0,
              "limits": "Assembler transformation; caller must relink, validate image bounds and test the linked image. No IRQ timing or peripheral proof."}
    outline_dce(source_dce,output_dce,selected)
    (output_dce / "outlining.json").write_text(json.dumps(report,indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--outline-dir",type=Path,help="Experimental separate assembler output, never the source build")
    parser.add_argument("--max-helpers",type=int,default=200)
    parser.add_argument("--min-saving",type=int,default=1)
    parser.add_argument("--listing-suffix", choices=(".rst", ".lst"), default=".rst",
                        help=".rst audits a linked image; .lst permits outlining before any link")
    args=parser.parse_args()
    build=args.build_dir.resolve()
    blocks,rejected=parse(build,args.listing_suffix)
    candidates=occurrences(blocks)
    normalized_candidates=occurrences(blocks,normalize=True)
    selected,selection=select_compact(blocks,args.max_helpers,args.min_saving)
    image=build/'ajazz_ak820_vial.ihx'
    report={"linked_image_sha256":hashlib.sha256(image.read_bytes()).hexdigest() if image.is_file() else None,
            "listing_suffix":args.listing_suffix,
            "scope":"Quantum and explicit foreground CSEG straight-line register/XDATA/CODE-DPTR instructions only; no branch/call/return, stack, PC, SFR/direct-memory or indirect-IRAM accesses; labels break windows",
            "limits":"Static candidates, not applied savings or a correctness proof. Every helper needs relink, byte/relocation checks, stack review and CPU regression. Normalized families require extra argument/live-register analysis and are never auto-outlined.",
            "safe_blocks":len(blocks),"rejected_instructions":rejected,
            "exact_top":[describe(c) for c in candidates[:20]],
            "normalized_top":[describe(c) for c in normalized_candidates[:20]],
            "selection":selection,"selected_exact":[describe(c) for c in selected],
            "selected_nominal_net_bytes":sum(c[0] for c in selected),"extra_stack_bytes":2 if selected else 0}
    if args.outline_dir:
        outline_dce(build / "dce",args.outline_dir.resolve(),selected)
        report["experimental_outline_dir"]=str(args.outline_dir.resolve())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({"safe_blocks":len(blocks),"exact_groups":len(candidates),"normalized_groups":len(normalized_candidates),"selected_helpers":len(selected),"nominal_net_bytes":report['selected_nominal_net_bytes']}))


if __name__=='__main__':main()
