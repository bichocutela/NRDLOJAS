import re

file_path = "app/src/main/java/com/example/data/ProductRepository.kt"
with open(file_path, "r") as f:
    content = f.read()

replacements = {
    '"Bri Creme"': '"Brioche de Creme"',
    '"Bri Especial"': '"Brioche Especial"',
    '"Bri Leite Pó"': '"Brioche de Leite em Pó"',
    '"Baguete Ger"': '"Baguete com Gergelim"',
    '"Baguete Inte"': '"Baguete Integral"',
    '"Pão Dark Castan"': '"Pão Dark com Castanhas"',
    '"Sobrecoxa S/ Pele Bom Todo"': '"Sobrecoxa Sem Pele Bom Todo"',
    '"Coxa/Sobrecoxa"': '"Coxa e Sobrecoxa de Frango"',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w") as f:
    f.write(content)
