import re

content = open("app/src/main/java/com/example/ui/AdminScreen.kt").read()

# For addProductSuspend
add_pattern = r"""(isAdding = true\s*viewModel\.addProductSuspend\([\s\S]*?\)\s*)showManualForm = false\s*isAdding = false\s*snackbarHostState\.showSnackbar\("Produto adicionado com sucesso!"\)"""

add_repl = """isAdding = true
                                val success = viewModel.addProductSuspend(
                                    name = productName,
                                    code = productCode,
                                    category = if (productCategory.isNotBlank()) productCategory else "Geral",
                                    unit = "un",
                                    imageUrl = productImageUrl.ifBlank { null }?.let { com.example.util.ImageUrlHelper.normalizeUrl(it) }
                                )
                                isAdding = false
                                if (success) {
                                    showManualForm = false
                                    snackbarHostState.showSnackbar("Produto adicionado com sucesso!")
                                }"""

# We need to correctly match and replace
# It's better to just do exact string replacement for the blocks

content = re.sub(
    r'isAdding = true\s*viewModel\.addProductSuspend\(\s*name = productName,\s*code = productCode,\s*category = if \(productCategory\.isNotBlank\(\)\) productCategory else "Geral",\s*unit = "un",\s*imageUrl = productImageUrl\.ifBlank \{ null \}\?\.let \{ com\.example\.util\.ImageUrlHelper\.normalizeUrl\(it\) \}\s*\)\s*showManualForm = false\s*isAdding = false\s*snackbarHostState\.showSnackbar\("Produto adicionado com sucesso!"\)',
    add_repl,
    content
)

update_pattern = r'viewModel\.updateProductSuspend\(product, newProduct\)\s*isSaving = false\s*isEditing = false'
update_repl = 'val success = viewModel.updateProductSuspend(product, newProduct)\n                            isSaving = false\n                            if (success) {\n                                isEditing = false\n                            }'

content = re.sub(update_pattern, update_repl, content)

open("app/src/main/java/com/example/ui/AdminScreen.kt", "w").write(content)
print("Success")
