import re

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "r") as f:
    content = f.read()

replacement = """
    fun getProductsByCategory(category: String) = repository.getProductsByCategory(category)

    fun addProduct(name: String, code: String, category: String, unit: String) {"""

content = content.replace("    fun addProduct(name: String, code: String, category: String, unit: String) {", replacement)

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "w") as f:
    f.write(content)
