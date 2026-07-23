import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

force_insert_code = """
        // Force add new products if they don't exist
        if (dao.getProductByCode("257806") == null) {
            dao.insertAll(listOf(Product(code = "257806", name = "Pão Baguete com Queijo", searchName = "pao baguete com queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80")))
        }
        if (dao.getProductByCode("257822") == null) {
            dao.insertAll(listOf(Product(code = "257822", name = "Pão Delícia Trançada Queijo", searchName = "pao delicia trancada queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80")))
        }
"""

content = content.replace("suspend fun populateInitialDataIfNeeded() {", "suspend fun populateInitialDataIfNeeded() {\n" + force_insert_code)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
