# -*- coding: utf-8 -*-
"""
1. sobre-1  <- Downloads/unnamed (7).jpg  (crop 4:3, foco na janela/equipamento)
2. servico-clinica-geral <- _novas/clinocogeral3.jpg (2:1 foco na boca)
   servico-lentes          <- _novas/lentes.jpg       (2:1 foco no sorriso de baixo)
3. dupla (Corpo clínico): gradiente casado com o da seção .doctor-feature
   (linear-gradient 120deg nas coords da seção, mapeado na fatia de 47% à direita)
"""
from PIL import Image, ImageOps
import numpy as np

NOVAS = 'lavic-odontologia/tools/_novas'
OUT = 'lavic-odontologia/assets/images'
WEBP = dict(format='WEBP', quality=84, method=6)
JPEG = dict(format='JPEG', quality=85, optimize=True, progressive=True)
AVIF = dict(format='AVIF', quality=54, speed=6)

# ---------- 1. sobre-1 ----------
im = ImageOps.exif_transpose(Image.open(r'C:\Users\vaniu\Downloads\unnamed (7).jpg')).convert('RGB')
w, h = im.size
print('unnamed(7):', im.size)
# janela 4:3, largura total, foco na metade superior (janela com vista + cadeira)
ch = int(w * 3 / 4)
cy = int(h * 0.35)
box = (0, max(0, min(h - ch, cy - ch // 2)), w, max(0, min(h - ch, cy - ch // 2)) + ch)
ImageOps.fit(im.crop(box), (480, 360), Image.LANCZOS).save(f'{OUT}/sobre-1.webp', **WEBP)
ImageOps.fit(im.crop(box), (480, 360), Image.LANCZOS).save(f'{OUT}/sobre-1.jpg', **JPEG)
im.crop(box).save('lavic-odontologia/assets/originals/sobre-1-nova.jpg', quality=92)
print('sobre-1 ok box=', box)

# ---------- 2. crops 2:1 com foco na boca ----------
def crop_2x1(src, name, mouth_frac):
    s = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    w, h = s.size
    ch = w // 2                      # janela 2:1 (largura cheia)
    cy = int(h * mouth_frac)
    y1 = max(0, min(h - ch, cy - ch // 2))
    box = (0, y1, w, y1 + ch)
    print(f'{name}: src={w}x{h} box={box}')
    fit = ImageOps.fit(s.crop(box), (720, 360), Image.LANCZOS)
    fit.save(f'{OUT}/{name}.webp', **WEBP)
    fit.save(f'{OUT}/{name}.jpg', **JPEG)
    s.crop(box).save(f'lavic-odontologia/assets/originals/{name}-nova.jpg', quality=92)

crop_2x1(f'{NOVAS}/clinocogeral3.jpg', 'servico-clinica-geral', 0.64)
crop_2x1(f'{NOVAS}/lentes.jpg', 'servico-lentes', 0.72)

# ---------- 3. dupla: gradiente nas coords da seção ----------
src = r'C:\Users\vaniu\Pictures\DENTISTAS ASSETS\Dentists_wearing_black_coats_2K_20260915233830 (1).png'
im = ImageOps.exif_transpose(Image.open(src)).convert('RGBA')
# enquadramento idêntico ao render final (960x1280 = caixa 47% x 100vh)
base = ImageOps.fit(im, (960, 1280), Image.LANCZOS)

W, H = 1440, 900            # seção desktop de referência
dx, dy = np.sin(np.deg2rad(120)), -np.cos(np.deg2rad(120))   # direção 120deg
DEN = dx * W + dy * H       # projeção máx da seção (canto inferior direito)
X0 = 0.53 * W               # início da fatia da imagem (47% à direita)
w2, h2 = base.size
xx, yy = np.mgrid[0:h2, 0:w2]
t = ((X0 + (xx / (w2 - 1)) * 0.47 * W) * dx + ((yy / (h2 - 1)) * H) * dy) / DEN
t = np.clip(t, 0, 1)

STOPS = [(0.0, (255, 255, 255)), (0.45, (247, 243, 236)), (0.78, (239, 230, 213)), (1.0, (227, 213, 184))]
grad = np.zeros((h2, w2, 3), np.float64)
for (p0, c0), (p1, c1) in zip(STOPS, STOPS[1:]):
    m = ((t >= p0) & (t <= p1))[..., None]
    f = np.clip((t - p0) / max(p1 - p0, 1e-6), 0, 1)[..., None]
    seg = np.array(c0, np.float64) * (1 - f) + np.array(c1, np.float64) * f
    grad = np.where(m, seg, grad)
bg = Image.fromarray(grad.astype(np.uint8), 'RGB')

out = Image.alpha_composite(bg.convert('RGBA'), base).convert('RGB')
out.save('lavic-odontologia/assets/originals/dupla-black-coats.jpg', quality=93)
ImageOps.fit(out, (960, 1280), Image.LANCZOS).save(f'{OUT}/dupla.webp', **WEBP)
ImageOps.fit(out, (960, 1280), Image.LANCZOS).save(f'{OUT}/dupla.jpg', **JPEG)
ImageOps.fit(out, (960, 1280), Image.LANCZOS).save(f'{OUT}/dupla.avif', **AVIF)
ImageOps.fit(out, (480, 640), Image.LANCZOS).save(f'{OUT}/dupla-480.webp', **WEBP)
print('dupla gradiente seção ok (t', round(float(t.min()), 3), '->', round(float(t.max()), 3), ')')
