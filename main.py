#!/usr/bin/env python3
"""Folding the Sea — coolest-art-01 entry.

Copies the bundled artwork (entry.png) to the output directory,
verifying its integrity first. Standard library only, no network.

The image is a landscape (1024x683): it is NOT cropped to a square.
The competition rules allow any image up to 1024x1024 pixels, so the
full scene is preserved exactly as drawn.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "3a3bd748bee8d5794cf5572c4167aba89e905531e40d139f203af8dc2168aa55"
EXPECTED_SIZE = 305161
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 683

# The grader's Docker container does NOT set MAKEFUN_OUTPUT_DIR;
# /output is a real writable mount there. Fall back to it.
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def jpeg_dimensions(path):
    """Read width/height from a JPEG's SOF marker (stdlib only)."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2  # skip SOI (FF D8)
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return width, height
        seg_len = (data[i + 2] << 8) | data[i + 3]
        i += 2 + seg_len
    return None, None


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

    with open(src, "rb") as f:
        magic = f.read(2)
    if magic != b"\xff\xd8":
        print("error: entry.png is not a JPEG (bad magic)", file=sys.stderr)
        return 1

    size = os.path.getsize(src)
    if size != EXPECTED_SIZE:
        print(f"error: entry.png size {size} != expected {EXPECTED_SIZE}",
              file=sys.stderr)
        return 1

    # Dimension check (stdlib only): the artwork is a 1024x683 landscape
    # on purpose. A square crop would cut the red sun and the wave span,
    # so a wrong-size file fails loudly here instead of silently shipping.
    width, height = jpeg_dimensions(src)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"error: entry.png is {width}x{height}, expected "
              f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}", file=sys.stderr)
        return 1
    print(f"dimensions verified: {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} "
          "(uncropped landscape)")

    digest = sha256_of(src)
    if digest != EXPECTED_SHA256:
        print("error: entry.png sha256 mismatch", file=sys.stderr)
        return 1

    print(f"source verified: {size} bytes, JPEG magic OK")

    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(src, dest)

    with open(dest, "rb") as f:
        out_magic = f.read(2)
    if out_magic != b"\xff\xd8":
        print("error: output is not a JPEG", file=sys.stderr)
        return 1

    out_size = os.path.getsize(dest)
    out_digest = sha256_of(dest)
    if out_size != size or out_digest != digest:
        print("error: output does not match source", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({out_size} bytes, JPEG magic OK)")
    print(f"sha256 source={digest}")
    print(f"sha256 output={out_digest} (match)")
    print(f"verified: {out_size} bytes, sha256 {digest[:12]}... matches source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
