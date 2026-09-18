# -*- coding: utf-8 -*-
"""Detecta a região de pele (rosto/cabeça) em cada original — coordenadas em px.

Sem OpenCV: máscara de pele em YCbCr + componentes conexos por BFS (numpy).
Imprime, por imagem, o bbox do maior componente de pele na metade superior
e o bbox da silhueta (pixels claros sobre fundo preto, quando aplicável).
"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "originals"


def skin_mask(im: Image.Image, scale: int = 4):
    """Máscara booleana de pele (downsample 'scale')."""
    w, h = im.size
    small = im.resize((max(1, w // scale), max(1, h // scale)), Image.BILINEAR)
    a = np.asarray(small).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
    mask = (cr > 133) & (cr < 180) & (cb > 77) & (cb < 130) & (y > 60) & (r > g) & (r > b)
    return mask, scale, (w, h)


def all_blobs(mask: np.ndarray, min_px: int = 8, top: int = 6):
    """Componentes conexos (4-vizinhos) ordenados por área desc."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    found = []
    for sy in range(h):
        for sx in range(w):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy, sx] = True
            x0 = x1 = sx
            y0 = y1 = sy
            n = 0
            while q:
                cx, cy = q.popleft()
                n += 1
                x0, x1 = min(x0, cx), max(x1, cx)
                y0, y1 = min(y0, cy), max(y1, cy)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((nx, ny))
            if n >= min_px:
                found.append((n, x0, y0, x1, y1))
    found.sort(reverse=True)
    return found[:top]


def silhouette(im: Image.Image, thresh: int = 80, coverage: float = 0.02):
    """bbox do assunto claro sobre fundo escuro, ignorando linhas/colunas quase vazias."""
    a = np.asarray(im.convert("L"))
    h, w = a.shape
    b = a > thresh
    rows = b.sum(1) > max(3, int(w * coverage))
    cols = b.sum(0) > max(3, int(h * coverage))
    ys = np.where(rows)[0]
    xs = np.where(cols)[0]
    if not len(ys) or not len(xs):
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def fmt(box, scale: int, w: int, h: int) -> str:
    x0, y0, x1, y1 = [v * scale for v in box]
    return (f"px=({x0}, {y0}, {x1}, {y1}) {x1 - x0}x{y1 - y0}"
            f"  {x0 * 100 // w}%..{x1 * 100 // w}% x | {y0 * 100 // h}%..{y1 * 100 // h}% y")


def report(name: str) -> None:
    im = Image.open(SRC / name).convert("RGB")
    w, h = im.size
    mask, scale, _ = skin_mask(im)
    print(f"\n{name}  ({w}x{h})")
    for n, x0, y0, x1, y1 in all_blobs(mask):
        print(f"  pele px={n:6d}  {fmt((x0, y0, x1, y1), scale, w, h)}")
    sil = silhouette(im)
    if sil:
        print(f"  silhueta (L>80) {fmt(sil, 1, w, h)}")


for p in sorted(SRC.glob("*.jpg")):
    report(p.name)