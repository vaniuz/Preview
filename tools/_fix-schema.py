from pathlib import Path
p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
reps = [
    ("https://SEU-DOMINIO.com.br/assets/images/hero.jpeg", "assets/images/hero.jpeg"),
    ("https://SEU-DOMINIO.com.br/", "https://www.google.com/maps/search/?api=1&query=LAVIC+Odontologia"),
]
n = 0
for a, b in reps:
    n += t.count(a)
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("substituicoes SEU-DOMINIO:", n)
print("restam SEU-DOMINIO:", t.count("SEU-DOMINIO"))
print("tem telefone real:", "94068-9803" in t or "+55-11-0000-0000" in t)
