# -*- coding: utf-8 -*-
"""Gera _originais-grid.png — cada original com grade de 10% para escolher recortes."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "originals"
FONT = "C:/Windows/Fonts/segoeui.ttf"

files = sorted(SRC.glob("*.jpg"))
TILE_W = 360
tiles = []
for p in files:
    im = Image.open(p).convert("RGB")
    h = int(TILE_W * im.size[1] / im.size[0])
    im = im.resize((TILE_W, h), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 11)
    for i in range(1, 10):
        x = int(TILE_W * i / 10)
        y = int(h * i / 10)
        d.line([(x, 0), (x, h)], fill=(255, 60, 60), width=1)
        d.line([(0, y), (TILE_W, y)], fill=(60, 160, 255), width=1)
        if i % 2 == 0:
            d.text((x + 2, 2), str(i * 10), font=f, fill=(255, 60, 60))
            d.text((2, y + 2), str(i * 10), font=f, fill=(60, 160, 255))
    tiles.append((p.name, im))

cols = 4
pad, label = 12, 20
row_h = max(t[1].size[1] for t in tiles) + label
rows = (len(tiles) + cols - 1) // cols
W = cols * (TILE_W + pad) + pad
H = rows * (row_h + pad) + pad
sheet = Image.new("RGB", (W, H), (247, 243, 236))
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype(FONT, 13)
for i, (name, im) in enumerate(tiles):
    cx = pad + (i % cols) * (TILE_W + pad)
    cy = pad + (i // cols) * (row_h + pad)
    sheet.paste(im, (cx, cy))
    d.text((cx, cy + im.size[1] + 3), name, font=f, fill=(18, 18, 22))
dest = ROOT / "tools" / "_originais-grid.png"
sheet.save(dest)
print("OK", dest, sheet.size)