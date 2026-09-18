from pathlib import Path
p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")
old = '"url": "https://www.google.com/maps/search/?api=1&query=LAVIC+Odontologia",'
assert old in t, "bloco url nao encontrado"
t = t.replace(old, '"url": "https://www.google.com/maps/search/?api=1\\u0026query=LAVIC+Odontologia",\n  "telephone": "+55-11-94068-9803",\n  "address": {"@type": "PostalAddress", "streetAddress": "Av. Imperatriz Leopoldina, 957 - Sala 1205", "addressLocality": "S\\u00e3o Paulo", "addressRegion": "SP", "postalCode": "05305-001", "addressCountry": "BR"},')
p.write_text(t, encoding="utf-8")
print("ok — schema com telefone + endereco")
