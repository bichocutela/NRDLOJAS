import re

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace old sync logic in init block
pattern_init_latest = re.compile(r'viewModelScope\.launch \{\s*com\.example\.data\.FirebaseService\.observeLatestProduct\(\)\.collect \{\s*_latestProduct\.value = it\s*if \(it != null\) \{\s*syncProductsFromFirebase\(\)\s*\}\s*\}\s*\}')
replacement_init_latest = '''viewModelScope.launch {
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
        }'''
content = pattern_init_latest.sub(replacement_init_latest, content)

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)
print("Patched MainViewModel init for automatic sync")
