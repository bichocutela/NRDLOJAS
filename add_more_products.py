import re

file_path = "app/src/main/java/com/example/data/ProductRepository.kt"

new_products = [
    # Image 1
    ('250092', 'ABACAXI DESC INTEIRO VACUO CFLV KG', 'abacaxi desc inteiro vacuo cflv', 'Hortifruti', 'kg'),
    ('7898366000139', 'ABACAXI PREMIUM DOCE MEL UN', 'abacaxi premium doce mel', 'Hortifruti', 'un'),
    ('250094', 'ABACAXI RODELAS VCO CFLV KG', 'abacaxi rodelas vco cflv', 'Hortifruti', 'kg'),
    ('7898366000092', 'ABACAXI GOLD DOCE MEL', 'abacaxi gold doce mel', 'Hortifruti', 'un'),
    ('250098', 'ABOBORA MORANGA KG', 'abobora moranga', 'Hortifruti', 'kg'),
    ('250104', 'ACELGA KG', 'acelga', 'Hortifruti', 'kg'),
    ('7898949599289', 'AGRIAO UND', 'agriao', 'Hortifruti', 'un'),
    ('254866', 'ALCACHOFRA KG', 'alcachofra', 'Hortifruti', 'kg'),
    ('7898140981982', 'ALHO PREMIUM', 'alho premium', 'Hortifruti', 'kg'),
    ('251191', 'ALECRIM UND', 'alecrim', 'Hortifruti', 'un'),
    ('7899090119609', 'ALFACE AMERICANO PEDRA DE FOGO UND.', 'alface americano pedra de fogo', 'Hortifruti', 'un'),
    ('7899090119616', 'ALFACE AMERICANA UN', 'alface americana', 'Hortifruti', 'un'),
    ('7898140981128', 'ALFACE LISA HIDROPONICA UN', 'alface lisa hidroponica', 'Hortifruti', 'un'),
    ('7898949599333', 'ALFACE LISA SEMPRE UND', 'alface lisa sempre', 'Hortifruti', 'un'),
    ('7898949599340', 'ALFACE MIMOSA UND', 'alface mimosa', 'Hortifruti', 'un'),
    ('253975', 'AMENDOIM JAPONES KG', 'amendoim japones', 'Mercearia', 'kg'),
    ('251221', 'ATEMOIA KG', 'atemoia', 'Hortifruti', 'kg'),
    ('252860', 'BANANA MAÇA MELICIA', 'banana maca melicia', 'Hortifruti', 'kg'),
    ('250166', 'BATATA APERITIVO KG', 'batata aperitivo', 'Hortifruti', 'kg'),
    ('250169', 'BATATA IAKON KG', 'batata iakon', 'Hortifruti', 'kg'),
    ('7898929773623', 'BATATA YACON 500G', 'batata yacon', 'Hortifruti', 'un'),
    ('7898140980114', 'BROCOLIS HORTIFRIOS UN', 'brocolis hortifrios', 'Hortifruti', 'un'),
    ('250087', 'CAMARAO KG', 'camarao', 'Peixaria', 'kg'),
    ('251261', 'CAQUI IMPORTADO KG', 'caqui importado', 'Hortifruti', 'kg'),
    ('250279', 'CAQUI RAMA FORTE KG', 'caqui rama forte', 'Hortifruti', 'kg'),
    ('250281', 'CARA PAULISTA KG', 'cara paulista', 'Hortifruti', 'kg'),
    ('251262', 'CARAMBOLA KG', 'carambola', 'Hortifruti', 'kg'),
    ('252184', 'CEREJA FRESCA', 'cereja fresca', 'Hortifruti', 'kg'),
    ('254769', 'CEBOLA IMPORTADA KG', 'cebola importada', 'Hortifruti', 'kg'),
    ('254770', 'CEBOLA BRANCA IMPORTADA KG', 'cebola branca importada', 'Hortifruti', 'kg'),
    ('252762', 'CEBOLA COLOSSAL KG', 'cebola colossal', 'Hortifruti', 'kg'),
    ('751320889027', 'CEBOLINHA HIDROPONICA UN', 'cebolinha hidroponica', 'Hortifruti', 'un'),
    ('251285', 'CHICORIA HIDROPONICA UN', 'chicoria hidroponica', 'Hortifruti', 'un'),
    ('250355', 'COCO SECO KG', 'coco seco', 'Hortifruti', 'kg'),
    ('7898681940011', 'COCO VERDE AQUACOCO DESC UND', 'coco verde aquacoco desc', 'Hortifruti', 'un'),
    ('251331', 'COUVE FOLHA UN', 'couve folha', 'Hortifruti', 'un'),
    ('7751320889058', 'ESPINAFRE HIDROPONICO UN', 'espinafre hidroponico', 'Hortifruti', 'un'),
    ('250039', 'FEIJAO VERDE DEBULHADO KG', 'feijao verde debulhado', 'Hortifruti', 'kg'),
    ('250440', 'GRAVIOLA KG', 'graviola', 'Hortifruti', 'kg'),
    ('253417', 'JABUTICABA KG', 'jabuticaba', 'Hortifruti', 'kg'),
    ('250451', 'JILO KG', 'jilo', 'Hortifruti', 'kg'),
    ('251484', 'MANGA KEIT KG', 'manga keit', 'Hortifruti', 'kg'),
    ('254455', 'MAÇA CRIPPYS', 'maca crippys', 'Hortifruti', 'kg'),
    ('7896304000012', 'MACA NACIONAL TURMA MONICA PC 1KG', 'maca nacional turma monica', 'Hortifruti', 'un'),
    ('250568', 'MELANCIA BABY KG', 'melancia baby', 'Hortifruti', 'kg'),
    ('250571', 'MELANCIA CEPI KG IND', 'melancia cepi ind', 'Hortifruti', 'kg'),
    ('252791', 'MELANCIA PINGO DOCE KG', 'melancia pingo doce', 'Hortifruti', 'kg'),
    ('250579', 'MELAO CEPI KG', 'melao cepi', 'Hortifruti', 'kg'),
    ('250574', 'MELAO ESPANHOL FAMOSA REDINHA KG', 'melao espanhol famosa redinha', 'Hortifruti', 'kg'),
    ('252322', 'MELÃO YELLORANGE MELUNA KG', 'melao yellorange meluna', 'Hortifruti', 'kg'),
    ('250599', 'MELAO REI REDINHA DOCE MEL KG', 'melao rei redinha doce mel', 'Hortifruti', 'kg'),
    ('7804643270003', 'MIRTILO 125G', 'mirtilo', 'Hortifruti', 'un'),
    ('7898949599944', 'MILHO VERDE BD 5 UNIDADES', 'milho verde bd 5 unidades', 'Hortifruti', 'un'),
    ('252865', 'MUDA DE ORQUÍDEA UM', 'muda de orquidea', 'Floricultura', 'un'),
    ('7898949599517', 'MOSTARDA', 'mostarda', 'Hortifruti', 'un'),
    ('7898140982118', 'NABO HORTIFRIOS UND.', 'nabo hortifrios', 'Hortifruti', 'un'),
    ('250763', 'PEPINO JAPONES SEMPRE VERDE KG', 'pepino japones sempre verde', 'Hortifruti', 'kg'),
    ('250769', 'PERA PACKAN`S', 'pera packans', 'Hortifruti', 'kg'),
    ('254836', 'CACAU KG', 'cacau', 'Hortifruti', 'kg'),
    
    # Image 2
    ('250774', 'PERA WILLIANS KG', 'pera willians', 'Hortifruti', 'kg'),
    ('253650', 'PIMENTA SERRANO VERDE KG', 'pimenta serrano verde', 'Hortifruti', 'kg'),
    ('251613', 'PIMENTÃO LARANJA KG', 'pimentao laranja', 'Hortifruti', 'kg'),
    ('7898915681024', 'PHYSALIS', 'physalis', 'Hortifruti', 'un'),
    ('250817', 'PIMENTAO VERMELHO KG', 'pimentao vermelho', 'Hortifruti', 'kg'),
    ('251615', 'PINHAO KG', 'pinhao', 'Hortifruti', 'kg'),
    ('251025', 'ROMA KG', 'roma', 'Hortifruti', 'kg'),
    ('751320518538', 'RUCULA HIDROPONICA UN', 'rucula hidroponica', 'Hortifruti', 'un'),
    ('251839', 'SALSINHA HIDROPONICA RANCHO GRANDE', 'salsinha hidroponica rancho grande', 'Hortifruti', 'un'),
    ('251079', 'SAPOTI KG', 'sapoti', 'Hortifruti', 'kg'),
    ('250027', 'TANGERINA MURCOTE KG', 'tangerina murcote', 'Hortifruti', 'kg'),
    ('250018', 'TANGERINA NACIONAL KG', 'tangerina nacional', 'Hortifruti', 'kg'),
    ('250475', 'TANGERINA PONKAN KG', 'tangerina ponkan', 'Hortifruti', 'kg'),
    ('251137', 'UVA BENITAKA KG', 'uva benitaka', 'Hortifruti', 'kg'),
    ('251856', 'UVA IMPORTADA RED GLOBE KG', 'uva importada red globe', 'Hortifruti', 'kg'),
    ('20222', 'AGUA SANTA MARIA 20L PREMIUM', 'agua santa maria 20l premium', 'Bebidas', 'un'),
    ('7898049880225', 'GARRAFÃO SANTA MARIA 20L PREMIUM', 'garrafao santa maria 20l premium', 'Bebidas', 'un'),
    ('7898049880287', 'AGUA SANTA MARIA 20L PLUS', 'agua santa maria 20l plus', 'Bebidas', 'un'),
    ('20248', 'GARRAFÃO SANTA MARIA 20L PLUS', 'garrafao santa maria 20l plus', 'Bebidas', 'un'),
    ('7898065907067', 'SACOLA NORDESTÃO 50 ANOS', 'sacola nordestao 50 anos', 'Bazar', 'un'),
    ('7898065900600', 'SUCO BETERRABA NORDESTÃO 500ML', 'suco beterraba nordestao 500ml', 'Bebidas', 'un'),
    ('7898065902437', 'SUCO DETOX NORDESTÃO 500ML', 'suco detox nordestao 500ml', 'Bebidas', 'un'),
    ('7898065900617', 'SUCO DE LARANJA 300ML', 'suco de laranja 300ml', 'Bebidas', 'un'),
    ('7898065902438', 'SUCO DE LARANJA 900ML', 'suco de laranja 900ml', 'Bebidas', 'un'),
    ('7898065900662', 'PIZZA ASSADA CALABRESA FAB PROPRIA', 'pizza assada calabresa fab propria', 'Padaria', 'un'),
    ('7898065900655', 'PIZZA ASSADA FRANGO FAB PROPRIA', 'pizza assada frango fab propria', 'Padaria', 'un'),
    ('7898065900631', 'PIZZA ASSADA SERTANEJA FAB PROPRIA', 'pizza assada sertaneja fab propria', 'Padaria', 'un'),
    ('7898065900624', 'PIZZA ASSADA PRESUNTO FAB PROPRIA', 'pizza assada presunto fab propria', 'Padaria', 'un'),
    ('7898065900648', 'PIZZA ASSADA PRESUNTO/CALABRESA FAB PROPRIA', 'pizza assada presunto calabresa fab propria', 'Padaria', 'un'),
    ('7898065900679', 'PIZZA ASSADA MUSSARELA FAB PROPRIA', 'pizza assada mussarela fab propria', 'Padaria', 'un'),
    ('250682', 'PÃO CEIA FAB PROPRIA', 'pao ceia fab propria', 'Padaria', 'un'),
    ('7898065902154', 'SALGADO FOLHADO QUEIJO FAB PROPRIA', 'salgado folhado queijo fab propria', 'Padaria', 'un'),
    ('7898065902130', 'SALGADO FOLHADO FRANGO FAB PROPRIA', 'salgado folhado frango fab propria', 'Padaria', 'un'),
    ('7898065902147', 'SALGADO FOLHADO PRESUNTO/QUEIJO FAB PROPRIA', 'salgado folhado presunto queijo fab propria', 'Padaria', 'un'),
    ('7898065902161', 'SALGADO FOLHADO SALSICHA FAB PROPRIA', 'salgado folhado salsicha fab propria', 'Padaria', 'un'),
    ('251059', 'SALGADO COXINHA FRANGO UND. FAB PROPRIA', 'salgado coxinha frango und fab propria', 'Padaria', 'un'),
    ('253365', 'SALGADO COXINHA FRANGO/REQUEIJÃO FAB PROPRIA', 'salgado coxinha frango requeijao fab propria', 'Padaria', 'un'),
    ('253373', 'SALGADO CARNE/REQUEIJÃO FAB PROPRIA', 'salgado carne requeijao fab propria', 'Padaria', 'un'),
    ('000000202340', 'CESTA BASICA SOLAR ALTAVISTA', 'cesta basica solar altavista', 'Mercearia', 'un')
]

product_strings = []
for p in new_products:
    product_strings.append(f'            Product(code = "{p[0]}", name = "{p[1]}", searchName = "{p[2]}", category = "{p[3]}", unit = "{p[4]}", searchCount = 0)')

code_to_insert = ",\n".join(product_strings)

with open(file_path, "r") as f:
    content = f.read()

# Let's use a regex to match the last item in imageProductsToForceAdd to replace
target_pattern = r'(Product\(code = "256075", name = "Coxa e Sobrecoxa de Frango", searchName = "coxa sobrecoxa frango", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images\.unsplash\.com/photo-1598514982205-f36b96d1e8d4\?auto=format&fit=crop&w=150&q=80"\)\s+)\)'

replacement = f'\\1,\n{code_to_insert}\n        )'

if re.search(target_pattern, content):
    content = re.sub(target_pattern, replacement, content)
    with open(file_path, "w") as f:
        f.write(content)
    print("Successfully added new products.")
else:
    print("Target not found. Let's try another approach.")
