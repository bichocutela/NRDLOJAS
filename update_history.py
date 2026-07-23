import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Add imports for animations and dialog
imports_to_add = """import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.ui.window.Dialog
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.text.style.TextAlign
"""

if "import androidx.compose.animation.*" not in content:
    content = content.replace("import androidx.compose.foundation.Image", imports_to_add + "import androidx.compose.foundation.Image")

old_history = """fun HistoryItem(product: Product, viewModel: MainViewModel) {
    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            confirmButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("FECHAR", color = MaterialTheme.colorScheme.primary)
                }
            },
            title = {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black)
                )
            },
            text = {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = product.code,
                        style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    val barcodeBitmap = generateBarcodeBitmap(product.code)
                    if (barcodeBitmap != null) {
                        Image(
                            bitmap = barcodeBitmap,
                            contentDescription = "Código de barras",
                            contentScale = ContentScale.FillBounds,
                            filterQuality = FilterQuality.None,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(90.dp)
                                .padding(horizontal = 24.dp)
                                .background(androidx.compose.ui.graphics.Color.White)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                    }
                    
                    Text(
                        text = "Código de barras / Referência",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            },
            shape = RoundedCornerShape(32.dp),
            containerColor = Color.White
        )
    }

    Row("""

new_history = """fun HistoryItem(product: Product, viewModel: MainViewModel) {
    var showDialog by remember { mutableStateOf(false) }
    var animateIn by remember { mutableStateOf(false) }
    val coroutineScope = rememberCoroutineScope()

    fun closeDialog() {
        animateIn = false
        coroutineScope.launch {
            delay(200)
            showDialog = false
        }
    }

    if (showDialog) {
        androidx.compose.runtime.LaunchedEffect(Unit) {
            animateIn = true
        }
        Dialog(onDismissRequest = { closeDialog() }) {
            AnimatedVisibility(
                visible = animateIn,
                enter = fadeIn() + scaleIn(initialScale = 0.8f, animationSpec = tween(300, easing = EaseOutBack)),
                exit = fadeOut(tween(200)) + scaleOut(targetScale = 0.8f, animationSpec = tween(200, easing = EaseIn))
            ) {
                Surface(
                    shape = RoundedCornerShape(32.dp),
                    color = Color.White,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally, 
                        modifier = Modifier.fillMaxWidth().padding(24.dp)
                    ) {
                        Text(
                            text = product.name,
                            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black),
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = product.code,
                            style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        val barcodeBitmap = generateBarcodeBitmap(product.code)
                        if (barcodeBitmap != null) {
                            Image(
                                bitmap = barcodeBitmap,
                                contentDescription = "Código de barras",
                                contentScale = ContentScale.FillBounds,
                                filterQuality = FilterQuality.None,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(90.dp)
                                    .padding(horizontal = 8.dp)
                                    .background(androidx.compose.ui.graphics.Color.White)
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        
                        Text(
                            text = "Código de barras / Referência",
                            style = MaterialTheme.typography.bodyMedium
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Button(
                            onClick = { closeDialog() },
                            modifier = Modifier.fillMaxWidth().height(56.dp),
                            shape = RoundedCornerShape(24.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                        ) {
                            Text("FECHAR", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        }
                    }
                }
            }
        }
    }

    Row("""

content = content.replace(old_history, new_history)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
