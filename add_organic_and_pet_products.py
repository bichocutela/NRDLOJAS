import re
import sys

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[áàãâä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòõôö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

pet_products = [
    ("0000000204110", "RACAO GATOS WHISKAS ADULT CARNE AG KG", "Pet Shop", "kg"),
    ("0000000204130", "RACAO GATOS WHISKAS GATO CAST CAR AG KG", "Pet Shop", "kg"),
    ("0000000204170", "RACAO GATOS WHISKAS ADULT PEIXE AG KG", "Pet Shop", "kg"),
]

organic_products = [
    ("0751320164551", "ABOBRINHA VERDE ORGANICO 1KG", "Hortifruti", "un"),
    ("7898949599029", "ALFACE AMERICANA ORGANICA UN", "Hortifruti", "un"),
    ("7898949599036", "ALFACE CRESPA ORGANICA UN", "Hortifruti", "un"),
    ("7898949599050", "ALFACE LISA ORGANICA UN", "Hortifruti", "un"),
    ("7898949599067", "ALFACE MIMOSA ORGANICO UND", "Hortifruti", "un"),
    ("7898949599043", "ALFACE ROXA ORGANICA UN", "Hortifruti", "un"),
    ("251234", "BANANA ORGANICA PACOVAN KG", "Hortifruti", "kg"),
    ("251235", "BATATA DOCE ORGANICA HORTAVIVA KG", "Hortifruti", "kg"),
    ("0751320164568", "BATATA DOCE ORGANICO 500G", "Hortifruti", "un"),
    ("0751320164629", "BETERRABA ORGANICO 500G", "Hortifruti", "un"),
    ("0751320888518", "CEBOLA ORGANICA 500G", "Hortifruti", "un"),
    ("7898949599111", "CEBOLINHA ORGANICA UND", "Hortifruti", "un"),
    ("7898963133100", "CENOURA ORGANICO 600G", "Hortifruti", "un"),
    ("7898963133209", "CHUCHU ORGANICO 600G", "Hortifruti", "un"),
    ("251291", "COENTRO ORGANICO UN", "Hortifruti", "un"),
    ("251332", "COUVE FOLHA ORGANICA UN", "Hortifruti", "un"),
    ("789894959166", "ESPINAFRE ORGANICO UN", "Hortifruti", "un"),
    ("7898910185121", "GOMA FRESCA DELICIA POTIGUAR ORGANICO", "Hortifruti", "kg"),
    ("0751320164469", "GOIABA ORGANICA 500G", "Hortifruti", "un"),
    ("7898949599180", "HORTELA ORGANICO UND", "Hortifruti", "un"),
    ("253303", "MANGA ROSA ORGANICA KG", "Hortifruti", "kg"),
    ("253282", "MAMAO FORMOSA ORGANICO", "Hortifruti", "kg"),
    ("253295", "MANGA TOMMY ORGANICA KG", "Hortifruti", "kg"),
    ("251486", "MANJERICAO ORGANICO UND", "Hortifruti", "un"),
    ("2019355", "MILHO ORGANICO 600G", "Hortifruti", "un"),
    ("0751320164490", "PIMENTA CHEIRO ORGANICA 100G", "Hortifruti", "un"),
    ("2017843", "PIMENTA CHEIRO ORGANICA 150G", "Hortifruti", "un"),
    ("0751320164513", "PIMENTA DEDO MOCA ORGANICA 200G", "Hortifruti", "un"),
    ("7898963133247", "PIMENTAO VERDE ORGANICO 300G", "Hortifruti", "un"),
    ("7898949599210", "RUCULA ORGANICA UN", "Hortifruti", "un"),
    ("7898949599227", "SALSA ORGANICA MOLHO", "Hortifruti", "un"),
    ("0751320164544", "TOMATE ORGANICO 500G", "Hortifruti", "un"),
    ("251008", "QUIABO HORTAVIVA", "Hortifruti", "kg"),
    ("251094", "TOMATE CEREJA HORTAVIVA", "Hortifruti", "kg"),
    ("251235", "BATATA DOCE HORTAVIVA", "Hortifruti", "kg"),
    ("250173", "BERINGELA HORTAVIVA", "Hortifruti", "kg"),
]

all_new_products = pet_products + organic_products

new_lines = []
for code, name, category, unit in all_new_products:
    search_name = normalize_text(name)
    new_lines.append(f'            Product(code = "{code}", name = "{name}", searchName = "{search_name}", category = "{category}", unit = "{unit}", searchCount = 0),')

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

target = '            Product(code = "7896029051543", name = "WHISKAS LATA ADULTO SARDINHA 290G", searchName = "whiskas lata adulto sardinha 290g", category = "Pet Shop", unit = "un", searchCount = 0)'
replacement = target + ",\n" + "\n".join(new_lines)

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
        f.write(content)
    print("Products added successfully.")
else:
    print("Target not found in file.")

