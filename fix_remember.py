import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

replacement = """@Composable
fun AdminProductItem(product: Product, viewModel: MainViewModel) {
    var isEditing by remember { mutableStateOf(false) }
    var editCode by remember(product.code) { mutableStateOf(product.code) }
    var editName by remember(product.name) { mutableStateOf(product.name) }"""

content = content.replace("""@Composable
fun AdminProductItem(product: Product, viewModel: MainViewModel) {
    var isEditing by remember { mutableStateOf(false) }
    var editCode by remember { mutableStateOf(product.code) }
    var editName by remember { mutableStateOf(product.name) }""", replacement)

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)
