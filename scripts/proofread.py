#!/usr/bin/env python3
"""Post-render proofread helper for the context-image skill.

Text baked into a generated illustration fails SILENTLY: GPT Image will render
"Misaiignment" where the prompt said "Misalignment", and at full size the word
looks correct. The defect is only visible under magnification.

This script slices a render into overlapping, upscaled tiles so every label is
large enough for the agent to proofread by eye. It does not OCR — stylized 3D
lettering defeats OCR, and the agent already has vision. The job here is purely
to make the text big enough to read reliably.

Usage:
    python3 proofread.py OUT.png                      # 2x2 grid, 2x upscale
    python3 proofread.py OUT.png --grid 3x2 --zoom 3  # finer slicing
    python3 proofread.py OUT.png --band 0.45 0.62     # one horizontal strip only

Then Read each printed tile path and compare the visible text, character by
character, against the exact strings the prompt asked for.
"""
import argparse
import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install --user Pillow")

OVERLAP = 0.10  # fraction of tile size repeated on each seam, so no glyph is cut


def parse_grid(text):
    try:
        cols, rows = (int(n) for n in text.lower().split("x"))
        if cols < 1 or rows < 1:
            raise ValueError
        return cols, rows
    except Exception:
        raise argparse.ArgumentTypeError("--grid expects COLSxROWS, e.g. 2x2")


def main():
    ap = argparse.ArgumentParser(description="Magnify a render so its labels can be proofread.")
    ap.add_argument("image", type=pathlib.Path)
    ap.add_argument("--grid", type=parse_grid, default=(2, 2), help="COLSxROWS (default 2x2)")
    ap.add_argument("--zoom", type=float, default=2.0, help="upscale factor (default 2.0)")
    ap.add_argument("--band", type=float, nargs=2, metavar=("TOP", "BOTTOM"),
                    help="crop one horizontal strip first, as fractions of height, e.g. 0.45 0.62")
    ap.add_argument("--outdir", type=pathlib.Path, default=None)
    args = ap.parse_args()

    if not args.image.is_file():
        sys.exit(f"not found: {args.image}")

    im = Image.open(args.image)
    if args.band:
        top, bottom = sorted(args.band)
        if not (0.0 <= top < bottom <= 1.0):
            sys.exit("--band values must satisfy 0 <= TOP < BOTTOM <= 1")
        im = im.crop((0, int(im.height * top), im.width, int(im.height * bottom)))

    outdir = args.outdir or args.image.parent / f"{args.image.stem}-proof"
    outdir.mkdir(parents=True, exist_ok=True)

    cols, rows = args.grid
    tw, th = im.width / cols, im.height / rows
    ox, oy = tw * OVERLAP, th * OVERLAP
    written = []

    for r in range(rows):
        for c in range(cols):
            box = (
                max(0, int(c * tw - ox)),
                max(0, int(r * th - oy)),
                min(im.width, int((c + 1) * tw + ox)),
                min(im.height, int((r + 1) * th + oy)),
            )
            tile = im.crop(box)
            tile = tile.resize(
                (max(1, int(tile.width * args.zoom)), max(1, int(tile.height * args.zoom))),
                Image.LANCZOS,
            )
            path = outdir / f"r{r + 1}c{c + 1}.png"
            tile.save(path)
            written.append(path)

    print(f"{len(written)} tiles at {args.zoom}x -> {outdir}")
    for p in written:
        print(p)
    print("\nRead each tile and compare every label character-by-character against the "
          "exact strings in the prompt. Any mismatch is a regeneration trigger.")


if __name__ == "__main__":
    main()
