#!/usr/bin/env python3
"""Entry point for news-image-20261127 (Friday 27 November 2026).

The image is pre-rendered (see render.py, run by hand on the author's
machine) and shipped in this repository as entry.png. This program only
copies it to $MAKEFUN_OUTPUT_DIR, using the standard library only, so it
runs identically on the grading server (no network, no Pillow, no fonts).

Deterministic: the same bytes are written on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
