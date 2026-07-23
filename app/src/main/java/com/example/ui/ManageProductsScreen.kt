package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.data.Product

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ManageProductsScreen(viewModel: MainViewModel, onNavigateBack: () -> Unit) {
    val products by viewModel.allProducts.collectAsState()
    var showDialog by remember { mutableStateOf(false) }
    var editingProduct by remember { mutableStateOf<Product?>(null) }
    
    var name by remember { mutableStateOf("") }
    var code by remember { mutableStateOf("") }
    var category by remember { mutableStateOf("") }
    var imageUrl by remember { mutableStateOf("") }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Gerenciar Produtos") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Voltar")
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier.padding(innerPadding).fillMaxSize()
        ) {
            items(products) { product ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(product.name, style = MaterialTheme.typography.titleMedium)
                            Text("Código: ${product.code} | Categoria: ${product.category}", style = MaterialTheme.typography.bodySmall)
                        }
                        IconButton(onClick = {
                            name = product.name
                            code = product.code
                            category = product.category
                            imageUrl = product.imageUrl ?: ""
                            editingProduct = product
                            showDialog = true
                        }) {
                            Icon(Icons.Default.Edit, contentDescription = "Editar")
                        }
                    }
                }
            }
        }
        
        if (showDialog && editingProduct != null) {
            AlertDialog(
                onDismissRequest = { showDialog = false },
                title = { Text("Editar Produto") },
                text = {
                    Column {
                        OutlinedTextField(
                            value = name,
                            onValueChange = { name = it },
                            label = { Text("Nome do Produto") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        OutlinedTextField(
                            value = code,
                            onValueChange = { code = it },
                            label = { Text("Código") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        OutlinedTextField(
                            value = category,
                            onValueChange = { category = it },
                            label = { Text("Categoria") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        OutlinedTextField(
                            value = imageUrl,
                            onValueChange = { imageUrl = it },
                            label = { Text("URL da Imagem (Opcional)") },
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                },
                confirmButton = {
                    TextButton(onClick = {
                        if (name.isNotBlank() && code.isNotBlank()) {
                            viewModel.updateProduct(
                                editingProduct!!.copy(
                                    name = name,
                                    code = code,
                                    category = category,
                                    imageUrl = imageUrl.takeIf { it.isNotBlank() }
                                )
                            )
                            showDialog = false
                        }
                    }) {
                        Text("Salvar")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showDialog = false }) {
                        Text("Cancelar")
                    }
                }
            )
        }
    }
}
