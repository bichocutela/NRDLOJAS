import csv
import re
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

products = []
with open("products.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        if len(row) < 2: continue
        code = row[0].strip()
        name = row[1].strip()
        
        # simple heuristic for category and unit
        category = "Geral"
        if "CESTA" in name: category = "Cestas"
        elif "ÁGUA" in name or "GARRAFÃO" in name or "SUCO" in name: category = "Bebidas"
        elif "PIZZA" in name or "SALGADO" in name or "PÃO" in name or "BRIOCHE" in name: category = "Padaria"
        elif "FRANGO" in name or "CAMARAO" in name: category = "Açougue"
        else: category = "Hortifruti"
        
        unit = "un"
        if "QUILOGRAMA" in name or " K G" in name or " KG" in name: unit = "kg"
        elif "UNIDADE" in name or " UM" in name: unit = "un"
        elif " 500G" in name or " 1KG" in name or " 600G" in name or " 200G" in name or " 100G" in name or " 125G" in name or " 300G" in name or " 150G" in name: unit = "un"
        
        # clean name a bit for display
        display_name = name.title()
        
        # searchname
        search_name = remove_accents(name.lower()).replace(' quilograma', '').replace(' unidade', '').strip()
        
        products.append(f'            Product(code = "{code}", name = "{display_name}", searchName = "{search_name}", category = "{category}", unit = "{unit}", searchCount = 0)')

print("        val importedProducts = listOf(")
print(",\n".join(products))
print("        )")
