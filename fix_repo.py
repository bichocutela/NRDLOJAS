import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

replacement = """    suspend fun insertProduct(product: Product) {
        dao.insertProduct(product)
    }

    suspend fun updateProduct(product: Product) {
        dao.updateProduct(product)
    }"""

content = content.replace("    suspend fun insertProduct(product: Product) {\n        dao.insertProduct(product)\n    }", replacement)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
