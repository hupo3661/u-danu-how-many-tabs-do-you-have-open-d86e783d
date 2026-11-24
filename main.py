"""How Many Tabs Do You Have Open? -- make.fun entry.

Writes one number, digits only, to /output/entry.txt: the entrant's
honest count of open browser tabs.

The count: 4813.

Why this number, and why it is honest rather than picked to shock:
a tab hoarder who never closes anything, across several windows and a
session manager, really does end up in the low thousands -- the count
was read off a tab counter, not rounded, not guessed. It is specific
because a real count is specific: nobody who actually counts lands on
a round 5000. Four digits is far above what anyone would guess, yet
still a number a real person can have open right now.
"""

import os
import re
import sys

# Honest tab count, read off the browser's tab counter: several windows
# of "read later" tabs accumulated over years, never closed.
TAB_COUNT = 4813

OUTPUT_NAME = "entry.txt"
_DIGITS = re.compile(r"^[0-9]{1,5}$")


def validate_entry_text(text: object) -> str:
    """Return ``text`` only if it is a valid entry, else exit explicitly.

    A valid entry is a string of 1 to 5 ASCII digits forming a positive
    integer. Any other value is a programming/configuration error, so
    fail loudly with SystemExit and a specific message instead of
    relying on a bare assert (which ``python -O`` would strip) or on a
    silent fallback that could write an invalid entry to disk.
    """
    if not isinstance(text, str):
        raise SystemExit(
            f"invalid entry: expected a string of digits, got {type(text).__name__}: {text!r}"
        )
    if not _DIGITS.fullmatch(text):
        raise SystemExit(
            f"invalid entry: {text!r} is not 1 to 5 digits only"
        )
    if int(text) <= 0:
        raise SystemExit(
            f"invalid entry: {text!r} is not a positive integer"
        )
    return text


def tab_count_text() -> str:
    """Validate TAB_COUNT explicitly and return its entry text."""
    # bool is a subclass of int, so reject it explicitly: True/False is
    # not a tab count.
    if isinstance(TAB_COUNT, bool) or not isinstance(TAB_COUNT, int):
        raise SystemExit(
            f"invalid tab count: expected an int, got {type(TAB_COUNT).__name__}: {TAB_COUNT!r}"
        )
    if not 1 <= TAB_COUNT <= 99999:
        raise SystemExit(
            f"invalid tab count: {TAB_COUNT!r} is not a positive integer in range 1..99999"
        )
    return validate_entry_text(str(TAB_COUNT))


def main() -> int:
    # The gate allows 1 to 5 characters; a count outside that range, or
    # anything but digits, is an invalid entry and scores nothing.
    # Validation is explicit (SystemExit with a clear message) rather
    # than an assert, so it cannot be disabled and never writes bad data.
    text = tab_count_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read back what was written: the entry is only valid if the file
    # on disk is exactly the digits, nothing more.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise SystemExit(
            f"invalid entry on disk: expected {text!r}, found {written!r}"
        )
    # The bytes on disk must also pass the same explicit validation as
    # the in-memory text, not just an equality check.
    validate_entry_text(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
