import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

old_search = """            products.filter { product ->
                val searchName = product.searchName
                val code = product.code
                
                if (code.contains(normalizedQuery)) return@filter true
                
                tokens.all { token ->
                    searchName.contains(token) || isTypoMatch(token, searchName)
                }
            }"""

new_search = """            products.filter { product ->
                val searchName = product.searchName
                val code = product.code
                val category = product.category.unaccent().lowercase()
                
                if (code.contains(normalizedQuery)) return@filter true
                
                tokens.all { token ->
                    searchName.contains(token) || isTypoMatch(token, searchName) || category.contains(token)
                }
            }"""

content = content.replace(old_search, new_search)

old_sync = """        return products.filter { product ->
            val searchName = product.searchName
            val code = product.code
            
            if (code.contains(normalizedQuery)) return@filter true
            
            tokens.all { token ->
                searchName.contains(token) || isTypoMatch(token, searchName)
            }
        }"""

new_sync = """        return products.filter { product ->
            val searchName = product.searchName
            val code = product.code
            val category = product.category.unaccent().lowercase()
            
            if (code.contains(normalizedQuery)) return@filter true
            
            tokens.all { token ->
                searchName.contains(token) || isTypoMatch(token, searchName) || category.contains(token)
            }
        }"""

content = content.replace(old_sync, new_sync)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
