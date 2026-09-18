# -*- coding: utf-8 -*-
"""Conferência de recortes: caixa desenhada no original + resultado final.

Uso:
    python tools/_crops.py            # todas as entradas de CANDIDATES
    python tools/_crops.py avatar     # filtra pelo nome (substring)

Gera tools/_crops-<grupo>.png — cada linha mostra:
  [ original com a caixa em vermelho + régua em px ] [ recorte no tamanho final ]
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
TILE_H = 420          # altura da miniatura do original
PREVIEW_H = 150       # altura do recorte final no sheet


def recorte(src, box, out_w, out_h):
    """(nome, arquivo_original, (x0,y0,x1,y1), (largura_final, altura_final))"""
    return (src, box, (out_w, out_h))


# ——————————————————————————————————————————————————————————————
# Candidatos: ajuste aqui e rode de novo até ficar bom.
# ——————————————————————————————————————————————————————————————
CANDIDATES = {
    "avatar-matheus": [
        ("dr-matheus-estudio.jpg", (145, 40, 605, 500), (240, 240)),
        ("dr-matheus-estudio.jpg", (150, 20, 630, 500), (240, 240)),
        ("dr-matheus-estudio.jpg", (170, 55, 590, 475), (240, 240)),
        ("dr-matheus-estudio.jpg", (135, 30, 645, 540), (240, 240)),
    ],
    "avatar-ana": [
        ("dra-ana-consultorio.jpg", (30, 270, 350, 590), (240, 240)),
        ("dra-ana-consultorio.jpg", (40, 250, 380, 590), (240, 240)),
        ("dra-ana-consultorio.jpg", (20, 290, 380, 650), (240, 240)),
        ("dra-ana-consultorio.jpg", (10, 260, 370, 620), (240, 240)),
    ],
    "alinhadores": [
        ("dupla-soussmile.jpg", (0, 100, 750, 500), (720, 360)),
        ("dupla-soussmile.jpg", (0, 130, 750, 493), (720, 360)),
        ("dupla-soussmile.jpg", (0, 60, 750, 435), (720, 360)),
        ("dupla-estudio.jpg", (0, 60, 750, 1030), (600, 800)),
        ("dupla-estudio.jpg", (0, 90, 750, 1090), (600, 800)),
    ],
}


def build(groups):
    for group in groups:
        items = CANDIDATES[group]
        rows = []
        for src, box, size in items:
            im = Image.open(SRC / src).convert("RGB")
            ow, oh = im.size
            scale = TILE_H / oh
            small = im.resize((int(ow * scale), TILE_H), Image.LANCZOS)
            d = ImageDraw.Draw(small)
            f = ImageFont.truetype(FONT, 11)
            sx, sy = small.size[0] / ow, TILE_H / oh
            x0, y0, x1, y1 = box
            d.rectangle([x0 * sx, y0 * sy, x1 * sx, y1 * sy], outline=(255, 0, 0), width=2)
            d.text((x0 * sx + 3, y0 * sy + 3), f"{x0},{y0}", font=f, fill=(255, 0, 0))
            d.text((x0 * sx + 3, y1 * sy - 14), f"{x1},{y1}", font=f, fill=(255, 0, 0))
            # régua de 50 px
            for gy in range(0, oh, 100):
                py = gy * sy
                d.line([(0, py), (8, py)], fill=(255, 0, 0), width=1)
                d.text((10, py + 1), str(gy), font=f, fill=(255, 0, 0))
            crop = im.crop(box)
            ph = PREVIEW_H
            pw = max(1, int(ph * size[0] / size[1]))
            rows.append((small, crop.resize((pw, ph), Image.LANCZOS), src, box, size))
        pad = 12
        W = max(r[0].size[0] for r in rows) + pad * 3 + max(r[1].size[0] for r in rows)
        H = len(rows) * (TILE_H + pad) + pad
        sheet = Image.new("RGB", (W, H), (247, 243, 236))
        d = ImageDraw.Draw(sheet)
        f = ImageFont.truetype(FONT, 13)
        y = pad
        for small, prev, src, box, size in rows:
            sheet.paste(small, (pad, y))
            px = pad * 2 + small.size[0]
            sheet.paste(prev, (px, y))
            d.text((px + 4, y + prev.size[1] + 4),
                   f"{src}  {box}  →  {size[0]}x{size[1]}", font=f, fill=(18, 18, 22))
            y += TILE_H + pad
        dest = ROOT / "tools" / f"_crops-{group}.png"
        sheet.save(dest)
        print("OK", dest, sheet.size)


if __name__ == "__main__":
    keys = sys.argv[1:]
    todo = [k for k in CANDIDATES if not keys or any(k.startswith(a) for a in keys)]
    build(todo)
