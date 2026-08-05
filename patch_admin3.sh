sed -i '81,85d' app/src/main/java/com/example/ui/AdminScreen.kt
sed -i '85a \
\
    LaunchedEffect(Unit) {\
        viewModel.syncMessage.collect { message ->\
            snackbarHostState.showSnackbar(message)\
        }\
    }' app/src/main/java/com/example/ui/AdminScreen.kt

sed -i '1i import androidx.compose.material.icons.filled.Sync' app/src/main/java/com/example/ui/AdminScreen.kt
