import re

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "r") as f:
    content = f.read()

replacement = """    fun getProductsByCategory(category: String) = repository.getProductsByCategory(category)

    fun updateProduct(product: Product) {
        viewModelScope.launch {
            repository.updateProduct(product)
        }
    }

    fun addProduct(name: String, code: String, category: String, unit: String) {"""

content = content.replace("    fun getProductsByCategory(category: String) = repository.getProductsByCategory(category)\n\n    fun addProduct(name: String, code: String, category: String, unit: String) {", replacement)

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "w") as f:
    f.write(content)
