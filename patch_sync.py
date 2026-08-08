import re

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()

pattern_sync_products = re.compile(r'fun syncProductsFromFirebase\(\) \{[\s\S]*?fun syncDatabase\(\) \{[\s\S]*?_syncMessage\.emit\("Erro ao sincronizar: \$\{e\.message\}"\)\s*\}\s*finally\s*\{\s*_isSyncing\.value = false\s*\}\s*\}\s*\}')

replacement = '''fun syncProductsFromFirebase() {
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

    fun syncDatabase() {
        viewModelScope.launch {
            _isSyncing.value = true
            try {
                if (!com.example.data.FirebaseService.isFirebaseConfigured()) {
                    val msg = com.example.data.FirebaseService.lastError ?: "Configuração ausente."
                    _syncMessage.emit("Nuvem não configurada: $msg")
                    _isSyncing.value = false
                    return@launch
                }
                
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
                
                _syncMessage.emit("Banco de dados sincronizado com sucesso!")
            } catch (e: Throwable) {
                _syncMessage.emit("Erro ao sincronizar: ${e.message}")
            } finally {
                _isSyncing.value = false
            }
        }
    }'''

content = pattern_sync_products.sub(replacement, content)

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)
print("Patched MainViewModel sync logic")
