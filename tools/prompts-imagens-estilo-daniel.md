# Prompts de imagens — estilo Projeto Daniel (LAVIC)

Como usar: copie o bloco EN no Midjourney / Flux / Ideogram / Firefly.
Salve em `assets/originals/` com o nome indicado e rode `python tools/build-images.py`.

Paleta LAVIC: charcoal `#121216` + dourado `#C9A560` + creme `#F7F3EC`.
Luvas: azul `#1E5AA8` (clinico) / lavanda (orto) / preto (macro premium).

## DNA de estilo (cole junto em todos)

```
premium dental editorial photography, Brazilian dental clinic, ultra-detailed,
cinematic studio lighting, soft gold rim light, shallow depth of field,
85mm f/1.8, natural skin texture, no over-retouch, hyperrealistic
```

## Negativo universal

```
no text, no watermark, no logo, no distorted teeth, no extra fingers,
no deformed hands, no cartoon, no illustration, no oversaturated,
no blurry, no low-res, no yellow stained teeth, no scary, no blood
```

---

## 1) HERO — `hero.jpeg` (16:9) + `hero-mobile.jpg` (3:4)

Fusao da ref 1 (spray + fundo escuro) + ref 2 (sorriso beauty).
Precisa de espaco vazio a esquerda para o titulo.

**Prompt EN (copiar):**

```
cinematic wide hero photograph, beautiful Brazilian woman with dark slicked-back hair,
radiant natural white smile, dewy glowing skin, hand gently near eye in joyful expression,
dark charcoal studio background, fine water mist spray with golden backlight on left side,
large empty negative space on left third for text overlay, premium dental clinic campaign,
editorial beauty lighting, soft gold rim light, ultra-detailed, 85mm f1.8,
shallow depth of field, photorealistic, 8k --ar 16:9 --style raw --v 6.1
```

**Variacao B (mais clinica):**

```
premium dental hero, smiling Brazilian couple, natural perfect teeth,
dentist hand in blue nitrile glove holding modern dental handpiece with fine water spray,
dark moody charcoal background, golden rim light, copy space on left for headline,
cinematic, ultra sharp macro detail, photorealistic --ar 16:9 --style raw
```

Mobile: mesmo prompt + `--ar 3:4`, salvar como `hero-mobile.jpg`.

---

## 2) TRATAMENTOS — cards 2:1 (720x360)

### 2.1 `servico-clinica-geral.jpg` — igual ref 1 (spray)

```
macro photograph of dentist hand in blue nitrile glove holding modern
stainless steel dental handpiece spraying fine water mist,
dark charcoal black studio background, dramatic side lighting
with warm golden highlight, frozen water droplets in air,
ultra sharp, premium dental equipment campaign, photorealistic --ar 2:1
```

### 2.2 `servico-prevencao.jpg` — igual ref 5 (higiene dia a dia)

```
editorial beauty close-up, young Brazilian woman with freckles
and natural glowing skin brushing teeth with premium minimalist
metallic toothbrush, genuine happy smile, white teeth,
soft beige cream studio background, natural daylight,
skin texture visible, dental hygiene campaign,
photorealistic, 85mm --ar 2:1
```

### 2.3 `servico-clareamento.jpg` — igual ref 2 (branco puro)

```
beauty portrait of Brazilian woman with dark slicked hair,
eyes closed smiling joyfully, perfect ultra-white natural teeth,
dewy luminous skin, hand elegantly near face, pure white studio
background, high-key softbox lighting, premium teeth whitening
campaign, hyper-detailed teeth, photorealistic --ar 2:1
```

### 2.4 `servico-lentes.jpg` — facetas / detalhe estetica

```
extreme macro of perfect white dental veneers smile,
Brazilian woman lower face only, natural pink lips,
flawless teeth proportions, soft white background with subtle
gold reflector glow, luxury dental aesthetics campaign,
ultra sharp, photorealistic --ar 2:1
```

### 2.5 `servico-alinhadores.jpg` — igual ref 4 (orto macro)

```
clinical macro photograph, dentist hands in lavender purple gloves
adjusting metal orthodontic braces on young Brazilian female patient
smile with dental instrument, soft clinical blue background blur,
sharp focus on brackets, premium orthodontics campaign,
photorealistic, ultra-detailed --ar 2:1
```

Variacao alinhador invisivel (se preferir sem metal):

```
dentist hand in black glove holding transparent clear aligner
over dark background, perfect white smile of Brazilian woman
blurred behind, studio premium lighting, invisible orthodontics
campaign, photorealistic --ar 2:1
```

### 2.6 `servico-dtm.jpg` — DTM / bruxismo

```
cinematic portrait of Brazilian woman in profile holding jaw with
hand expressing relief after treatment, dentist hand in blue glove
gently examining jaw joint, dark charcoal studio background,
soft golden rim light, calm premium mood, temporomandibular joint
treatment campaign, photorealistic, serene, no pain expression --ar 2:1
```

---

## 3) CUIDADOS DIA A DIA — cards 3:4 (600x800)

Estilo: beauty editorial claro, pele real, fundo branco/creme.
Cover = lifestyle claro. Hover = macro clinico escuro.

### 3.1 Prevencao — `blog-1.jpg` (cover) + `tip-prevencao.jpg` (hover)

Cover clara:

```
lifestyle editorial, happy Brazilian woman brushing teeth
in bright modern bathroom, morning natural light, cream tiles,
fresh minimal aesthetic, genuine smile, photorealistic --ar 3:4
```

Hover macro premium escuro:

```
macro of metallic toothbrush bristles with water droplets,
black glove hand, dark charcoal background with gold backlight,
premium hygiene detail, photorealistic --ar 3:4
```

### 3.2 Estetica — `blog-2.jpg` (cover) + `tip-clareamento.jpg` (hover)

Cover:

```
beauty close-up Brazilian woman perfect white smile holding small
mirror, white background, dewy skin, natural makeup, teeth whitening
result campaign, photorealistic --ar 3:4
```

Hover:

```
before-after style macro of white teeth smile detail,
dentist shade guide in blue glove next to smile,
dark premium background, clinical aesthetic, photorealistic --ar 3:4
```

### 3.3 Ortodontia — `blog-3.jpg` (cover) + `tip-alinhadores.jpg` (hover)

Cover:

```
young Brazilian woman smiling holding transparent clear aligner
in fingers near smile, bright white studio background, natural beauty,
orthodontics lifestyle campaign, photorealistic --ar 3:4
```

Hover (igual ref 3 — implante premium):

```
macro photograph of dental implant with ceramic crown held between
fingers in black nitrile gloves, pure black studio background,
dramatic premium lighting, ultra sharp titanium detail,
implantology campaign, photorealistic --ar 3:4
```

---

## Dicas para ficar igual Daniel

1. Gere em dobro e escolha pele com textura (evite smooth skin).
2. Modelos brasileiros: adicione `Brazilian, mixed skin tone, dark hair`.
3. Escuro = charcoal + gold rim. Claro = white/beige high-key softbox.
4. Salve o original em 2048px+ e deixe o build-images.py cortar.
5. Dente torto/dedo extra? Regenere com `perfect hands, perfect teeth`.


