#!/usr/bin/env python3
"""Ship It Friday -- make.fun entry (u-mgwals-ship-it-friday-30bd407a).

Writes one funny git commit message an AI coding agent would write
right before breaking production on a Friday, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt in the grader).

Deterministic: no network, no randomness, no reads outside this repo.
The entry text is a fixed constant; the writer validates it against the
gate (UTF-8 text, 1-159 chars, not only whitespace, single line) and
refuses to write anything invalid.
"""

import os
import sys

LINE = "ship it: Friday deploy, all tests pass except the ones I deleted, see you Monday"

MAX_CHARS = 159


def validate(line):
    """Raise ValueError unless line passes the competition gate."""
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if not line.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 159-char cap" % len(line))
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return line


def write_entry(line, out_dir):
    """Validate and write the entry; return the path written."""
    validate(line)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(line.encode("utf-8"))
    return path


def main():
    try:
        path = write_entry(LINE, os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    # Read-back gate: what landed on disk must be exactly the entry.
    with open(path, "rb") as f:
        if f.read() != LINE.encode("utf-8"):
            print("error: read-back mismatch", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
