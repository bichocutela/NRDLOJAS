import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

replacement = """                    onClick = {
                        val searchName = editName.lowercase().replace(Regex("[áàâã]"), "a").replace(Regex("[éèê]"), "e").replace(Regex("[íìî]"), "i").replace(Regex("[óòôõ]"), "o").replace(Regex("[úùû]"), "u").replace(Regex("[ç]"), "c")
                        viewModel.updateProduct(product.copy(code = editCode, name = editName, searchName = searchName))
                        isEditing = false
                    },"""

content = content.replace("""                    onClick = {
                        viewModel.updateProduct(product.copy(code = editCode, name = editName))
                        isEditing = false
                    },""", replacement)

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)
