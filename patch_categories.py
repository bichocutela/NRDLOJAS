import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """        categories.forEach { categoryCount ->
            CategoryItem(
                category = categoryCount.category,
                viewModel = viewModel,
                isExpanded = expandedCategory == categoryCount.category,
                onExpandToggle = {
                    if (expandedCategory == categoryCount.category) {
                        expandedCategory = null
                    } else {
                        expandedCategory = categoryCount.category
                    }
                }
            )
        }"""

replacement = """        val allCategoriesList = remember(categories) {
            val defaultCategories = listOf("Hortifruti", "Açougue", "Padaria", "Frios", "Bebidas", "Mercearia", "Limpeza", "Higiene", "Laticínios", "Congelados", "Bazar", "Pet Shop")
            val dbCategories = categories.map { it.category }
            (dbCategories + defaultCategories).distinct().sorted()
        }

        allCategoriesList.forEach { categoryName ->
            CategoryItem(
                category = categoryName,
                viewModel = viewModel,
                isExpanded = expandedCategory == categoryName,
                onExpandToggle = {
                    if (expandedCategory == categoryName) {
                        expandedCategory = null
                    } else {
                        expandedCategory = categoryName
                    }
                }
            )
        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)

