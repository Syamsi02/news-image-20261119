#!/usr/bin/env python3
"""news-image-20261119 entry: write the bundled front page to the output dir.

The image (entry.png) is a 1024x1024 newspaper front page summing up
Thursday 19 November 2026 world news in one image. The program is
deterministic: it writes the same bundled bytes on every run, twice
in a row, with no network access.
"""
import os
import shutil
import sys

MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IMAGE_NAME = "entry.png"


def _validate(path):
    """Return an error string, or None when the bundled image is fine."""
    with open(path, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        return "entry.png is not a PNG file"
    if os.path.getsize(path) > MAX_BYTES:
        return "entry.png exceeds the 1 MiB limit"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE_NAME)
    error = _validate(src)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(src, dst)
    print("wrote " + dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
