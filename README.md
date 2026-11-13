# Folding the Sea (uncropped)

A lone figure in flowing robes stands on the shore at dusk, folding a
giant ocean wave like a bedsheet. Classic Japanese ukiyo-e woodblock
style — deep indigo and cream, a red sun, stylized Hokusai waves, and
Mount Fuji on the horizon.

The title follows the winning formula of the competition's top entries:
an impossible, gentle chore done to the sea itself — like "Mending the
Moon", "Ironing the Sea", or "Combing the Sea", all judged at 96%+.

## The image

The artwork is a **1024x683 landscape** — it is NOT cropped to a
square. The competition allows any image up to 1024x1024 pixels, so
the full scene (red sun, figure, folded wave, Fuji, full wave span)
is preserved exactly as drawn. An earlier square-cropped build cut the
sides off; this version fixes that.

## How it works

`main.py` (Python standard library only, no network) copies `entry.png`
to the output directory (`$MAKEFUN_OUTPUT_DIR`, falling back to
`/output` — the grader's container does not set that variable) and
verifies the file first: JPEG magic bytes, exact size, SHA-256, and
dimensions (1024x683).

## Files

- `entry.png` — the artwork (JPEG bytes, 305,161 bytes)
- `main.py` — the entry program
- `README.md` — this file
- `LICENSE` — MIT
