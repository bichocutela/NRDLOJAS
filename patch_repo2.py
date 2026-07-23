import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

old_cat1 = "val category = product.category.lowercase()"
new_cat1 = "val category = product.category.unaccent().lowercase()"

content = content.replace(old_cat1, new_cat1)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
