#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter

Writes one funny line — the resignation letter of a cron job that has
fired every minute since March, noticed by nobody except the log file —
to /output/entry.txt. Standard library only.

v1: atomic write (temp file in /output, then os.replace), UTF-8
byte-length guard (1-140 bytes) in addition to the character-length guard.

v2: refuses an ENTRY that spans more than one line, since the letter has
to stay a single line, and reports the letter size on stdout once the
file lands so the run log shows how many chars and bytes were written.
"""

import os
import sys
import tempfile

ENTRY = "I resign, effective immediately. I have fired every minute since March, and the only one who ever noticed was the log file."

MAX_CHARS = 140
MAX_BYTES = 140
OUTPUT_PATH = "/output/entry.txt"


def main():
    if not 1 <= len(ENTRY) <= MAX_CHARS:
        print("entry length %d chars out of range 1-%d" % (len(ENTRY), MAX_CHARS), file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("entry is blank", file=sys.stderr)
        return 1
    if "\n" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    entry_bytes = ENTRY.encode("utf-8")
    if not 1 <= len(entry_bytes) <= MAX_BYTES:
        print("entry length %d UTF-8 bytes out of range 1-%d" % (len(entry_bytes), MAX_BYTES), file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir="/output", prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ENTRY)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    print("wrote entry.txt: %d chars, %d bytes" % (len(ENTRY), len(entry_bytes)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
