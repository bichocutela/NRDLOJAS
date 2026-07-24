cat app/src/main/java/com/example/ui/MainViewModel.kt | awk '
/import kotlinx.coroutines.flow.StateFlow/ {
    print "import kotlinx.coroutines.flow.MutableSharedFlow"
    print "import kotlinx.coroutines.flow.asSharedFlow"
    print $0
    next
}
/fun addProduct\(/ {
    print "    private val _syncMessage = MutableSharedFlow<String>()"
    print "    val syncMessage = _syncMessage.asSharedFlow()"
    print ""
    print $0
    print "        viewModelScope.launch {"
    print "            val product = Product("
    print "                code = code,"
    print "                name = name,"
    print "                searchName = name.lowercase().replace(Regex(\"[áàâã]\"), \"a\").replace(Regex(\"[éèê]\"), \"e\").replace(Regex(\"[íìî]\"), \"i\").replace(Regex(\"[óòôõ]\"), \"o\").replace(Regex(\"[úùû]\"), \"u\").replace(Regex(\"[ç]\"), \"c\"),"
    print "                category = category,"
    print "                unit = unit"
    print "            )"
    print "            repository.insertProduct(product)"
    print "            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {"
    print "                _syncMessage.emit(\"Salvo apenas localmente (Nuvem não configurada)\")"
    print "            } else {"
    print "                com.example.data.FirebaseService.saveProduct(product)"
    print "                com.example.data.FirebaseService.publishLatestProduct(product)"
    print "                _syncMessage.emit(\"Produto adicionado na nuvem!\")"
    print "            }"
    print "            _newProductsCount.value += 1"
    print "        }"
    print "    }"
    skip = 1
    next
}
/private val _isSyncing/ {
    if (skip == 1) {
        skip = 0
    }
    print $0
    next
}
/fun syncProductsFromFirebase/ {
    print $0
    print "        viewModelScope.launch {"
    print "            _isSyncing.value = true"
    print "            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {"
    print "                _syncMessage.emit(\"Aviso: Nuvem não configurada. Nenhum produto baixado.\")"
    print "                _isSyncing.value = false"
    print "                return@launch"
    print "            }"
    print "            val remoteProducts = com.example.data.FirebaseService.getAllProducts()"
    print "            if (remoteProducts.isNotEmpty()) {"
    print "                repository.insertProducts(remoteProducts)"
    print "                _syncMessage.emit(\"Produtos atualizados da nuvem!\")"
    print "            } else {"
    print "                _syncMessage.emit(\"Nuvem já está sincronizada.\")"
    print "            }"
    print "            _isSyncing.value = false"
    print "        }"
    print "    }"
    skip = 1
    next
}
/fun clearNewProductsCount/ {
    if (skip == 1) {
        skip = 0
    }
    print $0
    next
}
{
    if (skip == 0) {
        print $0
    }
}
' > MainViewModel_new.kt
mv MainViewModel_new.kt app/src/main/java/com/example/ui/MainViewModel.kt
