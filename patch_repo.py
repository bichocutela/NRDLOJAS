import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

# Replace search logic to include category
old_search = """                val searchName = product.searchName
                val code = product.code
                
                // All tokens must match either searchName or code
                tokens.all { token ->
                    searchName.contains(token) || code.contains(token)
                }"""

new_search = """                val searchName = product.searchName
                val code = product.code
                val category = product.category.lowercase()
                
                // All tokens must match either searchName, code or category
                tokens.all { token ->
                    searchName.contains(token) || code.contains(token) || category.contains(token)
                }"""

content = content.replace(old_search, new_search)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
