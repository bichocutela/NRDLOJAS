sed -i '80a \
    LaunchedEffect(Unit) {\
        viewModel.syncMessage.collect { message ->\
            snackbarHostState.showSnackbar(message)\
        }\
    }' app/src/main/java/com/example/ui/AdminScreen.kt
