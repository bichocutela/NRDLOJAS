sed -i '/Scaffold(/i \    val snackbarHostState = remember { SnackbarHostState() }\
    LaunchedEffect(Unit) {\
        viewModel.syncMessage.collect { message ->\
            snackbarHostState.showSnackbar(message)\
        }\
    }' app/src/main/java/com/example/ui/MestreScreen.kt

sed -i '/Scaffold(/a \        snackbarHost = { SnackbarHost(snackbarHostState) },' app/src/main/java/com/example/ui/MestreScreen.kt
