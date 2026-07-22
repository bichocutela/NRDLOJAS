package com.example.ui

import android.graphics.Bitmap
import android.graphics.ImageDecoder
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.AddAPhoto
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import com.example.data.Product
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.BuildConfig
import com.example.api.*
import com.patrykandpatrick.vico.compose.axis.horizontal.rememberBottomAxis
import com.patrykandpatrick.vico.compose.axis.vertical.rememberStartAxis
import com.patrykandpatrick.vico.compose.chart.Chart
import com.patrykandpatrick.vico.compose.chart.column.columnChart
import com.patrykandpatrick.vico.core.entry.ChartEntryModelProducer
import com.patrykandpatrick.vico.core.entry.entryOf
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.putJsonObject
import kotlinx.serialization.json.put

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdminScreen(viewModel: MainViewModel, onNavigateBack: () -> Unit) {
    var showManualForm by remember { mutableStateOf(false) }
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    var selectedBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var isProcessing by remember { mutableStateOf(false) }
    
    var productName by remember { mutableStateOf("") }
    var productCode by remember { mutableStateOf("") }
    var productCategory by remember { mutableStateOf("") }
    var statusMessage by remember { mutableStateOf<String?>(null) }

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }
    
    val categoryCounts by viewModel.productsCountByCategory.collectAsStateWithLifecycle()
    val allProducts by viewModel.allProducts.collectAsStateWithLifecycle()
    val chartEntryModelProducer = remember { ChartEntryModelProducer() }
    
    LaunchedEffect(categoryCounts) {
        val entries = categoryCounts.mapIndexed { index, categoryCount ->
            entryOf(index.toFloat(), categoryCount.count.toFloat())
        }
        chartEntryModelProducer.setEntries(entries)
    }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri: Uri? ->
        uri?.let {
            selectedImageUri = it
            showManualForm = true // Show form to verify
            productName = ""
            productCode = ""
            productCategory = ""
            
            // Convert URI to Bitmap
            try {
                selectedBitmap = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                    val source = ImageDecoder.createSource(context.contentResolver, it)
                    ImageDecoder.decodeBitmap(source)
                } else {
                    MediaStore.Images.Media.getBitmap(context.contentResolver, it)
                }
                
                // Process image with Gemini
                scope.launch {
                    isProcessing = true
                    statusMessage = "A IA está analisando a imagem..."
                    
                    try {
                        val result = analyzeImage(selectedBitmap!!)
                        if (result != null) {
                            productName = result.name
                            productCode = result.code
                            productCategory = result.category
                            statusMessage = "Análise concluída. Verifique as informações."
                        } else {
                            statusMessage = "Erro na análise. Preencha manualmente."
                        }
                    } catch (e: Exception) {
                        statusMessage = "Erro: ${e.message}"
                    } finally {
                        isProcessing = false
                    }
                }
            } catch (e: Exception) {
                statusMessage = "Erro ao carregar a imagem."
            }
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            TopAppBar(
                title = { Text("Painel Administrativo") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (categoryCounts.isNotEmpty()) {
                Text(
                    text = "Dashboard de Inventário",
                    style = MaterialTheme.typography.titleLarge
                )
                Spacer(modifier = Modifier.height(16.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Produtos por Categoria",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Chart(
                            chart = columnChart(),
                            chartModelProducer = chartEntryModelProducer,
                            startAxis = rememberStartAxis(),
                            bottomAxis = rememberBottomAxis(valueFormatter = { value, _ ->
                                categoryCounts.getOrNull(value.toInt())?.category ?: ""
                            }),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(200.dp)
                        )
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = {
                        scope.launch {
                            val path = com.example.util.PdfExporter.exportProductsToPdf(context, allProducts)
                            if (path != null) {
                                snackbarHostState.showSnackbar("Inventário exportado para PDF: $path")
                            } else {
                                snackbarHostState.showSnackbar("Erro ao exportar PDF.")
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Default.Save, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Exportar Inventário (PDF)")
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
            
            Text(
                text = "Adicionar Novo Produto",
                style = MaterialTheme.typography.titleLarge
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Button(
                    onClick = {
                        launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                    }
                ) {
                    Icon(Icons.Default.AddAPhoto, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Por Foto (IA)")
                }
                
                Button(
                    onClick = {
                        selectedImageUri = null
                        selectedBitmap = null
                        productName = ""
                        productCode = ""
                        productCategory = ""
                        showManualForm = true
                        statusMessage = null
                    }
                ) {
                    Icon(Icons.Default.Edit, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Manualmente")
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            if (showManualForm) {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp)
                    ) {
                        if (selectedBitmap != null) {
                            Image(
                                bitmap = selectedBitmap!!.asImageBitmap(),
                                contentDescription = "Imagem do produto",
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(200.dp)
                                    .padding(bottom = 16.dp)
                            )
                        }
                        
                        if (isProcessing) {
                            CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally))
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        
                        OutlinedTextField(
                            value = productName,
                            onValueChange = { productName = it },
                            label = { Text("Nome do Produto") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        OutlinedTextField(
                            value = productCode,
                            onValueChange = { productCode = it },
                            label = { Text("Código EAN / Interno") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        OutlinedTextField(
                            value = productCategory,
                            onValueChange = { productCategory = it },
                            label = { Text("Categoria") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        Button(
                            onClick = {
                                if (productName.isNotBlank() && productCode.isNotBlank()) {
                                    viewModel.addProduct(
                                        name = productName,
                                        code = productCode,
                                        category = if (productCategory.isNotBlank()) productCategory else "Geral",
                                        unit = "un"
                                    )
                                    com.example.util.NotificationHelper.showNewProductNotification(context, productName)
                                    showManualForm = false
                                    scope.launch {
                                        snackbarHostState.showSnackbar("Produto adicionado com sucesso!")
                                    }
                                } else {
                                    scope.launch {
                                        snackbarHostState.showSnackbar("Preencha o nome e código.")
                                    }
                                }
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Icon(Icons.Default.Save, contentDescription = null)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("SALVAR PRODUTO")
                        }
                    }
                }
            }
            
            if (statusMessage != null) {
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

        }
    }
}

data class ProductAnalysisResult(val name: String, val code: String, val category: String)

suspend fun analyzeImage(bitmap: Bitmap): ProductAnalysisResult? = withContext(Dispatchers.IO) {
    try {
        val apiKey = BuildConfig.GEMINI_API_KEY
        val prompt = "Analise a imagem deste produto. Identifique o nome do produto, seu código (EAN ou número em destaque) e a categoria mais provável (ex: Açougue, Padaria, Hortifruti, Bebidas, etc). Retorne apenas um JSON com as chaves: 'nome', 'codigo', 'categoria'."
        
        val requestBody = GenerateContentRequest(
            contents = listOf(Content(
                parts = listOf(
                    Part(text = prompt),
                    Part(inlineData = InlineData(mimeType = "image/jpeg", data = bitmap.toBase64()))
                )
            )),
            generationConfig = GenerationConfig(
                responseFormat = ResponseFormat(
                    text = ResponseFormatText(
                        mimeType = "application/json",
                        schema = buildJsonObject {
                            put("type", "OBJECT")
                            putJsonObject("properties") {
                                putJsonObject("nome") {
                                    put("type", "STRING")
                                    put("description", "O nome do produto.")
                                }
                                putJsonObject("codigo") {
                                    put("type", "STRING")
                                    put("description", "O código EAN ou numérico do produto.")
                                }
                                putJsonObject("categoria") {
                                    put("type", "STRING")
                                    put("description", "A categoria do produto.")
                                }
                            }
                        }
                    )
                )
            )
        )
        
        val response = RetrofitClient.service.generateContent(apiKey, requestBody)
        val responseText = response.candidates.firstOrNull()?.content?.parts?.firstOrNull()?.text
        
        if (responseText != null) {
            val jsonResponse = Json.parseToJsonElement(responseText).jsonObject
            val name = jsonResponse["nome"]?.jsonPrimitive?.content ?: ""
            val code = jsonResponse["codigo"]?.jsonPrimitive?.content ?: ""
            val category = jsonResponse["categoria"]?.jsonPrimitive?.content ?: ""
            return@withContext ProductAnalysisResult(name, code, category)
        }
        null
    } catch (e: Exception) {
        e.printStackTrace()
        null
    }
}

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
    var editCode by remember(product.code) { mutableStateOf(product.code) }
    var editName by remember(product.name) { mutableStateOf(product.name) }
    
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
                        val searchName = editName.lowercase().replace(Regex("[áàâã]"), "a").replace(Regex("[éèê]"), "e").replace(Regex("[íìî]"), "i").replace(Regex("[óòôõ]"), "o").replace(Regex("[úùû]"), "u").replace(Regex("[ç]"), "c")
                        viewModel.updateProduct(product.copy(code = editCode, name = editName, searchName = searchName))
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
