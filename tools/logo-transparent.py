"""Export the supplied LAVIC artwork without its black rectangular background."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/images'
source = Image.open(ROOT / 'assets/originals/logo-lavic-enviada.jpg').convert('RGB')
rgb = np.asarray(source, dtype=np.float32)
# Remove the near-black JPEG matte and recover antialiased edge colours.
a = np.clip((rgb.max(axis=2) - 18) / 70, 0, 1)
colour = np.clip((rgb - 8 * (1 - a[..., None])) / np.maximum(a[..., None], .001), 0, 255)
rgba = Image.fromarray(np.dstack((colour, a * 255)).astype('uint8'))
logo = rgba.crop(rgba.getbbox())
logo.save(OUT / 'logo-natural.png')
for width in (256, 512):
    logo.resize((width, round(width * logo.height / logo.width)), Image.Resampling.LANCZOS).save(
        OUT / f'logo-natural-{width}.webp', lossless=True)
symbol = rgba.crop((125, 140, 515, 440))
symbol = symbol.crop(symbol.getbbox())
icon = ImageOps.pad(symbol, (512, 512), color=(0, 0, 0, 0))
for size in (16, 32, 180, 192, 512):
    icon.resize((size, size), Image.Resampling.LANCZOS).save(OUT / f'favicon-clear-{size}.png')
icon.save(OUT / 'favicon-clear.ico', sizes=[(16, 16), (32, 32), (48, 48)])
html = ROOT / 'index.html'
s = html.read_text(encoding='utf-8')
s = s.replace('logo-128.webp', 'logo-natural-256.webp').replace('logo-256.webp', 'logo-natural-512.webp').replace("assets/images/logo.png", "assets/images/logo-natural.png")
for size in (16, 32, 180):
    s = s.replace(f'favicon-{size}.png?v=2', f'favicon-clear-{size}.png?v=3')
s = s.replace('favicon.ico?v=2', 'favicon-clear.ico?v=3')
html.write_text(s, encoding='utf-8')
manifest_path = ROOT / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['icons'] = [{'src': f'assets/images/favicon-clear-{n}.png', 'sizes': f'{n}x{n}', 'type': 'image/png'} for n in (192, 512)]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Transparent logo:', logo.size, '| favicon: transparent symbol')
