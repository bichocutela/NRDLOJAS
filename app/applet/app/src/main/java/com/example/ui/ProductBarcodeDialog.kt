package com.example.ui

import android.graphics.Bitmap
import androidx.compose.animation.*
import androidx.compose.animation.core.EaseIn
import androidx.compose.animation.core.EaseOutBack
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.FilterQuality
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.data.Product
import com.google.zxing.BarcodeFormat
import com.google.zxing.EncodeHintType
import com.google.zxing.MultiFormatWriter
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.EnumMap

enum class ScannerProfile {
    PADRAO, SYMBOL, DATALOGIC
}

fun generateBarcode(data: String, width: Int, height: Int): ImageBitmap? {
    try {
        val writer = MultiFormatWriter()
        val hints = EnumMap<EncodeHintType, Any>(EncodeHintType::class.java)
        hints[EncodeHintType.MARGIN] = 0
        val bitMatrix = writer.encode(data, BarcodeFormat.CODE_128, width, height, hints)
        val bmp = Bitmap.createBitmap(bitMatrix.width, bitMatrix.height, Bitmap.Config.ARGB_8888)
        for (x in 0 until bitMatrix.width) {
            for (y in 0 until bitMatrix.height) {
                bmp.setPixel(x, y, if (bitMatrix.get(x, y)) android.graphics.Color.BLACK else android.graphics.Color.WHITE)
            }
        }
        return bmp.asImageBitmap()
    } catch (e: Exception) {
        return null
    }
}

@Composable
fun ProfileButton(text: String, isSelected: Boolean, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
            contentColor = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
        ),
        shape = RoundedCornerShape(16.dp),
        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 8.dp)
    ) {
        Text(text, fontSize = 12.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ProductBarcodeDialog(product: Product, onDismiss: () -> Unit) {
    val showDialog = remember { mutableStateOf(true) }
    val animateIn = remember { mutableStateOf(false) }
    val coroutineScope = rememberCoroutineScope()
    
    var scannerProfile by remember { mutableStateOf(ScannerProfile.PADRAO) }
    var sizePercentage by remember { mutableFloatStateOf(100f) }

    fun closeDialog() {
        animateIn.value = false
        coroutineScope.launch {
            delay(200)
            showDialog.value = false
            onDismiss()
        }
    }

    if (showDialog.value) {
        LaunchedEffect(Unit) {
            animateIn.value = true
        }
        Dialog(
            onDismissRequest = { closeDialog() },
            properties = DialogProperties(usePlatformDefaultWidth = false)
        ) {
            AnimatedVisibility(
                visible = animateIn.value,
                enter = fadeIn() + scaleIn(initialScale = 0.8f, animationSpec = tween(300, easing = EaseOutBack)),
                exit = fadeOut(tween(200)) + scaleOut(targetScale = 0.8f, animationSpec = tween(200, easing = EaseIn))
            ) {
                Surface(
                    shape = RoundedCornerShape(32.dp),
                    color = MaterialTheme.colorScheme.surface,
                    modifier = Modifier.fillMaxWidth(0.95f).padding(vertical = 24.dp)
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .fillMaxWidth()
                            .verticalScroll(rememberScrollState())
                            .padding(24.dp)
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

                        val barcodeBitmap = remember(product.code) { generateBarcode(product.code, 1500, 300) }
                        
                        val screenWidth = LocalConfiguration.current.screenWidthDp.dp
                        val baseWidth = when (scannerProfile) {
                            ScannerProfile.PADRAO -> screenWidth * 0.8f
                            ScannerProfile.SYMBOL -> screenWidth * 0.9f
                            ScannerProfile.DATALOGIC -> screenWidth * 0.7f
                        }
                        val baseHeight = when (scannerProfile) {
                            ScannerProfile.PADRAO -> 90.dp
                            ScannerProfile.SYMBOL -> 110.dp
                            ScannerProfile.DATALOGIC -> 140.dp
                        }
                        val baseMargin = when (scannerProfile) {
                            ScannerProfile.PADRAO -> 16.dp
                            ScannerProfile.SYMBOL -> 24.dp
                            ScannerProfile.DATALOGIC -> 8.dp
                        }

                        val scaleFactor = sizePercentage / 100f
                        val currentWidth = baseWidth * scaleFactor
                        val currentHeight = baseHeight * scaleFactor
                        val currentMargin = baseMargin * scaleFactor

                        if (barcodeBitmap != null) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(Color.White)
                                    .padding(vertical = 16.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Image(
                                    bitmap = barcodeBitmap,
                                    contentDescription = "Código de barras",
                                    contentScale = ContentScale.FillBounds,
                                    filterQuality = FilterQuality.None,
                                    modifier = Modifier
                                        .width(currentWidth)
                                        .height(currentHeight)
                                        .padding(horizontal = currentMargin)
                                )
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                        }
                        
                        Text(
                            text = "Código de barras / Referência",
                            style = MaterialTheme.typography.bodyMedium
                        )
                        
                        Spacer(modifier = Modifier.height(24.dp))
                        Divider(color = MaterialTheme.colorScheme.outlineVariant)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text(
                            text = "Ajuste de Leitura",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.align(Alignment.Start)
                        )
                        Spacer(modifier = Modifier.height(16.dp))

                        Text(
                            text = "Perfil do Leitor",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.align(Alignment.Start)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            ProfileButton("Padrão", scannerProfile == ScannerProfile.PADRAO) { scannerProfile = ScannerProfile.PADRAO }
                            ProfileButton("Symbol", scannerProfile == ScannerProfile.SYMBOL) { scannerProfile = ScannerProfile.SYMBOL }
                            ProfileButton("Datalogic", scannerProfile == ScannerProfile.DATALOGIC) { scannerProfile = ScannerProfile.DATALOGIC }
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        Text(
                            text = "Tamanho e Proporção",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.align(Alignment.Start)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.Center,
                            modifier = Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(16.dp)).padding(8.dp)
                        ) {
                            IconButton(onClick = { sizePercentage = (sizePercentage - 10f).coerceAtLeast(30f) }) {
                                Icon(Icons.Default.Remove, contentDescription = "Diminuir")
                            }
                            Text(
                                text = "${sizePercentage.toInt()}%",
                                style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                                modifier = Modifier.padding(horizontal = 24.dp)
                            )
                            IconButton(onClick = { sizePercentage = (sizePercentage + 10f).coerceAtMost(200f) }) {
                                Icon(Icons.Default.Add, contentDescription = "Aumentar")
                            }
                        }

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
}