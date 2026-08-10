package com.example.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.BuildConfig
import com.example.api.Content
import com.example.api.GenerateContentRequest
import com.example.api.Part
import com.example.api.RetrofitClient
import com.example.data.Product
import com.example.data.ProductRepository
import com.example.data.UserPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class MainViewModel(private val repository: ProductRepository, val userPreferences: UserPreferences) : ViewModel() {
    val authRepository = com.example.data.AuthRepository()


    private val _latestProduct = MutableStateFlow<Map<String, Any>?>(null)
    val latestProduct = _latestProduct.asStateFlow()
    init {
        viewModelScope.launch {
            com.example.data.FirebaseService.observeDynamicTabs().collect { remoteTabs ->
                val localTabs = repository.getAllTabs().first()
                remoteTabs.forEach { remoteTab ->
                    val localTab = localTabs.find { it.id == remoteTab.id }
                    if (localTab != remoteTab) {
                        repository.insertTab(remoteTab)
                    }
                }
                val remoteIds = remoteTabs.map { it.id }.toSet()
                val tabsToDelete = localTabs.filter { it.id !in remoteIds }
                if (tabsToDelete.isNotEmpty() && !isSyncingTabs) {
                    tabsToDelete.forEach { repository.deleteTab(it) }
                }
            }
        }
        viewModelScope.launch {
            com.example.data.FirebaseService.observeBannerUrl().collect { url ->
                if (url != null) {
                    userPreferences.setBannerImageUri(url)
                }
            }
        }
        viewModelScope.launch {
            com.example.data.FirebaseService.observeLatestProduct().collect {
                _latestProduct.value = it
            }
        }
        viewModelScope.launch {
            com.example.data.FirebaseService.observeProducts().collect { remoteProducts ->
                if (remoteProducts.isNotEmpty()) {
                    val localProducts = repository.getAllProductsSync()
                    val remoteIds = remoteProducts.map { it.code }.toSet()
                    val toDelete = localProducts.filter { it.code !in remoteIds }
                    
                    if (toDelete.isNotEmpty() && !_isSyncing.value) {
                        repository.deleteProducts(toDelete)
                    }
                    
                    val missingOrUpdated = remoteProducts.filter { remote ->
                        val local = localProducts.find { it.code == remote.code }
                        local == null || local.name != remote.name || local.imageUrl != remote.imageUrl || local.category != remote.category || local.unit != remote.unit
                    }
                    if (missingOrUpdated.isNotEmpty() && !_isSyncing.value) {
                        repository.insertProducts(missingOrUpdated)
                    }
                }
            }
        }
        viewModelScope.launch {
            repository.populateInitialDataIfNeeded()
            syncProductsFromFirebase()
            
            val existing = repository.searchProductsSync("256075")
            if (existing.isEmpty()) {
                val newProducts = listOf(
                    com.example.data.Product(code = "256075", name = "Coxa/Sobrecoxa de Frango Resfriada", searchName = "coxa sobrecoxa de frango resfriada", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254297", name = "Sobrecoxa de Frango S/ Pele", searchName = "sobrecoxa de frango sem pele", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254307", name = "Coração de Frango Bom Todo", searchName = "coracao de frango bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1590080874088-eec64895e423?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "256088", name = "Pé de Frango Resfriado", searchName = "pe de frango resfriado", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254304", name = "Filé de Peito Bom Todo", searchName = "file de peito bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254331", name = "Coxa de Frango Resfriada", searchName = "coxa de frango resfriada", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254306", name = "Moela de Frango Bom Todo", searchName = "moela de frango bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254308", name = "Filé de Sobrecoxa Bom Todo", searchName = "file de sobrecoxa bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254293", name = "Coxinha da Asa Bom Todo", searchName = "coxinha da asa bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254333", name = "Sobrecoxa de Frango Bom Todo", searchName = "sobrecoxa de frango bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "256087", name = "Fígado de Frango Resfriado", searchName = "figado de frango resfriado", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1590080874088-eec64895e423?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254311", name = "Asa de Frango Bom Todo", searchName = "asa de frango bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                    com.example.data.Product(code = "254305", name = "Meio da Asa Bom Todo", searchName = "meio da asa bom todo", category = "Açougue", unit = "kg", imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80")
                )
                repository.insertProducts(newProducts)
                if (com.example.data.FirebaseService.isFirebaseConfigured()) {
                    newProducts.forEach { product ->
                        com.example.data.FirebaseService.saveProduct(product)
                    }
                    com.example.data.FirebaseService.publishProductEvent("NEW_PRODUCT", newProducts.last().name, null, newProducts.last().code)
                }
            }
        }
    }

    private val _searchQuery = MutableStateFlow("")
    val searchQuery = _searchQuery.asStateFlow()

    private val _chatInput = MutableStateFlow("")
    val chatInput = _chatInput.asStateFlow()

    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages = _chatMessages.asStateFlow()

    private val _aiProductDetails = MutableStateFlow<String?>(null)
    val aiProductDetails = _aiProductDetails.asStateFlow()

    private val _isAiLoading = MutableStateFlow(false)
    val isAiLoading = _isAiLoading.asStateFlow()


    private val _newProductsCount = MutableStateFlow(0)
    val newProductsCount: StateFlow<Int> = _newProductsCount.asStateFlow()

    val favorites = repository.favorites.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val mostUsed = repository.mostUsed.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val history = repository.history.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val allProducts = repository.allProducts.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val productsCountByCategory = repository.productsCountByCategory.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val latestProductLocal = repository.latestProductLocal.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
    
    val searchResults: StateFlow<List<Product>> = _searchQuery
        .debounce(300)
        .flatMapLatest { query ->
            if (query.isBlank()) {
                flowOf(emptyList())
            } else {
                repository.searchProducts(query)
            }
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun updateSearchQuery(query: String) {
        _searchQuery.value = query
    }

    fun onProductSearched(product: Product) {
        viewModelScope.launch {
            repository.registerSearch(product)
        }
    }

    fun toggleFavorite(product: Product) {
        viewModelScope.launch {
            repository.toggleFavorite(product)
        }
    }

    fun updateChatInput(input: String) {
        _chatInput.value = input
    }


    fun consultProductInfoAi(product: Product) {
        viewModelScope.launch {
            _isAiLoading.value = true
            _aiProductDetails.value = null
            try {
                val prompt = "Forneça informações detalhadas sobre o produto de supermercado: ${product.name} (Categoria: ${product.category}). Inclua dicas de uso, armazenamento ou curiosidades. Seja breve e informativo."
                val request = GenerateContentRequest(
                    contents = listOf(Content(parts = listOf(Part(text = prompt))))
                )
                val response = RetrofitClient.service.generateContent(BuildConfig.GEMINI_API_KEY, request)
                _aiProductDetails.value = response.candidates?.firstOrNull()?.content?.parts?.firstOrNull()?.text ?: "Informações não disponíveis."
            } catch (e: Throwable) {
                _aiProductDetails.value = "Erro ao buscar informações: ${e.message}"
            } finally {
                _isAiLoading.value = false
            }
        }
    }
    
    fun clearAiProductDetails() {
        _aiProductDetails.value = null
    }

    fun sendChatMessage() {
        val query = _chatInput.value
        if (query.isBlank()) return

        _chatInput.value = ""
        val newMessages = _chatMessages.value.toMutableList()
        newMessages.add(ChatMessage(query, true))
        _chatMessages.value = newMessages

        viewModelScope.launch {
            try {
                val allProducts = repository.searchProductsSync("")
                
                val contextString = allProducts.joinToString("\n") { 
                    "${it.name} (${it.category}) - Código: ${it.code} - Vendido por: ${it.unit}"
                }

                val systemPrompt = """
                    Você é um assistente de um supermercado para ajudar operadores de caixa e repositores a encontrar códigos de produtos.
                    Sempre responda de forma amigável, direta e curta.
                    Quando o usuário perguntar sobre um produto, forneça o código dele usando a lista abaixo.
                    Se o produto não estiver na lista, diga que não encontrou.
                    
                    Lista de produtos:
                    $contextString
                """.trimIndent()

                val request = GenerateContentRequest(
                    contents = listOf(Content(parts = listOf(Part(text = query)))),
                    systemInstruction = Content(parts = listOf(Part(text = systemPrompt)))
                )
                
                val response = RetrofitClient.service.generateContent(BuildConfig.GEMINI_API_KEY, request)
                val responseText = response.candidates?.firstOrNull()?.content?.parts?.firstOrNull()?.text ?: "Desculpe, não entendi."
                
                val updatedMessages = _chatMessages.value.toMutableList()
                updatedMessages.add(ChatMessage(responseText, false))
                _chatMessages.value = updatedMessages

            } catch (e: Throwable) {
                val updatedMessages = _chatMessages.value.toMutableList()
                updatedMessages.add(ChatMessage("Erro ao conectar com a IA: ${e.message}", false))
                _chatMessages.value = updatedMessages
            }
        }
    }

    fun getProductsByCategory(category: String) = repository.getProductsByCategory(category)

    suspend fun updateProductSuspend(oldProduct: Product, newProduct: Product): Boolean {
        var finalProduct = newProduct
        finalProduct = finalProduct.copy(id = oldProduct.id)
        
        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            if (oldProduct.code != newProduct.code) {
                android.util.Log.d("ProductSync", "Verificando se o novo código já existe: ${newProduct.code}")
                val exists = com.example.data.FirebaseService.productExists(newProduct.code)
                if (exists) {
                    android.util.Log.e("ProductSync", "Código já existe: ${newProduct.code}")
                    _syncMessage.emit("Já existe outro produto com esse código.")
                    return false
                }
            }
        }

        if (newProduct.imageUrl?.startsWith("content://") == true) {
            android.util.Log.d("ProductSync", "Iniciando upload de imagem para alteração: ${newProduct.code}")
            val uri = android.net.Uri.parse(newProduct.imageUrl)
            val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${newProduct.code}_${System.currentTimeMillis()}.jpg")
            if (url != null) {
                android.util.Log.d("ProductSync", "Upload sucesso: $url")
                finalProduct = finalProduct.copy(imageUrl = url)
            } else {
                android.util.Log.e("ProductSync", "Upload falhou para: ${newProduct.code}")
                _syncMessage.emit("Não foi possível enviar a foto. Tente novamente.")
                return false
            }
        }

        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            android.util.Log.d("ProductSync", "Iniciando save Firestore para edição: ${finalProduct.code}")
            val saveSuccess = com.example.data.FirebaseService.saveProduct(finalProduct)
            if (saveSuccess) {
                if (oldProduct.code != finalProduct.code) {
                    android.util.Log.d("ProductSync", "Código alterado de ${oldProduct.code} para ${finalProduct.code}. Excluindo antigo.")
                    val deleteSuccess = com.example.data.FirebaseService.deleteProduct(oldProduct.code)
                    if (!deleteSuccess) {
                        android.util.Log.e("ProductSync", "Erro ao excluir documento antigo: ${oldProduct.code}. Iniciando rollback.")
                        val rollbackSuccess = com.example.data.FirebaseService.deleteProduct(finalProduct.code)
                        if (rollbackSuccess) {
                            android.util.Log.e("ProductSync", "Rollback com sucesso para: ${finalProduct.code}")
                            _syncMessage.emit("Não foi possível alterar o código. Tente novamente.")
                        } else {
                            android.util.Log.e("ProductSync", "Erro crítico: rollback falhou para: ${finalProduct.code}")
                            _syncMessage.emit("Erro ao concluir a alteração do código. Tente novamente.")
                        }
                        return false
                    }
                }
                
                android.util.Log.d("ProductSync", "Atualizando Room: ${finalProduct.code}")
                repository.updateProduct(finalProduct)
                
                val type = when {
                    oldProduct.code != finalProduct.code && oldProduct.name != finalProduct.name -> "INFO_CHANGED"
                    oldProduct.code != finalProduct.code -> "CODE_CHANGED"
                    oldProduct.name != finalProduct.name -> "NAME_CHANGED"
                    else -> "INFO_CHANGED" // Fallback se não for CODE_CHANGED nem NAME_CHANGED
                }
                // Ajustar fallback para ser mais exato ou não? O código antigo enviava INFO_CHANGED se ==, let's keep it.
                // Na vdd a instrução diz "Se alterar apenas nome -> NAME_CHANGED, se código -> CODE_CHANGED, etc."
                // Se alterar ambos -> INFO_CHANGED.
                
                android.util.Log.d("ProductSync", "Publicando evento: $type")
                com.example.data.FirebaseService.publishProductEvent(type, finalProduct.name, oldProduct.name, finalProduct.code)
                _syncMessage.emit("Produto atualizado na nuvem!")
                return true
            } else {
                android.util.Log.e("ProductSync", "Save Firestore falhou para edição: ${finalProduct.code}")
                _syncMessage.emit("Erro ao atualizar produto na nuvem.")
                return false
            }
        } else {
            repository.updateProduct(finalProduct)
            _syncMessage.emit("Atualizado apenas localmente")
            return true
        }
    }
    suspend fun removeProductImage(product: Product): Boolean {
        val updatedProduct = product.copy(imageUrl = null)
        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            val success = com.example.data.FirebaseService.saveProduct(updatedProduct)
            if (success) {
                repository.updateProduct(updatedProduct)
                com.example.data.FirebaseService.publishProductEvent("INFO_CHANGED", updatedProduct.name, product.name, updatedProduct.code)
                _syncMessage.emit("Foto removida com sucesso.")
                return true
            } else {
                _syncMessage.emit("Não foi possível remover a foto.")
                return false
            }
        } else {
            _syncMessage.emit("Não foi possível remover a foto. Verifique a conexão e tente novamente.")
            return false
        }
    }

    suspend fun deleteProductSuspend(product: Product): Boolean {
        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            val success = com.example.data.FirebaseService.deleteProduct(product.code)
            if (success) {
                repository.deleteProduct(product)
                _syncMessage.emit("Produto excluído com sucesso.")
                return true
            } else {
                _syncMessage.emit("Não foi possível excluir o produto. Tente novamente.")
                return false
            }
        } else {
            _syncMessage.emit("Não foi possível excluir o produto. Verifique a conexão e tente novamente.")
            return false
        }
    }

    fun updateProduct(oldProduct: Product, newProduct: Product) {
        viewModelScope.launch {
            updateProductSuspend(oldProduct, newProduct)
        }
    }


    private val _syncMessage = MutableSharedFlow<String>()
    val syncMessage = _syncMessage.asSharedFlow()

        suspend fun addProductSuspend(name: String, code: String, category: String, unit: String, imageUrl: String? = null): Boolean {
        var finalImageUrl = imageUrl
        if (imageUrl?.startsWith("content://") == true) {
            android.util.Log.d("ProductSync", "Iniciando upload de imagem para $code")
            val uri = android.net.Uri.parse(imageUrl)
            val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${code}_${System.currentTimeMillis()}.jpg")
            if (url != null) {
                android.util.Log.d("ProductSync", "Upload sucesso: $url")
                finalImageUrl = url
            } else {
                android.util.Log.e("ProductSync", "Upload falhou para $code")
                _syncMessage.emit("Não foi possível enviar a foto. Tente novamente.")
                return false
            }
        }
        val product = Product(
            code = code,
            name = name,
            searchName = name.lowercase().replace(Regex("[áàâã]"), "a").replace(Regex("[éèê]"), "e").replace(Regex("[íìî]"), "i").replace(Regex("[óòôõ]"), "o").replace(Regex("[úùû]"), "u").replace(Regex("[ç]"), "c"),
            category = category,
            unit = unit,
            imageUrl = finalImageUrl
        )
        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            android.util.Log.d("ProductSync", "Iniciando save Firestore para novo produto: $code")
            val success = com.example.data.FirebaseService.saveProduct(product)
            if (success) {
                android.util.Log.d("ProductSync", "Save Firestore sucesso, atualizando Room: $code")
                repository.insertProduct(product)
                com.example.data.FirebaseService.publishProductEvent("NEW_PRODUCT", product.name, null, product.code)
                _syncMessage.emit("Produto adicionado na nuvem!")
                _newProductsCount.value += 1
                return true
            } else {
                android.util.Log.e("ProductSync", "Save Firestore falhou para: $code")
                _syncMessage.emit("Erro ao salvar produto na nuvem.")
                return false
            }
        } else {
            _syncMessage.emit("Não foi possível publicar o produto. Verifique a conexão e tente novamente.")
            return false
        }
    }
    
    fun addProduct(name: String, code: String, category: String, unit: String, imageUrl: String? = null) {
        viewModelScope.launch {
            addProductSuspend(name, code, category, unit, imageUrl)
        }
    }
    private val _isSyncing = MutableStateFlow(false)
    val isSyncing = _isSyncing.asStateFlow()
    
    fun syncProductsFromFirebase() {
        viewModelScope.launch {
            _isSyncing.value = true
            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {
                val msg = com.example.data.FirebaseService.lastError ?: "Configuração ausente."
                _syncMessage.emit("Nuvem não configurada: $msg")
                _isSyncing.value = false
                return@launch
            }
            try {
                val remoteProducts = com.example.data.FirebaseService.getAllProducts()
                if (remoteProducts.isNotEmpty()) {
                    val localProducts = repository.getAllProductsSync()
                    val remoteIds = remoteProducts.map { it.code }.toSet()
                    val toDelete = localProducts.filter { it.code !in remoteIds }
                    
                    if (toDelete.isNotEmpty()) {
                        repository.deleteProducts(toDelete)
                    }
                    
                    val missingOrUpdated = remoteProducts.filter { remote ->
                        val local = localProducts.find { it.code == remote.code }
                        local == null || local.name != remote.name || local.imageUrl != remote.imageUrl || local.category != remote.category || local.unit != remote.unit
                    }
                    if (missingOrUpdated.isNotEmpty()) {
                        repository.insertProducts(missingOrUpdated)
                    }
                }
            } catch (e: Exception) {
                // Ignore
            } finally {
                _isSyncing.value = false
            }
        }
    }

    fun clearNewProductsCount() {
        _newProductsCount.value = 0
    }
    val dynamicTabs: kotlinx.coroutines.flow.StateFlow<List<com.example.data.DynamicTab>> = repository.getAllTabs()
        .stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.WhileSubscribed(5000), emptyList())


    private var isSyncingTabs = false

    fun insertTab(tab: com.example.data.DynamicTab) = viewModelScope.launch {
        isSyncingTabs = true
        val existingIds = repository.getAllTabs().first().map { it.id }.toSet()
        repository.insertTab(tab)
        val tabs = repository.getAllTabs().first { list -> list.any { it.id !in existingIds } }
        com.example.data.FirebaseService.syncAllDynamicTabs(tabs)
        isSyncingTabs = false
    }

    fun updateTab(tab: com.example.data.DynamicTab) = viewModelScope.launch {
        isSyncingTabs = true
        repository.updateTab(tab)
        val tabs = repository.getAllTabs().first { list -> list.any { it == tab } }
        com.example.data.FirebaseService.syncAllDynamicTabs(tabs)
        isSyncingTabs = false
    }

    fun deleteProduct(product: Product) {
        viewModelScope.launch {
            repository.deleteProduct(product)
            if (com.example.data.FirebaseService.isFirebaseConfigured()) {
                com.example.data.FirebaseService.deleteProduct(product.code)
                _syncMessage.emit("Produto excluído na nuvem!")
            }
        }
    }

    fun deleteTab(tab: com.example.data.DynamicTab) = viewModelScope.launch {
        isSyncingTabs = true
        repository.deleteTab(tab)
        com.example.data.FirebaseService.deleteDynamicTab(tab)
        isSyncingTabs = false
    }


    fun setOnboardingShown() {
        viewModelScope.launch {
            userPreferences.setOnboardingShown(true)
        }
    }
}

data class ChatMessage(val text: String, val isUser: Boolean)
