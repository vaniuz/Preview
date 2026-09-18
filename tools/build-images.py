# -*- coding: utf-8 -*-
"""
build-images.py — gera TODAS as imagens do site LAVIC a partir dos originais.

Originais  : assets/originals/
Saída      : assets/images/  (webp + jpg + avif conforme o uso no HTML)
Planilha   : tools/_contact-sheet.png  (conferência visual dos recortes)

Uso:
    python tools/build-images.py
    python tools/build-images.py --sheet   # também gera a folha de conferência
"""
from __future__ import annotations

import sys
from pathlib import Path

try:  # console do Windows pode estar em cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "originals"
OUT = ROOT / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

WEBP = dict(format="WEBP", quality=84, method=6)
WEBP_LL = dict(format="WEBP", lossless=True, method=6)
JPEG = dict(format="JPEG", quality=85, optimize=True, progressive=True)
AVIF = dict(format="AVIF", quality=54, speed=6)

FONT_BOLD = "C:/Windows/Fonts/georgiab.ttf"   # monograma (serifa — combina com Playfair)
FONT_UI = "C:/Windows/Fonts/segoeui.ttf"      # legenda da folha de conferência

INK = (18, 18, 22)        # --ink
GOLD = (201, 165, 96)     # --primary
CREAM = (247, 243, 236)   # --bg-alt


def source(name: str) -> Image.Image:
    im = Image.open(SRC / name)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def novas(name: str) -> Image.Image:
    """Fonte avulsa em tools/_novas (fotos de tratamento dos cards 2:1)."""
    im = Image.open(ROOT / "tools" / "_novas" / name)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def render(im: Image.Image, crop=None, size=None, name: str = "", formats=("webp", "jpg")) -> None:
    """Recorta, redimensiona e salva nos formatos pedidos."""
    if crop:
        im = im.crop(crop)
    if size:
        w, h = im.size
        if size[0] > w * 1.12:  # ampliando bastante → leve nitidez extra
            im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=72, threshold=3))
        im = im.resize(size, Image.LANCZOS)

    for fmt in formats:
        if fmt == "webp":
            dest, opts = OUT / f"{name}.webp", WEBP
        elif fmt == "jpg":
            dest, opts = OUT / f"{name}.jpg", JPEG
            im = im.convert("RGB") if im.mode != "RGB" else im
        elif fmt == "jpeg":
            dest, opts = OUT / f"{name}.jpeg", JPEG
            im = im.convert("RGB") if im.mode != "RGB" else im
        elif fmt == "avif":
            dest, opts = OUT / f"{name}.avif", AVIF
        else:
            raise ValueError(fmt)
        im.save(dest, **opts)
        print(f"  · {dest.name:34s} {im.size[0]}x{im.size[1]}")


# ——————————————————————————————————————————————————————————————
# Monograma LAVIC (favicon / logo da navbar e do rodapé)
# ——————————————————————————————————————————————————————————————
def monogram(size: int) -> Image.Image:
    """Badge circular preto com anel e 'L' dourado — legível em fundo claro e escuro."""
    ss = max(size, 512) * 2
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(ss * 0.035)
    d.ellipse([pad, pad, ss - pad, ss - pad], fill=INK + (255,),
              outline=GOLD + (255,), width=max(2, int(ss * 0.022)))

    f = ImageFont.truetype(FONT_BOLD, int(ss * 0.60))
    box = d.textbbox((0, 0), "L", font=f)
    d.text(((ss - (box[2] - box[0])) / 2 - box[0], (ss - (box[3] - box[1])) / 2 - box[1] - int(ss * 0.02)),
           "L", font=f, fill=GOLD + (255,))
    return img.resize((size, size), Image.LANCZOS)


def build_logos() -> None:
    print("● logotipos")
    badge = monogram(512)
    badge.save(OUT / "logo.png", format="PNG", optimize=True)
    print(f"  · logo.png                           512x512")
    for px in (128, 256):
        im = monogram(px)
        dest = OUT / f"logo-{px}.webp"
        im.save(dest, **WEBP_LL)
        print(f"  · {dest.name:34s} {px}x{px}")


# ——————————————————————————————————————————————————————————————
# Recortes
# ——————————————————————————————————————————————————————————————
def build_all() -> None:
    build_logos()

    print("● hero")
    sorriso = source("hero-atendimento-novo.jpg")            # 2752x1536
    desk = sorriso.crop((11, 0, 2741, 1536))                # 16:9 exato, sem esticar
    for w, h in ((480, 270), (960, 540), (1440, 810), (1920, 1080)):
        fmts = ("webp",) if w != 1440 else ("webp", "avif")
        render(desk, None, (w, h), f"hero-{w}", fmts)
    render(desk, None, (1440, 810), "hero", ("jpeg",))
    render(sorriso.crop((1080, 0, 1944, 1536)), None, (1080, 1920), "hero-mobile", ("jpg", "webp"))

    print("● doutores / dupla")
    dupla_coats = source("dupla-black-coats.jpg")           # dupla sorrindo + gradiente do site já aplicado
    render(dupla_coats, None, (480, 640), "dupla-480", ("webp",))
    render(dupla_coats, None, (960, 1280), "dupla", ("webp", "jpg", "avif"))

    print("● equipe")
    matheus = source("dr-matheus-estudio.jpg")              # 750x1235 — fundo preto; rosto x 268..554
    ana = source("dra-ana-consultorio.jpg")                 # 750x1235 — rosto x 200..324; cabelo y=290
    # retrato 3:4 — testa em y=104 e queixo em y=515 dentro do quadro (corte no preto, invisível)
    render(matheus, (105, 5, 705, 805), (900, 1200), "time-matheus", ("webp", "jpg"))
    render(ana, (0, 235, 750, 1235), (900, 1200), "time-ana", ("webp", "jpg"))
    # avatares 1:1 — caixa quadrada com folga e rosto centralizado (Matheus x=411, Ana x=262)
    render(matheus, (135, 5, 675, 545), (240, 240), "avatar-matheus", ("jpg", "webp"))
    render(ana, (92, 265, 432, 605), (240, 240), "avatar-ana", ("jpg", "webp"))

    print("● tratamentos (2:1 — janela de 750x375 no original)")
    cadeira = source("cadeira-odontologica.jpg")            # 750x1235
    # NOTA: dupla-soussmile.jpg fica fora do site — a caixa "Sousmile" ocupa x 0..430 / y 532..862
    # e nenhuma janela de 950+ px de altura (3:4 e 4:3) consegue evitar esse branding.
    # origens novas (2:1 já recortado): foco na boca / sorriso de baixo
    render(source("servico-lentes-nova.jpg"), None, (720, 360), "servico-lentes", ("webp", "jpg"))
    # fotos de tratamento (tools/_novas) — recorte 2:1 via ImageOps.fit (centering ajustado ao assunto)
    render(ImageOps.fit(novas("clareamento2.jpg"), (720, 360), Image.LANCZOS, centering=(0.5, 0.45)),
           None, None, "servico-clareamento", ("webp", "jpg"))
    render(ImageOps.fit(novas("bruxismo.jpg"), (720, 360), Image.LANCZOS, centering=(0.5, 0.5)),
           None, None, "servico-dtm", ("webp", "jpg"))
    render(ImageOps.fit(novas("ortodontia2.jpg"), (720, 360), Image.LANCZOS, centering=(0.5, 0.55)),
           None, None, "servico-alinhadores", ("webp", "jpg"))
    # origem nova (2:1 já recortado): atendimento em foco
    render(source("servico-clinica-geral-nova.jpg"), None, (720, 360), "servico-clinica-geral", ("webp", "jpg"))
    render(ImageOps.fit(novas("limpeza.jpg"), (720, 360), Image.LANCZOS, centering=(0.5, 0.45)),
           None, None, "servico-prevencao", ("webp", "jpg"))

    print("● sobre (4:3 — janela de 750x562)")
    # par intencional: sobre-1 = janela com vista + cadeira (origem nova 4:3) / sobre-2 = equipamento
    render(source("sobre-1-nova.jpg"), None, (480, 360), "sobre-1", ("webp", "jpg"))
    render(cadeira, (0, 400, 750, 962), (480, 360), "sobre-2", ("webp", "jpg"))

    print("● dicas (3:4 — capas temáticas de cuidados)")
    render(ImageOps.fit(novas("cuidados.jpg"), (600, 800), Image.LANCZOS, centering=(0.5, 0.42)),
           None, None, "blog-1", ("webp", "jpg"))
    render(ImageOps.fit(novas("clareamento2.jpg"), (600, 800), Image.LANCZOS, centering=(0.5, 0.45)),
           None, None, "blog-2", ("webp", "jpg"))
    render(ImageOps.fit(novas("ortodontia2.jpg"), (600, 800), Image.LANCZOS, centering=(0.5, 0.38)),
           None, None, "blog-3", ("webp", "jpg"))
    render(source("tip-prevencao-nova.jpg"), None, (600, 800), "tip-prevencao", ("avif", "webp", "jpg"))
    # hovers 2 e 3: fotos de tratamento (originais em assets/originals)
    render(ImageOps.fit(source("tip-clareamento-orig.jpg"), (600, 800), Image.LANCZOS, centering=(0.55, 0.50)),
           None, None, "tip-clareamento", ("avif", "webp", "jpg"))
    render(ImageOps.fit(source("tip-alinhadores-orig.jpg"), (600, 800), Image.LANCZOS, centering=(0.54, 0.50)),
           None, None, "tip-alinhadores", ("avif", "webp", "jpg"))


# ——————————————————————————————————————————————————————————————
# Folha de conferência
# ——————————————————————————————————————————————————————————————
def contact_sheet() -> None:
    files = sorted(p for p in OUT.glob("*.webp"))
    cols, tile, pad, label = 6, 220, 14, 22
    rows = (len(files) + cols - 1) // cols
    W = cols * (tile + pad) + pad
    H = rows * (tile + label + pad) + pad
    sheet = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_UI, 13)
    for i, p in enumerate(files):
        im = Image.open(p).convert("RGB")
        im.thumbnail((tile, tile), Image.LANCZOS)
        cx = pad + (i % cols) * (tile + pad)
        cy = pad + (i // cols) * (tile + label + pad)
        sheet.paste(im, (cx + (tile - im.size[0]) // 2, cy + (tile - im.size[1]) // 2))
        d.text((cx, cy + tile + 4), p.name.replace(".webp", ""), font=f, fill=INK)
    dest = ROOT / "tools" / "_contact-sheet.png"
    sheet.save(dest)
    print(f"● folha de conferência: {dest}")


if __name__ == "__main__":
    build_all()
    if "--sheet" in sys.argv:
        contact_sheet()
    print(f"\nOK — {len(list(OUT.glob('*')))} arquivos em assets/images/")