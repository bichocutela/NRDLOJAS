import sys
with open("app/src/main/java/com/example/ui/ManageProductsScreen.kt", "r") as f:
    content = f.read()

if "import com.example.ui.theme.getDynamicThemeColor" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport com.example.ui.theme.getDynamicThemeColor")

# Add appTheme collection
content = content.replace('val products by viewModel.allProducts.collectAsStateWithLifecycle(initialValue = emptyList())', 'val products by viewModel.allProducts.collectAsStateWithLifecycle(initialValue = emptyList())\n    val appTheme by viewModel.userPreferences.appTheme.collectAsStateWithLifecycle(initialValue = "multicolor")')

# Convert items to itemsIndexed
target_list = """        LazyColumn(
            modifier = Modifier.padding(innerPadding).fillMaxSize()
        ) {
            items(products) { product ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
                ) {"""
replacement_list = """        LazyColumn(
            modifier = Modifier.padding(innerPadding).fillMaxSize()
        ) {
            itemsIndexed(products) { index, product ->
                val dynColors = getDynamicThemeColor(index, appTheme, MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.onPrimaryContainer)
                Card(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, dynColors.first)
                ) {"""
content = content.replace(target_list, replacement_list)

# also need to add itemsIndexed import
if "import androidx.compose.foundation.lazy.itemsIndexed" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.items", "import androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.lazy.itemsIndexed")

with open("app/src/main/java/com/example/ui/ManageProductsScreen.kt", "w") as f:
    f.write(content)
print("Success")
