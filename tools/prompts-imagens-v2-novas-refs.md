# Prompts V2 — estilo refs novas (claro, real, brasileiro)

Use estes para Hero + Tratamentos + Dia a dia.
Estilo Daniel V2: luz natural clara, pele real com textura,
sorriso brasileiro natural, luva azul clara, macro clinico nitido.
Nada de fundo preto pesado — tudo clean, clinica premium clara.

## Base para todos (cole junto)

```
bright premium dental photography, Brazilian patient, natural real skin
with texture, natural white teeth, soft daylight, clean modern clinic,
shallow depth of field, 85mm f1.8, ultra detailed, photorealistic, 8k
```

## Negativo

```
no text, no watermark, no logo, no yellow teeth, no distorted teeth,
no extra fingers, no deformed hands, no cartoon, no illustration,
no dark moody, no black background, no blood, no scary, no blurry
```

## HERO — hero.jpeg 16:9 + hero-mobile.jpg 3:4

Modelo: morena sorrindo olhos fechados com sol no rosto (sua ref cb6b).
Fundo claro quente, espaco a esquerda para titulo.

```
CENAS: close-up alegre
```

Prompt copiar:

```
joyful close-up of young Brazilian woman with dark hair smiling widely
with eyes closed, sun-kissed glowing skin, perfect natural white teeth,
hair strands softly over face, bright warm daylight, light blue sky
and white shirt, large empty negative space on left for headline text,
premium dental clinic hero campaign, natural skin texture, photorealistic --ar 16:9
```

Mobile: mesmo prompt + `--ar 3:4`

---

## TRATAMENTOS — 2:1

### servico-clinica-geral.jpg (sua ref 5de3 — espelho clinico)

```
clinical macro, dentist hand in light blue nitrile glove holding
dental mirror inside smiling Brazilian patient mouth, perfect white
lower teeth in sharp focus, soft bright clinic background blur,
premium general dentistry campaign, ultra sharp, photorealistic --ar 2:1
```

### servico-prevencao.jpg (sua ref 3fc8 — fio dental)

```
close-up of young Brazilian woman with curly hair flossing teeth
with white dental floss, bright bathroom with plants and daylight,
genuine smile, white teeth, fresh morning mood, prevention campaign,
natural skin texture, photorealistic --ar 2:1
```

### servico-clareamento.jpg (varie a ref cb6b — sorriso sol)

```
beauty close-up of Brazilian woman lower face, radiant white smile,
sunlit skin with natural glow, dark hair in wind, white background,
teeth whitening result campaign, hyper detailed teeth, photorealistic --ar 2:1
```

### servico-alinhadores.jpg

```
young Brazilian woman smiling holding transparent clear aligner
between fingers near smile, bright white studio background,
natural beauty, orthodontics lifestyle campaign, photorealistic --ar 2:1
```

### servico-lentes.jpg

```
extreme macro of perfect white dental veneers, Brazilian woman
lower face only, natural pink lips, flawless proportions,
soft white background, luxury smile design campaign,
ultra sharp, photorealistic --ar 2:1
```

### servico-dtm.jpg

```
calm portrait of Brazilian woman in profile, dentist hand in light
blue glove gently touching jaw joint, bright soft clinic light,
serene relief expression, premium facial pain treatment campaign,
photorealistic, no pain, no dark --ar 2:1
```

---

## DIA A DIA — 3:4 vertical (blog cover + hover tip)

### blog-1.jpg + tip-prevencao.jpg — fio dental / rotina

Cover:

```
lifestyle photo, young Brazilian woman with curly hair flossing
teeth smiling in bright bathroom with plants, morning daylight,
fresh minimal aesthetic, photorealistic --ar 3:4
```

Hover:

```
macro of white dental floss between perfect teeth detail,
bright clean background, premium hygiene detail, photorealistic --ar 3:4
```

### blog-2.jpg + tip-clareamento.jpg — sorriso sol

Cover:

```
beauty close-up Brazilian woman laughing with eyes closed,
sunlit perfect white smile, dark hair in wind, light blue sky,
summer glow, photorealistic --ar 3:4
```

Hover:

```
macro of white teeth smile with dental shade guide in blue glove,
bright clinical background, whitening comparison, photorealistic --ar 3:4
```

### blog-3.jpg + tip-alinhadores.jpg — consulta / espelho

Cover:

```
dentist hand in blue glove with dental mirror near smiling
Brazilian patient mouth, bright modern clinic, check-up moment,
photorealistic --ar 3:4
```

Hover:

```
close-up of transparent clear aligner held in fingers over bright
background, white smile blurred behind, photorealistic --ar 3:4
```

---

## Como aplicar

1. Gere no Midjourney / Firefly / Flux com os blocos acima.
2. Salve os escolhidos em `assets/originals/` com o nome exato
   (hero.jpeg, hero-mobile.jpg, servico-*.jpg, blog-*.jpg, tip-*.jpg).
3. Rode `python tools/build-images.py` — ele gera webp/jpg/avif nos cortes.


