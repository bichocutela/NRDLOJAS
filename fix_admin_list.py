import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import com.example.data.Product
"""
content = content.replace("import com.example.data.Product", "") # remove if exists
content = content.replace("import androidx.compose.material.icons.filled.Edit", imports + "import androidx.compose.material.icons.filled.Edit")

# Inject list below status message
list_injection = """            if (statusMessage != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = statusMessage!!,
                    color = MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(16.dp))
            AdminProductList(allProducts, viewModel)
"""
content = content.replace("            if (statusMessage != null) {\n                Spacer(modifier = Modifier.height(16.dp))\n                Text(\n                    text = statusMessage!!,\n                    color = MaterialTheme.colorScheme.primary,\n                    style = MaterialTheme.typography.bodyMedium\n                )\n            }", list_injection)

# Add Composables
composables = """
@Composable
fun AdminProductList(products: List<Product>, viewModel: MainViewModel) {
    var searchQuery by remember { mutableStateOf("") }
    
    Text("Gerenciar Produtos", style = MaterialTheme.typography.titleLarge)
    Spacer(modifier = Modifier.height(16.dp))
    
    OutlinedTextField(
        value = searchQuery,
        onValueChange = { searchQuery = it },
        label = { Text("Pesquisar produto ou categoria") },
        modifier = Modifier.fillMaxWidth(),
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Pesquisar") }
    )
    
    Spacer(modifier = Modifier.height(16.dp))
    
    val filteredProducts = products.filter {
        it.name.contains(searchQuery, ignoreCase = true) ||
        it.category.contains(searchQuery, ignoreCase = true) ||
        it.code.contains(searchQuery, ignoreCase = true)
    }
    
    val groupedProducts = filteredProducts.groupBy { it.category }
    
    groupedProducts.forEach { (category, categoryProducts) ->
        Text(
            text = category,
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(vertical = 8.dp)
        )
        categoryProducts.forEach { product ->
            AdminProductItem(product, viewModel)
        }
    }
}

@Composable
fun AdminProductItem(product: Product, viewModel: MainViewModel) {
    var isEditing by remember { mutableStateOf(false) }
    var editCode by remember { mutableStateOf(product.code) }
    var editName by remember { mutableStateOf(product.name) }
    
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(text = product.name, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f))
                IconButton(onClick = { isEditing = !isEditing }) {
                    Icon(if (isEditing) Icons.Default.Close else Icons.Default.Edit, contentDescription = "Editar")
                }
            }
            if (isEditing) {
                OutlinedTextField(
                    value = editName,
                    onValueChange = { editName = it },
                    label = { Text("Nome do Produto") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = editCode,
                    onValueChange = { editCode = it },
                    label = { Text("Novo Código") },
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
                Spacer(modifier = Modifier.height(8.dp))
                Button(
                    onClick = {
                        viewModel.updateProduct(product.copy(code = editCode, name = editName))
                        isEditing = false
                    },
                    modifier = Modifier.align(Alignment.End)
                ) {
                    Text("Salvar")
                }
            } else {
                Text(text = "Código: ${product.code}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.secondary)
            }
        }
    }
}
"""

content += composables

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)
