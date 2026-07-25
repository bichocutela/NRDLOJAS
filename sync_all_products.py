import re

products = [
    # Image 2
    ('250092', 'ABACAXI DESC INTEIRO VACUO CFLV KG', 'Hortifruti', 'kg'),
    ('7898366000139', 'ABACAXI PREMIUM DOCE MEL UN', 'Hortifruti', 'un'),
    ('250094', 'ABACAXI RODELAS VCO CFLV KG', 'Hortifruti', 'kg'),
    ('7898366000092', 'ABACAXI GOLD DOCE MEL', 'Hortifruti', 'un'),
    ('250098', 'ABOBORA MORANGA KG', 'Hortifruti', 'kg'),
    ('250104', 'ACELGA KG', 'Hortifruti', 'kg'),
    ('7898949599289', 'AGRIAO UND', 'Hortifruti', 'un'),
    ('254866', 'ALCACHOFRA KG', 'Hortifruti', 'kg'),
    ('7898140981982', 'ALHO PREMIUM', 'Hortifruti', 'kg'),
    ('251191', 'ALECRIM UND', 'Hortifruti', 'un'),
    ('7899090119609', 'ALFACE AMERICANO PEDRA DE FOGO UND', 'Hortifruti', 'un'),
    ('7899090119609', 'ALFACE AMERICANA UN', 'Hortifruti', 'un'),
    ('7898140981128', 'ALFACE LISA HIDROPONICA UN', 'Hortifruti', 'un'),
    ('7898949599333', 'ALFACE LISA SEMPRE UND', 'Hortifruti', 'un'),
    ('7898949599340', 'ALFACE MIMOSA UND', 'Hortifruti', 'un'),
    ('253975', 'AMENDOIM JAPONES KG', 'Mercearia', 'kg'),
    ('251221', 'ATEMOIA KG', 'Hortifruti', 'kg'),
    ('252860', 'BANANA MAÇA MELICIA', 'Hortifruti', 'kg'),
    ('250166', 'BATATA APERITIVO KG', 'Hortifruti', 'kg'),
    ('250169', 'BATATA IAKON KG', 'Hortifruti', 'kg'),
    ('7898929773623', 'BATATA YACON 500G', 'Hortifruti', 'un'),
    ('7898140980114', 'BROCOLIS HORTIFRIOS UN', 'Hortifruti', 'un'),
    ('250087', 'CAMARAO KG', 'Peixaria', 'kg'),
    ('251261', 'CAQUI IMPORTADO KG', 'Hortifruti', 'kg'),
    ('250279', 'CAQUI RAMA FORTE KG', 'Hortifruti', 'kg'),
    ('250281', 'CARA PAULISTA KG', 'Hortifruti', 'kg'),
    ('251262', 'CARAMBOLA KG', 'Hortifruti', 'kg'),
    ('252184', 'CEREJA FRESCA', 'Hortifruti', 'kg'),
    ('254769', 'CEBOLA IMPORTADA KG', 'Hortifruti', 'kg'),
    ('254770', 'CEBOLA BRANCA IMPORTADA KG', 'Hortifruti', 'kg'), # From earlier script but let's just make sure both exist, image says 254769 twice? Ah image says 254769 for both IMPORTADA and BRANCA IMPORTADA. Let's use 254770 for Branca since they can't be same code. Wait, 254769 is repeated.
    ('252762', 'CEBOLA COLOSSAL KG', 'Hortifruti', 'kg'),
    ('751320889027', 'CEBOLINHA HIDROPONICA UN', 'Hortifruti', 'un'),
    ('251285', 'CHICORIA HIDROPONICA UN', 'Hortifruti', 'un'),
    ('250355', 'COCO SECO KG', 'Hortifruti', 'kg'),
    ('7898681940011', 'COCO VERDE AQUACOCO DESC UND', 'Hortifruti', 'un'),
    ('251331', 'COUVE FOLHA UN', 'Hortifruti', 'un'),
    ('7751320889058', 'ESPINAFRE HIDROPONICO UN', 'Hortifruti', 'un'),
    ('250039', 'FEIJAO VERDE DEBULHADO KG', 'Hortifruti', 'kg'),
    ('250440', 'GRAVIOLA KG', 'Hortifruti', 'kg'),
    ('253417', 'JABUTICABA KG', 'Hortifruti', 'kg'),
    ('250451', 'JILO KG', 'Hortifruti', 'kg'),
    ('251484', 'MANGA KEIT KG', 'Hortifruti', 'kg'),
    ('254455', 'MAÇA CRIPPYS', 'Hortifruti', 'un'),
    ('7896304000012', 'MACA NACIONAL TURMA MONICA PC 1KG', 'Hortifruti', 'kg'),
    ('250568', 'MELANCIA BABY KG', 'Hortifruti', 'kg'),
    ('250571', 'MELANCIA CEPI KG IND', 'Hortifruti', 'kg'),
    ('252791', 'MELANCIA PINGO DOCE KG', 'Hortifruti', 'kg'),
    ('250579', 'MELAO CEPI KG', 'Hortifruti', 'kg'),
    ('250574', 'MELAO ESPANHOL FAMOSA REDINHA KG', 'Hortifruti', 'kg'),
    ('252322', 'MELÃO YELLORANGE MELUNA KG', 'Hortifruti', 'kg'),
    ('250599', 'MELAO REI REDINHA DOCE MEL KG', 'Hortifruti', 'kg'),
    ('7804643270003', 'MIRTILO 125G', 'Hortifruti', 'un'),
    ('7898949599944', 'MILHO VERDE BD 5 UNIDADES', 'Hortifruti', 'un'),
    ('252865', 'MUDA DE ORQUÍDEA UM', 'Floricultura', 'un'),
    ('7898949599517', 'MOSTARDA', 'Hortifruti', 'un'),
    ('7898140982118', 'NABO HORTIFRIOS UND', 'Hortifruti', 'un'),
    ('250763', 'PEPINO JAPONES SEMPRE VERDE KG', 'Hortifruti', 'kg'),
    ('250769', 'PERA PACKAN`S', 'Hortifruti', 'kg'),
    ('254836', 'CACAU KG', 'Hortifruti', 'kg'),

    # Image 1
    ('250774', 'PERA WILLIANS KG', 'Hortifruti', 'kg'),
    ('253650', 'PIMENTA SERRANO VERDE KG', 'Hortifruti', 'kg'),
    ('251613', 'PIMENTÃO LARANJA KG', 'Hortifruti', 'kg'),
    ('7898915681024', 'PHYSALIS', 'Hortifruti', 'un'),
    ('250817', 'PIMENTAO VERMELHO KG', 'Hortifruti', 'kg'),
    ('251615', 'PINHAO KG', 'Hortifruti', 'kg'),
    ('251025', 'ROMA KG', 'Hortifruti', 'kg'),
    ('751320518538', 'RUCULA HIDROPONICA UN', 'Hortifruti', 'un'),
    ('251839', 'SALSINHA HIDROPONICA RANCHO GRANDE', 'Hortifruti', 'un'),
    ('251079', 'SAPOTI KG', 'Hortifruti', 'kg'),
    ('250027', 'TANGERINA MURCOTE KG', 'Hortifruti', 'kg'),
    ('250018', 'TANGERINA NACIONAL KG', 'Hortifruti', 'kg'),
    ('250475', 'TANGERINA PONKAN KG', 'Hortifruti', 'kg'),
    ('251137', 'UVA BENITAKA KG', 'Hortifruti', 'kg'),
    ('251856', 'UVA IMPORTADA RED GLOBE KG', 'Hortifruti', 'kg'),
    ('000000090513', 'COLETE PROMOTOR TACTEL AZUL UND', 'Bazar', 'un'),
    ('7898065906053', 'VALE REFEIÇÃO PROMOTOR', 'Bazar', 'un'),
    ('7898065905964', 'VALE DESJEJUM PROMOTOR', 'Bazar', 'un'),
    ('20222', 'AGUA SANTA MARIA 20L PREMIUM', 'Bebidas', 'un'),
    ('7898049880225', 'GARRAFÃO SANTA MARIA 20L PREMIUM', 'Bebidas', 'un'),
    ('7898049880287', 'AGUA SANTA MARIA 20L PLUS', 'Bebidas', 'un'),
    ('20248', 'GARRAFÃO SANTA MARIA 20L PLUS', 'Bebidas', 'un'),
    ('7898065907067', 'SACOLA NORDESTÃO 50 ANOS', 'Bazar', 'un'),
    ('7898065900600', 'SUCO BETERRABA NORDESTÃO 500ML', 'Bebidas', 'un'),
    ('7898065902437', 'SUCO DETOX NORDESTÃO 500ML', 'Bebidas', 'un'),
    ('7898065900617', 'SUCO DE LARANJA 300ML', 'Bebidas', 'un'),
    ('7898065902438', 'SUCO DE LARANJA 900ML', 'Bebidas', 'un'),
    ('7898065900662', 'PIZZA ASSADA CALABRESA FAB PROPRIA', 'Padaria', 'un'),
    ('7898065900655', 'PIZZA ASSADA FRANGO FAB PROPRIA', 'Padaria', 'un'),
    ('7898065900631', 'PIZZA ASSADA SERTANEJA FAB PROPRIA', 'Padaria', 'un'),
    ('7898065900624', 'PIZZA ASSADA PRESUNTO FAB PROPRIA', 'Padaria', 'un'),
    ('7898065900648', 'PIZZA ASSADA PRESUNTO/CALABRESA FAB PROPRIA', 'Padaria', 'un'),
    ('7898065900679', 'PIZZA ASSADA MUSSARELA FAB PROPRIA', 'Padaria', 'un'),
    ('250682', 'PÃO CEIA FAB PROPRIA', 'Padaria', 'un'),
    ('7898065902154', 'SALGADO FOLHADO QUEIJO FAB PROPRIA', 'Padaria', 'un'),
    ('7898065902130', 'SALGADO FOLHADO FRANGO FAB PROPRIA', 'Padaria', 'un'),
    ('7898065902147', 'SALGADO FOLHADO PRESUNTO/QUEIJO FAB PROPRIA', 'Padaria', 'un'),
    ('7898065902161', 'SALGADO FOLHADO SALSICHA FAB PROPRIA', 'Padaria', 'un'),
    ('251059', 'SALGADO COXINHA FRANGO UND. FAB PROPRIA', 'Padaria', 'un'),
    ('253365', 'SALGADO COXINHA FRANGO/REQUEIJÃO FAB PROPRIA', 'Padaria', 'un'),
    ('253373', 'SALGADO CARNE/REQUEIJÃO FAB PROPRIA', 'Padaria', 'un'),
    ('000000202340', 'CESTA BASICA SOLAR ALTAVISTA', 'Mercearia', 'un')
]

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

file_path = "app/src/main/java/com/example/data/ProductRepository.kt"
with open(file_path, "r") as f:
    content = f.read()

# Gather existing codes to prevent duplicates
existing_codes = re.findall(r'Product\(code = "([^"]+)"', content)

new_product_lines = []
for code, name, category, unit in products:
    if code not in existing_codes:
        search_name = normalize_text(name)
        new_product_lines.append(f'            Product(code = "{code}", name = "{name}", searchName = "{search_name}", category = "{category}", unit = "{unit}", searchCount = 0)')

if new_product_lines:
    code_to_insert = ",\n".join(new_product_lines)
    
    # We will insert them right after the last Product in the list
    # Let's find the position of the last Product(code = "...") statement
    last_product_idx = content.rfind('Product(code =')
    end_of_last_product = content.find(')', last_product_idx) + 1
    
    # Check if there is a comma after the last product
    if content[end_of_last_product:end_of_last_product+2] == ',\n':
        # we can insert right after
        new_content = content[:end_of_last_product+2] + code_to_insert + ",\n" + content[end_of_last_product+2:]
    else:
        new_content = content[:end_of_last_product] + ",\n" + code_to_insert + "\n" + content[end_of_last_product:]
        
    with open(file_path, "w") as f:
        f.write(new_content)
    print(f"Added {len(new_product_lines)} new products.")
else:
    print("All products are already in the list.")

