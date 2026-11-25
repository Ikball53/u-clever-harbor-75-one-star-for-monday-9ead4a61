#!/usr/bin/env python3
"""One Star for Monday — a one-star restaurant review of Monday.

Writes exactly one line (no trailing newline) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output), atomically.
"""

import os
import tempfile

LINE = (
    "Came in for breakfast, waited forty minutes, and Monday served "
    "a cold alarm, dead coffee, and a 9 a.m. meeting. "
    "Never again. One star."
)


def main() -> None:
    # Guard the brief's hard limits before writing anything.
    if len(LINE) > 180:
        raise ValueError("entry exceeds 180 characters")
    if len(LINE.split()) > 25:
        raise ValueError("entry exceeds 25 words")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
