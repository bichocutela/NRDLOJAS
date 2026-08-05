sed -i '257a \
\
    fun syncDatabase() {\
        viewModelScope.launch {\
            _isSyncing.value = true\
            try {\
                if (!com.example.data.FirebaseService.isFirebaseConfigured()) {\
                    _syncMessage.emit("Aviso: Nuvem não configurada. Impossível sincronizar.")\
                    return@launch\
                }\
                val localProducts = repository.getAllProductsSync()\
                if (localProducts.isNotEmpty()) {\
                    com.example.data.FirebaseService.syncAllProducts(localProducts)\
                }\
                val remoteProducts = com.example.data.FirebaseService.getAllProducts()\
                if (remoteProducts.isNotEmpty()) {\
                    repository.insertProducts(remoteProducts)\
                }\
                _syncMessage.emit("Banco de dados sincronizado com sucesso!")\
            } catch (e: Exception) {\
                _syncMessage.emit("Erro ao sincronizar: ${e.message}")\
            } finally {\
                _isSyncing.value = false\
            }\
        }\
    }' app/src/main/java/com/example/ui/MainViewModel.kt
