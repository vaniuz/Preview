# -*- coding: utf-8 -*-
"""Remove o fundo (transparência virou verde no PNG) e aplica o gradiente do site."""
from PIL import Image, ImageOps
import numpy as np

SRC = r'C:\Users\vaniu\Pictures\DENTISTAS ASSETS\Dentists_wearing_black_coats_2K_20260915233830 (1).png'
OUT1 = 'lavic-odontologia/assets/originals/dupla-black-coats.jpg'
OUT2 = 'lavic-odontologia/tools/_novas/dupla-black-coats-gradiente.jpg'

im = ImageOps.exif_transpose(Image.open(SRC)).convert('RGBA')
w, h = im.size

# gradiente 120deg igual ao fundo do site: #FFFFFF -> #F7F3EC 45% -> #EFE6D5 78% -> #E3D5B8
stops = [(0.0, (255, 255, 255)), (0.45, (247, 243, 236)), (0.78, (239, 230, 213)), (1.0, (227, 213, 184))]
ang = np.deg2rad(120)
dx, dy = np.sin(ang), -np.cos(ang)   # 120deg CSS: direita e levemente para baixo
yy, xx = np.mgrid[0:h, 0:w]
proj = (xx - (w - 1) * (dx < 0)) * dx + (yy - (h - 1) * (dy < 0)) * dy
t = (proj - proj.min()) / max(proj.max() - proj.min(), 1e-6)

grad = np.zeros((h, w, 3), np.float64)
for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
    m = ((t >= p0) & (t <= p1))[..., None]
    f = np.clip((t - p0) / max(p1 - p0, 1e-6), 0, 1)[..., None]
    seg = np.array(c0, np.float64) * (1 - f) + np.array(c1, np.float64) * f
    grad = np.where(m, seg, grad)
bg = Image.fromarray(grad.astype(np.uint8), 'RGB')

out = Image.alpha_composite(bg.convert('RGBA'), im).convert('RGB')
out.save(OUT1, quality=93)
out.save(OUT2, quality=93)
print('gradiente ok', out.size)
