# -*- coding: utf-8 -*-
"""Medições objetivas nos originais (px do original) — para escolher recortes sem achismo.

Uso:
    python tools/_measure.py                 # todos os originais
    python tools/_measure.py dupla-soussmile # um original

Imprime, por imagem:
  · faixa clara no topo (borda/quarto) — px onde a linha é quase toda luminosa
  · topo do cabelo  — 1ª linha com massa escura no miolo da imagem
  · rosto (pele)    — bbox do componente de pele dominante na metade de cima
  · centro do rosto — centroide x da pele (para centralizar avatares)
  · caixa laranja   — bbox de pixels laranja saturados (branding de terceiros)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "originals"


def load(name: str):
    im = ImageOps.exif_transpose(Image.open(SRC / name))
    return np.asarray(im.convert("RGB")).astype(np.float32)


def skin(a: np.ndarray) -> np.ndarray:
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
    return (cr > 133) & (cr < 180) & (cb > 77) & (cb < 130) & (y > 60) & (r > g) & (r > b)


def lum(a: np.ndarray) -> np.ndarray:
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def bbox(mask: np.ndarray):
    ys, xs = np.where(mask)
    if not len(ys):
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def warm_profile(name: str, thresh: int = 200) -> None:
    """Faixas de linhas com muita massa laranja/quente (objeto de branding)."""
    a = load(name)
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    warm = (r > 150) & ((r - b) > 60) & (g < r * 0.78)
    cnt = warm.sum(1)
    runs, start = [], None
    for y in range(h):
        if cnt[y] > thresh:
            if start is None:
                start = y
        elif start is not None:
            runs.append((start, y - 1))
            start = None
    if start is not None:
        runs.append((start, h - 1))
    if not runs:
        print(f"  quente: nenhuma linha com >{thresh} px")
    for s, e in runs:
        xs = np.where(warm[s:e + 1].any(0))[0]
        print(f"  quente y={s}..{e}  x={int(xs.min())}..{int(xs.max())}  "
              f"max_px/linha={int(cnt[s:e + 1].max())}")


def column_profile(name: str, x0: int, x1: int, y0: int = 0, y1=None, step: int = 10) -> None:
    """Perfil por linha numa faixa de x: pixels escuros (cabelo) e de pele (rosto)."""
    a = load(name)
    h, w = a.shape[:2]
    x0, x1 = max(0, x0), min(w, x1)
    y1 = min(y1 or h, h)
    L = lum(a)
    m = skin(a)
    dark = L < 95
    print(f"  perfil x={x0}..{x1}  (linha: escuro=cabelo  pele=rosto)")
    for y in range(y0, y1, step):
        dd = int(dark[y, x0:x1].sum())
        ss = int(m[y, x0:x1].sum())
        if dd > 15 or ss > 15:
            print(f"    y={y:4d}  escuro={dd:4d}  pele={ss:4d}")


def row_profile(name: str, y0: int, y1: int, x0: int = 0, x1=None, step: int = 25) -> None:
    """Perfil por coluna numa faixa de y: onde está a pele (rosto) no eixo x."""
    a = load(name)
    h, w = a.shape[:2]
    x1 = min(x1 or w, w)
    L = lum(a)
    m = skin(a)
    dark = L < 95
    print(f"  perfil y={y0}..{y1}  (coluna: pele=rosto  escuro=cabelo/roupa)")
    for xb in range(x0, x1, step):
        ss = int(m[y0:y1, xb:xb + step].sum())
        dd = int(dark[y0:y1, xb:xb + step].sum())
        if ss > 5 or dd > 5:
            print(f"    x={xb:4d}..{xb + step - 1:4d}  pele={ss:5d}  escuro={dd:5d}")


def report(name: str) -> None:
    a = load(name)
    h, w = a.shape[:2]
    L = lum(a)
    print(f"\n{name}  ({w}x{h})")

    # faixa clara no topo (fundo/quarto atrás do estúdio)
    for y in range(0, min(60, h)):
        if (L[y] > 200).mean() > 0.6:
            print(f"  linha clara y={y}  ({100 * y / h:.0f}%)")
        else:
            break

    # rosto: componente de pele dominante na metade de cima, por colunas
    m = skin(a)
    m[int(h * 0.62):] = False
    cols = m.sum(0)
    if cols.max() > 0:
        thr = cols.max() * 0.25
        idx = np.where(cols > thr)[0]
        x0, x1 = int(idx.min()), int(idx.max()) + 1
        tot = cols[idx].sum()
        cx = int((cols[idx] * idx).sum() / tot)
        band = m[:, x0:x1]
        rows = np.where(band.sum(1) > 4)[0]
        y0, y1 = int(rows.min()), int(rows.max()) + 1
        print(f"  pele_cols x={x0}..{x1}  centro_x={cx}  ({100 * cx / w:.0f}%)")
        print(f"  pele_linhas y={y0}..{y1}  altura={y1 - y0}  ({100 * y0 / h:.0f}%..{100 * y1 / h:.0f}%)")

    # topo do cabelo: 1ª linha com massa escura no miolo (25%..75% de x)
    mid = slice(int(w * 0.25), int(w * 0.75))
    for y in range(0, min(400, h)):
        if (L[y, mid] < 70).mean() > 0.35:
            print(f"  cabelo_topo y={y}  ({100 * y / h:.0f}%)")
            break

    # objeto laranja saturado (branding de terceiros, ex.: caixa Sousmile)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    orange = (r > 200) & (g > 80) & (g < 150) & (b < 90) & ((r - b) > 120)
    ob = bbox(orange)
    if ob and (ob[2] - ob[0]) * (ob[3] - ob[1]) > 2000:
        x0, y0, x1, y1 = ob
        print(f"  LARANJA saturado x={x0}..{x1}  y={y0}..{y1}  "
              f"({100 * y0 / h:.0f}%..{100 * y1 / h:.0f}% y)")
        print("  perfil por linha (y: px / x0..x1):")
        for y in range(y0, min(y1, h), 20):
            row = orange[y]
            xs = np.where(row)[0]
            if len(xs) > 20:
                print(f"    y={y:4d} px={len(xs):4d} x={int(xs.min())}..{int(xs.max())}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in ("-p", "perfil", "profile"):
        # python tools/_measure.py perfil dupla-estudio 380 750 [y0] [y1] [passo]
        name, x0, x1, *rest = args[1:]
        name = name if name.lower().endswith(".jpg") else name + ".jpg"
        column_profile(name, int(x0), int(x1), *[int(v) for v in rest])
        raise SystemExit

    if args and args[0] in ("-l", "linhas", "rows"):
        # python tools/_measure.py linhas dra-ana-consultorio 300 560 [x0] [x1] [passo]
        name, y0, y1, *rest = args[1:]
        name = name if name.lower().endswith(".jpg") else name + ".jpg"
        row_profile(name, int(y0), int(y1), *[int(v) for v in rest])
        raise SystemExit

    files = ([n if n.lower().endswith(".jpg") else n + ".jpg" for n in args]
             or sorted(p.name for p in SRC.glob("*.jpg")))
    for f in files:
        report(f)
        warm_profile(f)
