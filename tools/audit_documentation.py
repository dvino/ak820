#!/usr/bin/env python3
"""Check active project documentation links and bilingual feature/profile registries."""
from __future__ import annotations

import importlib.util
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)


def slugify(text: str) -> str:
    text = html.unescape(text).strip().lower()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[^\w -]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def heading_slugs(text: str) -> set[str]:
    counts: dict[str, int] = {}
    result = set()
    for heading in HEADING.findall(text):
        slug = slugify(heading)
        suffix = counts.get(slug, 0)
        counts[slug] = suffix + 1
        result.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return result


def active_markdown() -> list[Path]:
    paths = {ROOT / "README.md", ROOT / "web/README.md",
             ROOT / "qmk-8051-ak820/keyboards/ajazz/ak820/readme.md"}
    for directory in (ROOT / "docs", ROOT / "web/docs"):
        paths.update(directory.rglob("*.md"))
    return sorted(path for path in paths if path.is_file())


def source_registries() -> dict[str, object]:
    source = ROOT / "qmk-8051-ak820/util/ak820_profiles.py"
    spec = importlib.util.spec_from_file_location("ak820_profiles", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    wanted = ("BASE_FEATURES", "SWITCHES", "RELEASE_PROFILES", "PROFILES", "DEFAULT_PROFILE")
    values = {name: getattr(module, name) for name in wanted}
    values["CONFIGURATIONS"] = {name: module.configuration(name) for name in module.RELEASE_PROFILES}
    return values


def check_catalog(errors: list[str]) -> None:
    catalog_path = ROOT / "web/module-descriptions.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    registries = source_registries()
    features = catalog.get("features", [])
    profiles = catalog.get("profiles", [])
    feature_ids = [item.get("id") for item in features]
    profile_ids = [item.get("id") for item in profiles]
    if len(feature_ids) != len(set(feature_ids)):
        errors.append("module-descriptions.json has duplicate feature IDs")
    if {item.get("id") for item in features if item.get("kind") == "base"} != set(registries["BASE_FEATURES"]):
        errors.append("Feature catalog base IDs differ from BASE_FEATURES")
    if {item.get("id") for item in features if item.get("kind") == "optional"} != set(registries["SWITCHES"]) | {"nkro-reports", "vialrgb-direct-ram"}:
        errors.append("Feature catalog optional IDs differ from SWITCHES")
    if profile_ids != list(registries["RELEASE_PROFILES"]):
        errors.append("Profile catalog IDs/order differ from RELEASE_PROFILES")
    if sum(bool(item.get("default")) for item in profiles) != 1:
        errors.append("Exactly one profile must be marked default")
    if next((item.get("id") for item in profiles if item.get("default")), None) != registries["DEFAULT_PROFILE"]:
        errors.append("Profile catalog default differs from DEFAULT_PROFILE")
    source_profiles = registries["PROFILES"]
    for profile in profiles:
        identifier = profile.get("id")
        expected = list(source_profiles.get(identifier, ()))
        if profile.get("optional_features") != expected:
            errors.append(f"Profile catalog feature set differs from source: {identifier}")
        configuration = registries["CONFIGURATIONS"].get(identifier)
        if configuration is None or profile.get("configuration") != configuration:
            errors.append(f"Profile catalog configuration differs from source: {identifier}")
        if configuration is None or profile.get("features") != sorted(configuration["base_features"] + configuration["optional_features"]):
            errors.append(f"Profile catalog derived features differ from source: {identifier}")
        for field in ("title", "summary", "purpose"):
            value = profile.get(field, {})
            if not all(isinstance(value.get(language), str) and value[language].strip()
                       for language in ("en", "ru")):
                errors.append(f"Profile {identifier} is missing bilingual {field}")
    for feature in features:
        for field in ("title", "summary", "limits"):
            value = feature.get(field, {})
            if not all(isinstance(value.get(language), str) and value[language].strip()
                       for language in ("en", "ru")):
                errors.append(f"Feature {feature.get('id')} is missing bilingual {field}")
        guides = feature.get("guide", {})
        for language in ("en", "ru"):
            destination = guides.get(language)
            if not isinstance(destination, str) or not destination.strip():
                errors.append(f"Feature {feature.get('id')} is missing {language} guide")
                continue
            target, separator, anchor = destination.partition("#")
            resolved = (ROOT / "web" / unquote(target)).resolve() if target else None
            # An empty target means an anchor in the catalog's default guide
            # context (the current Markdown document when auditing Markdown).
            # JSON catalog entries have no implicit document, so require a path.
            if resolved is None:
                errors.append(f"{catalog_path.relative_to(ROOT)} guide has no target: {destination}")
                continue
            if not resolved.is_file():
                errors.append(f"{catalog_path.relative_to(ROOT)} guide missing: {destination}")
            elif separator and unquote(anchor) not in heading_slugs(resolved.read_text(encoding="utf-8")):
                errors.append(f"{catalog_path.relative_to(ROOT)} guide anchor missing: {destination}")

    matrix_path = ROOT / "web/firmware-matrix.json"
    if matrix_path.exists():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            expected_names = list(registries["RELEASE_PROFILES"])
            rows = matrix.get("profiles", [])
            row_ids = [row.get("id", row.get("profile")) for row in rows]
            if matrix.get("default_profile") != registries["DEFAULT_PROFILE"]:
                errors.append("Firmware matrix default differs from DEFAULT_PROFILE")
            if row_ids != expected_names:
                errors.append("Firmware matrix profile IDs/order differ from RELEASE_PROFILES")
            source_profiles = registries["PROFILES"]
            for row in rows:
                identifier = row.get("id", row.get("profile"))
                expected = list(source_profiles.get(identifier, ()))
                actual = row.get("optional_features")
                if actual is None:
                    actual = row.get("configuration", {}).get("optional_features")
                if actual != expected:
                    errors.append(f"Firmware matrix feature set differs from source: {identifier}")
        except (OSError, json.JSONDecodeError, AttributeError, TypeError) as exc:
            errors.append(f"Firmware matrix cannot be checked: {exc}")


def main() -> int:
    errors: list[str] = []
    for document in active_markdown():
        text = document.read_text(encoding="utf-8", errors="replace")
        for match in MARKDOWN_LINK.finditer(text):
            destination = match.group(1).split(maxsplit=1)[0].strip("<>")
            if destination.startswith(("https://", "http://", "mailto:", "data:")):
                continue
            target, separator, anchor = destination.partition("#")
            resolved = (document.parent / unquote(target)).resolve() if target else document
            if not resolved.exists():
                errors.append(f"{document.relative_to(ROOT)}: missing link {destination}")
            elif separator and resolved.is_file():
                if unquote(anchor) not in heading_slugs(resolved.read_text(encoding="utf-8", errors="replace")):
                    errors.append(f"{document.relative_to(ROOT)}: missing anchor {destination}")
    check_catalog(errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentation audit failed: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print(f"documentation audit passed: {len(active_markdown())} active Markdown files; feature/profile catalogs and guide links match source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
