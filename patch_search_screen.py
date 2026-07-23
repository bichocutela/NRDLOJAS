import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# 1. Imports
if "import androidx.compose.material3.AlertDialog" not in content:
    content = content.replace("import androidx.compose.material3.BadgedBox", "import androidx.compose.material3.BadgedBox\nimport androidx.compose.material3.AlertDialog\nimport androidx.compose.material3.TextButton\nimport androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.remember\nimport androidx.compose.runtime.setValue")

# 2. Search Bar changes
search_bar_old = """        // Custom Search Bar
        Row(
            modifier = Modifier.padding(horizontal = 16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            SearchBar(
                query = searchQuery,
                onQueryChange = viewModel::updateSearchQuery,
                onSearch = { },
                active = false,
                onActiveChange = { },
                placeholder = { Text("Nome...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Pesquisar") },
                trailingIcon = {
                    Row {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { viewModel.updateSearchQuery("") }) {
                                Icon(Icons.Default.Clear, contentDescription = "Limpar")
                            }
                        } else {
                            IconButton(onClick = { /* TODO Voice Search */ }) {
                                Icon(Icons.Default.Mic, contentDescription = "Voz", tint = MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                },
                modifier = Modifier
                    .weight(1f)
                    .background(Color.White, RoundedCornerShape(24.dp))
                    .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(24.dp)),
                colors = SearchBarDefaults.colors(
                    containerColor = Color.Transparent,
                    dividerColor = Color.Transparent,
                )
            ) {}
            
            Spacer(modifier = Modifier.width(8.dp))
            
            Button(
                onClick = { /* Do search */ },
                shape = RoundedCornerShape(24.dp), // Estilo balão
                modifier = Modifier.height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Text("PESQUISAR", fontWeight = FontWeight.Bold, fontSize = 12.sp)
            }
        }"""

search_bar_new = """        // Custom Search Bar
        Column(
            modifier = Modifier.padding(horizontal = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            SearchBar(
                query = searchQuery,
                onQueryChange = viewModel::updateSearchQuery,
                onSearch = { },
                active = false,
                onActiveChange = { },
                placeholder = { Text("Pesquisar produto...", style = MaterialTheme.typography.bodyLarge) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Pesquisar", modifier = Modifier.size(28.dp)) },
                trailingIcon = {
                    Row {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { viewModel.updateSearchQuery("") }) {
                                Icon(Icons.Default.Clear, contentDescription = "Limpar")
                            }
                        } else {
                            IconButton(onClick = { /* TODO Voice Search */ }) {
                                Icon(Icons.Default.Mic, contentDescription = "Voz", tint = MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White, RoundedCornerShape(32.dp))
                    .border(2.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(32.dp)),
                colors = SearchBarDefaults.colors(
                    containerColor = Color.Transparent,
                    dividerColor = Color.Transparent,
                )
            ) {}
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = { /* Do search */ },
                shape = RoundedCornerShape(32.dp), // Estilo balão gigante
                modifier = Modifier.fillMaxWidth().height(64.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Text("PESQUISAR PRODUTO", fontWeight = FontWeight.Black, fontSize = 18.sp, letterSpacing = 1.sp)
            }
        }"""

content = content.replace(search_bar_old, search_bar_new)

# 3. CategorySection signature and call
content = content.replace("CategorySection()", "CategorySection(viewModel)")
content = content.replace("fun CategorySection()", "fun CategorySection(viewModel: MainViewModel)")
content = content.replace(".clickable { /* Filter by category */ }", ".clickable { viewModel.updateSearchQuery(category) }")

# 4. HistoryItem Dialog
history_old = """fun HistoryItem(product: Product, viewModel: MainViewModel) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.5f))
            .border(1.dp, MaterialTheme.colorScheme.primaryContainer, RoundedCornerShape(16.dp))
            .clickable { viewModel.onProductSearched(product) }"""

history_new = """fun HistoryItem(product: Product, viewModel: MainViewModel) {
    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            confirmButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("FECHAR", color = MaterialTheme.colorScheme.primary)
                }
            },
            title = {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black)
                )
            },
            text = {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = product.code,
                        style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Código de barras / Referência",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            },
            shape = RoundedCornerShape(32.dp),
            containerColor = Color.White
        )
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.5f))
            .border(1.dp, MaterialTheme.colorScheme.primaryContainer, RoundedCornerShape(16.dp))
            .clickable { showDialog = true }"""

content = content.replace(history_old, history_new)


with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)

