# -*- coding: utf-8 -*-
"""Inspeção de originais: dimensões + régua fina para localizar áreas indesejadas.

Uso:
    python tools/_inspect.py                 # lista dimensões de todos os originais
    python tools/_inspect.py dupla-soussmile # régua fina (25px) em toda a imagem
    python tools/_inspect.py dupla-soussmile 450 1000   # recorte ampliado da faixa y
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
CREAM = (247, 243, 236)
INK = (18, 18, 22)


def dims():
    for p in sorted(SRC.glob("*.jpg")):
        im = Image.open(p)
        from PIL import ImageOps
        im = ImageOps.exif_transpose(im)
        print(f"{p.name:32s} {im.size[0]:5d} x {im.size[1]:<5d} {im.mode}")


def ruler(name: str, y0=None, y1=None, every=25, out_h=900):
    im = Image.open(SRC / name).convert("RGB")
    ow, oh = im.size
    x0, xx1 = 0, ow
    a, b = (0, oh) if y0 is None else (y0, y1)
    region = im.crop((x0, a, xx1, b))
    rw, rh = region.size
    scale = min(out_h / rh, 2.5)  # >1 amplia faixas estreitas
    region = region.resize((max(1, int(rw * scale)), max(1, int(rh * scale))), Image.LANCZOS)
    pad_l = 62
    sheet = Image.new("RGB", (region.size[0] + pad_l, region.size[1]), CREAM)
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 12)
    fy = max(1, int(every * scale))
    for gy in range(a - a % every, b + 1, every):
        py = int((gy - a) * scale)
        if py > region.size[1]:
            continue
        major = gy % 100 == 0
        col = (200, 30, 30) if major else (160, 160, 160)
        d.line([(pad_l - 10, py), (pad_l, py)], fill=col, width=1)
        if major:
            d.text((2, max(0, py - 7)), str(gy), font=f, fill=col)
    sheet.paste(region, (pad_l, 0))
    dest = ROOT / "tools" / f"_inspect-{Path(name).stem}{'' if y0 is None else f'-{a}-{b}'}.png"
    sheet.save(dest)
    print("OK", dest, sheet.size, f"(orig {ow}x{oh})")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        dims()
    else:
        name = args[0]
        if not name.lower().endswith(".jpg"):
            name += ".jpg"
        if len(args) >= 3:
            ruler(name, int(args[1]), int(args[2]))
        else:
            ruler(name)
