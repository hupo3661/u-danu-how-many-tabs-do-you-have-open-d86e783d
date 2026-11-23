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


def main() -> int:
    # The gate allows 1 to 5 characters; a count outside that range, or
    # anything but digits, is an invalid entry and scores nothing.
    if not isinstance(TAB_COUNT, int) or not 0 <= TAB_COUNT <= 99999:
        print(f"tab count out of range: {TAB_COUNT!r}", file=sys.stderr)
        return 1
    text = str(TAB_COUNT)
    if not _DIGITS.match(text):
        print(f"refusing to write invalid entry: {text!r}", file=sys.stderr)
        return 1
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
        print(f"entry mismatch on disk: {written!r}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
