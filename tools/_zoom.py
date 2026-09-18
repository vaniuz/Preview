# -*- coding: utf-8 -*-
"""Zoom com grade de 5% (coordenadas relativas ao ORIGINAL) nas regiões críticas.

Gera tools/_zoom-a.png e tools/_zoom-b.png para escolher recortes de rosto/sorriso.
"""
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
TILE = 700

SHEETS = {
    "a": [
        ("dr-matheus-estudio.jpg", (0, 0, 750, 700)),
        ("dra-ana-consultorio.jpg", (0, 200, 750, 900)),
    ],
    "b": [
        ("dupla-soussmile.jpg", (0, 100, 750, 900)),
        ("dupla-estudio.jpg", (0, 200, 750, 900)),
    ],
}


def annotate(img: Image.Image, orig_w: int, orig_h: int, box) -> Image.Image:
    """Grade de 5% do original, com rótulos em % do original."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 12)
    sx = img.size[0] / (x1 - x0)
    sy = img.size[1] / (y1 - y0)
    for i in range(1, 20):
        pct = i * 5
        gx = int(orig_w * pct / 100)
        gy = int(orig_h * pct / 100)
        if x0 < gx < x1:
            px = int((gx - x0) * sx)
            col = (255, 40, 40) if pct % 10 == 0 else (255, 170, 60)
            d.line([(px, 0), (px, img.size[1])], fill=col, width=1)
            if pct % 10 == 0:
                d.text((px + 2, 2), str(pct), font=f, fill=(255, 40, 40))
        if y0 < gy < y1:
            py = int((gy - y0) * sy)
            col = (40, 150, 255) if pct % 10 == 0 else (120, 220, 255)
            d.line([(0, py), (img.size[0], py)], fill=col, width=1)
            if pct % 10 == 0:
                d.text((2, py + 2), str(pct), font=f, fill=(20, 90, 255))
    return img


for key, items in SHEETS.items():
    tiles = []
    for name, box in items:
        im = Image.open(SRC / name).convert("RGB")
        ow, oh = im.size
        crop = im.crop(box)
        w = TILE
        h = int(TILE * crop.size[1] / crop.size[0])
        crop = crop.resize((w, h), Image.LANCZOS)
        tiles.append((name, annotate(crop, ow, oh, box)))
    pad, label = 12, 22
    W = sum(t[1].size[0] for t in tiles) + pad * (len(tiles) + 1)
    H = max(t[1].size[1] for t in tiles) + label + pad * 2
    sheet = Image.new("RGB", (W, H), (247, 243, 236))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 14)
    x = pad
    for name, im in tiles:
        sheet.paste(im, (x, pad))
        d.text((x, pad + im.size[1] + 4), name, font=f, fill=(18, 18, 22))
        x += im.size[0] + pad
    dest = ROOT / "tools" / f"_zoom-{key}.png"
    sheet.save(dest)
    print("OK", dest, sheet.size)