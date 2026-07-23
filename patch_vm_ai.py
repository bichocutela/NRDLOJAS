import re

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "r") as f:
    content = f.read()

state_code = """
    private val _aiProductDetails = MutableStateFlow<String?>(null)
    val aiProductDetails = _aiProductDetails.asStateFlow()

    private val _isAiLoading = MutableStateFlow(false)
    val isAiLoading = _isAiLoading.asStateFlow()
"""

func_code = """
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
"""

content = content.replace("    val chatMessages = _chatMessages.asStateFlow()", "    val chatMessages = _chatMessages.asStateFlow()\n" + state_code)
content = content.replace("    fun sendChatMessage() {", func_code + "\n    fun sendChatMessage() {")

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "w") as f:
    f.write(content)

