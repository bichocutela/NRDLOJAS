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
import kotlinx.coroutines.launch

class MainViewModel(private val repository: ProductRepository, val userPreferences: UserPreferences) : ViewModel() {
    val authRepository = com.example.data.AuthRepository()


    private val _latestProduct = MutableStateFlow<Map<String, Any>?>(null)
    val latestProduct = _latestProduct.asStateFlow()
    init {
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
                if (it != null) {
                    syncProductsFromFirebase()
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
                    com.example.data.FirebaseService.publishLatestProduct(newProducts.last())
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
            } catch (e: Exception) {
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

            } catch (e: Exception) {
                val updatedMessages = _chatMessages.value.toMutableList()
                updatedMessages.add(ChatMessage("Erro ao conectar com a IA: ${e.message}", false))
                _chatMessages.value = updatedMessages
            }
        }
    }

    fun getProductsByCategory(category: String) = repository.getProductsByCategory(category)

    fun updateProduct(product: Product) {
        viewModelScope.launch {
            repository.updateProduct(product)
        }
    }

    private val _syncMessage = MutableSharedFlow<String>()
    val syncMessage = _syncMessage.asSharedFlow()

    fun addProduct(name: String, code: String, category: String, unit: String) {
        viewModelScope.launch {
            val product = Product(
                code = code,
                name = name,
                searchName = name.lowercase().replace(Regex("[áàâã]"), "a").replace(Regex("[éèê]"), "e").replace(Regex("[íìî]"), "i").replace(Regex("[óòôõ]"), "o").replace(Regex("[úùû]"), "u").replace(Regex("[ç]"), "c"),
                category = category,
                unit = unit
            )
            repository.insertProduct(product)
            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {
                _syncMessage.emit("Salvo apenas localmente (Nuvem não configurada)")
            } else {
                com.example.data.FirebaseService.saveProduct(product)
                com.example.data.FirebaseService.publishLatestProduct(product)
                _syncMessage.emit("Produto adicionado na nuvem!")
            }
            _newProductsCount.value += 1
        }
    }
    private val _isSyncing = MutableStateFlow(false)
    val isSyncing = _isSyncing.asStateFlow()
    
    fun syncProductsFromFirebase() {
        viewModelScope.launch {
            _isSyncing.value = true
            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {
                _syncMessage.emit("Aviso: Nuvem não configurada. Nenhum produto baixado.")
                _isSyncing.value = false
                return@launch
            }
            val remoteProducts = com.example.data.FirebaseService.getAllProducts()
            if (remoteProducts.isNotEmpty()) {
                repository.insertProducts(remoteProducts)
                _syncMessage.emit("Produtos atualizados da nuvem!")
            } else {
                _syncMessage.emit("Nuvem já está sincronizada.")
            }
            _isSyncing.value = false
        }
    }
    fun clearNewProductsCount() {
        _newProductsCount.value = 0
    }
    val dynamicTabs: kotlinx.coroutines.flow.StateFlow<List<com.example.data.DynamicTab>> = repository.getAllTabs()
        .stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.WhileSubscribed(5000), emptyList())

    fun insertTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.insertTab(tab) }
    fun updateTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.updateTab(tab) }
    fun deleteTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.deleteTab(tab) }

    fun setOnboardingShown() {
        viewModelScope.launch {
            userPreferences.setOnboardingShown(true)
        }
    }
}

data class ChatMessage(val text: String, val isUser: Boolean)
