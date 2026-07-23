import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

new_products = """
                Product(code = "257806", name = "Pão Baguete com Queijo", searchName = "pao baguete com queijo", category = "Padaria", unit = "un", searchCount = 0),
                Product(code = "257822", name = "Pão Delícia Trançada Queijo", searchName = "pao delicia trancada queijo", category = "Padaria", unit = "un", searchCount = 0),
"""

# Insert before // Produtos da imagem
content = content.replace("// Produtos da imagem", new_products + "                // Produtos da imagem")

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
