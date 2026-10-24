# Startup stack check

The new `tests/ak820_startup/stack_contract.py` checks the exact linked CRT
from its initial stack-pointer assignment to entry into main. It uses main as
a proof boundary; it does not replace analysis of main with a leaf assumption.
The allowance is the maximum pre-main control-stack use, so it also covers
outer helper frames retained by a tail transfer to the program-startup call.

Six unit tests pass. They cover extra helper frames, changed stack placement,
changed main calls, interrupt enabling, unknown transfers, an alternate jump
to main and a helper tail transfer. Independent review found the two entry-frame
cases; both are now regression tests and both findings are closed. The corrected
checker is independently approved for this scope.

The exploratory full mask image reports two bytes before main and a two-byte
main-entry allowance. Packed entry still has separate checks for disabled
interrupts, bank and SP normalization, the single-DPTR startup contract and
the relocated native erase leaf. This is CPU/control-flow evidence; it makes
no claim about physical flash or peripherals.
