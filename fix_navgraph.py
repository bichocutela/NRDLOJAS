import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.ui.draw.alpha
"""
content = content.replace("import androidx.compose.foundation.layout.*", imports + "import androidx.compose.foundation.layout.*")

# Update ModalDrawerSheet
content = content.replace("LoginDrawerContent(onLoginSuccess = {", "LoginDrawerContent(viewModel = viewModel, onLoginSuccess = {")

# Update LoginDrawerContent signature
content = content.replace("fun LoginDrawerContent(onLoginSuccess: () -> Unit) {", "fun LoginDrawerContent(viewModel: MainViewModel, onLoginSuccess: () -> Unit) {")

# Update Column modifier inside LoginDrawerContent
new_column = """    val categories by viewModel.productsCountByCategory.collectAsState()
    var expandedCategory by remember { mutableStateOf<String?>(null) }
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {"""
content = content.replace("""    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {""", new_column)

# Append new content at the bottom of LoginDrawerContent
new_categories = """        if (loginStatus != null) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = loginStatus!!,
                color = if (loginStatus == "Login com sucesso!") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
            )
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Categorias",
            style = MaterialTheme.typography.titleLarge,
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.align(Alignment.Start)
        )
        Spacer(modifier = Modifier.height(16.dp))
        
        categories.forEach { categoryCount ->
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
        }
    }
}

@Composable
fun CategoryItem(
    category: String,
    viewModel: MainViewModel,
    isExpanded: Boolean,
    onExpandToggle: () -> Unit
) {
    val productsFlow = remember(category) { viewModel.getProductsByCategory(category) }
    val products by if (isExpanded) productsFlow.collectAsState(initial = emptyList()) else remember { mutableStateOf(emptyList()) }
    
    Column(modifier = Modifier.fillMaxWidth()) {
        TextButton(
            onClick = onExpandToggle,
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(vertical = 12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(text = category, style = MaterialTheme.typography.titleMedium)
                Icon(
                    imageVector = if (isExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                    contentDescription = if (isExpanded) "Recolher" else "Expandir"
                )
            }
        }
        
        if (isExpanded) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(start = 16.dp, end = 16.dp, bottom = 8.dp)
            ) {
                if (products.isEmpty()) {
                    Text("Carregando...", style = MaterialTheme.typography.bodyMedium)
                } else {
                    products.forEach { product ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = product.name,
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.weight(1f)
                            )
                            Text(
                                text = product.code,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                        HorizontalDivider(modifier = Modifier.alpha(0.5f))
                    }
                }
            }
        }
    }
}
"""

content = re.sub(r'        if \(loginStatus != null\) \{.*?\n        \}\n    \}\n\}', new_categories, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
