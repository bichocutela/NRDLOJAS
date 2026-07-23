package com.example.ui
import androidx.compose.ui.layout.ContentScale

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Restaurant
import androidx.compose.material.icons.filled.BakeryDining
import androidx.compose.material.icons.filled.Sanitizer
import androidx.compose.material.icons.filled.LocalLaundryService
import androidx.compose.material.icons.filled.SetMeal
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SearchBar
import androidx.compose.material3.SearchBarDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.Surface
import androidx.compose.material3.Badge
import androidx.compose.material3.BadgedBox
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.flow.collectLatest

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.ui.window.Dialog
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.foundation.Image
import com.example.R
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.graphics.drawscope.Stroke
import android.os.Vibrator
import android.content.Context
import android.os.VibrationEffect
import android.os.Build

import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.border
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import coil.request.ImageRequest
import androidx.compose.ui.platform.LocalContext
import com.example.data.Product
import android.graphics.Bitmap
import androidx.compose.ui.graphics.FilterQuality
import com.google.zxing.EncodeHintType
import java.util.EnumMap
import com.google.zxing.BarcodeFormat
import com.google.zxing.MultiFormatWriter
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.ui.window.Dialog
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.foundation.Image
import androidx.compose.ui.graphics.ImageBitmap


@Composable
fun StylizedText(
    text: String,
    baseStyle: TextStyle,
    largeText: Boolean,
    boldOutline: Boolean,
    uppercaseBold: Boolean,
    color: Color = Color.Unspecified,
    modifier: Modifier = Modifier
) {
    val finalText = if (uppercaseBold) text.uppercase() else text
    val weight = if (uppercaseBold || boldOutline) FontWeight.Bold else baseStyle.fontWeight
    val fontSize = if (largeText) baseStyle.fontSize * 1.3f else baseStyle.fontSize
    
    val styleWithMods = baseStyle.copy(
        fontWeight = weight,
        fontSize = fontSize,
        color = if (boldOutline) Color.Transparent else color
    )
    
    Box(modifier = modifier) {
        if (boldOutline) {
            androidx.compose.material3.Text(
                text = finalText,
                style = styleWithMods.copy(
                    drawStyle = Stroke(width = 2f)
                ),
                color = color
            )
        }
        androidx.compose.material3.Text(
            text = finalText,
            style = styleWithMods,
            color = if (boldOutline) Color.White else color
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(viewModel: MainViewModel, onOpenDrawer: () -> Unit = {}) {
    val bannerImageUri by viewModel.userPreferences.bannerImageUri.collectAsState(initial = null)
    val searchQuery by viewModel.searchQuery.collectAsStateWithLifecycle()
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    val mostUsed by viewModel.mostUsed.collectAsStateWithLifecycle()
    val history by viewModel.history.collectAsStateWithLifecycle()
    val favorites by viewModel.favorites.collectAsStateWithLifecycle()
    val newProductsCount by viewModel.newProductsCount.collectAsStateWithLifecycle()

    var isScannerOpen by remember { mutableStateOf(false) }

    if (isScannerOpen) {
        BarcodeScannerScreen(
            onBarcodeScanned = { code ->
                viewModel.updateSearchQuery(code)
                isScannerOpen = false
            },
            onClose = { isScannerOpen = false }
        )
        return // Return early so we don't show the rest of the screen
    }


    val aiProductDetails by viewModel.aiProductDetails.collectAsStateWithLifecycle()
    val isAiLoading by viewModel.isAiLoading.collectAsStateWithLifecycle()

    if (isAiLoading || aiProductDetails != null) {
        AlertDialog(
            onDismissRequest = { viewModel.clearAiProductDetails() },
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text("Detalhes com IA")
                }
            },
            text = {
                if (isAiLoading) {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                } else {
                    Text(aiProductDetails ?: "")
                }
            },
            confirmButton = {
                TextButton(onClick = { viewModel.clearAiProductDetails() }) {
                    Text("Fechar")
                }
            }
        )
    }


    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // App Bar / Header (Hero Image)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(180.dp) // Adjust height as needed for immersion
        ) {
            Box(
                modifier = Modifier.fillMaxSize()
            ) {
                coil.compose.AsyncImage(
                    model = bannerImageUri?.takeIf { it.isNotEmpty() } ?: R.drawable.hero_banner,
                    contentDescription = "Banner Nordestão",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Text(
                    text = "NRD Códigos Correlatos",
                    style = MaterialTheme.typography.titleMedium,
                    color = Color(0xFFE31B23), // Red color
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 8.dp)
                )
            }
            
            // Hamburger Menu overlay
            IconButton(
                onClick = {
                    viewModel.clearNewProductsCount()
                    onOpenDrawer()
                },
                modifier = Modifier
                    .padding(top = 48.dp, start = 8.dp)
                    .background(Color.Transparent) // Transparent background
            ) {
                BadgedBox(
                    badge = {
                        if (newProductsCount > 0) {
                            Badge { Text(newProductsCount.toString()) }
                        }
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.Menu, 
                        contentDescription = "Menu",
                        tint = Color.White // White icon for visibility over the banner
                    )
                }
            }
        }
        Spacer(modifier = Modifier.height(16.dp))

        // Custom Search Bar
        Column(
            modifier = Modifier.padding(horizontal = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            SearchBar(
                query = searchQuery,
                onQueryChange = viewModel::updateSearchQuery,
                onSearch = { },
                active = false,
                onActiveChange = { },
                placeholder = { Text("Pesquisar produto...", style = MaterialTheme.typography.bodyLarge) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Pesquisar", modifier = Modifier.size(28.dp)) },
                trailingIcon = {
                    Row {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { viewModel.updateSearchQuery("") }) {
                                Icon(Icons.Default.Clear, contentDescription = "Limpar")
                            }

                        } else {
                            IconButton(onClick = { isScannerOpen = true }) {
                                Icon(Icons.Default.CameraAlt, contentDescription = "Scanner QR", tint = MaterialTheme.colorScheme.primary)
                            }
                            IconButton(onClick = { /* TODO Voice Search */ }) {
                                Icon(Icons.Default.Mic, contentDescription = "Voz", tint = MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White, RoundedCornerShape(32.dp))
                    .border(2.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(32.dp)),
                colors = SearchBarDefaults.colors(
                    containerColor = Color.Transparent,
                    dividerColor = Color.Transparent,
                )
            ) {}
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = { /* Do search */ },
                shape = RoundedCornerShape(32.dp), // Estilo balão gigante
                modifier = Modifier.fillMaxWidth().height(64.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Text("PESQUISAR PRODUTO", fontWeight = FontWeight.Black, fontSize = 18.sp, letterSpacing = 1.sp)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (searchQuery.isNotEmpty()) {
            // Search Results
            LazyColumn(
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(searchResults) { product ->
                    ProductCard(product, viewModel)
                }
            }
        } else {
            // Dashboard (Categories, Most Used, History, Favorites)
            LazyColumn(
                contentPadding = PaddingValues(bottom = 16.dp),
                verticalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                item {
                    CategorySection(viewModel)
                }

                if (mostUsed.isNotEmpty()) {
                    item {
                        SectionHeader("Mais Utilizados")
                        LazyRow(
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(mostUsed) { product ->
                                MiniProductCard(product, viewModel)
                            }
                        }
                    }
                }

                if (history.isNotEmpty()) {
                    item {
                        SectionHeader("Histórico Recente")
                        Column(
                            modifier = Modifier.padding(horizontal = 16.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            history.take(5).forEach { product ->
                                HistoryItem(product, viewModel)
                            }
                        }
                    }
                }

                if (favorites.isNotEmpty()) {
                    item {
                        SectionHeader("Meus Favoritos")
                        Column(
                            modifier = Modifier.padding(horizontal = 16.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            favorites.forEach { product ->
                                ProductCard(product, viewModel)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun SectionHeader(title: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        if (title == "Mais Utilizados") {
            Text(
                text = "IA ATIVA",
                style = MaterialTheme.typography.labelMedium.copy(fontSize = 10.sp),
                color = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier
                    .background(MaterialTheme.colorScheme.primary, CircleShape)
                    .padding(horizontal = 8.dp, vertical = 2.dp)
            )
        }
    }
}

@Composable
fun CategorySection(viewModel: MainViewModel) {
    val categories = listOf(
        Pair("Padaria", MaterialTheme.colorScheme.tertiaryContainer to MaterialTheme.colorScheme.onTertiaryContainer),
        Pair("Hortifruti", MaterialTheme.colorScheme.secondaryContainer to MaterialTheme.colorScheme.onSecondaryContainer),
        Pair("Açougue", MaterialTheme.colorScheme.primaryContainer to MaterialTheme.colorScheme.onPrimaryContainer),
        Pair("Frios", MaterialTheme.colorScheme.tertiaryContainer to MaterialTheme.colorScheme.onTertiaryContainer),
        Pair("Confeitaria", MaterialTheme.colorScheme.secondaryContainer to MaterialTheme.colorScheme.onSecondaryContainer),
        Pair("Rotisserie", MaterialTheme.colorScheme.primaryContainer to MaterialTheme.colorScheme.onPrimaryContainer)
    )
    
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.padding(bottom = 8.dp)
    ) {
        items(categories) { (category, colors) ->
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(12.dp))
                    .background(colors.first)
                    .clickable { viewModel.updateSearchQuery(category) }
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = category.uppercase(),
                    style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                    color = colors.second
                )
            }
        }
    }
}

@Composable
fun ProductCard(product: Product, viewModel: MainViewModel) {
    val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)
    val vibrateOnFound by viewModel.userPreferences.vibrateOnFound.collectAsState(initial = true)
    val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)
    val boldOutline by viewModel.userPreferences.boldOutline.collectAsState(initial = false)
    val uppercaseBold by viewModel.userPreferences.uppercaseBold.collectAsState(initial = false)
    val context = LocalContext.current
    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator }
    fun triggerVibration() {
        if (!vibrateOnClick) return
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(50)
        }
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(Color.White)
            .border(1.dp, MaterialTheme.colorScheme.surface, RoundedCornerShape(24.dp))
            .clickable { viewModel.onProductSearched(product) }
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Icon / Category Color Box
        if (product.imageUrl != null) {
            AsyncImage(
                model = product.imageUrl,
                contentDescription = product.name,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
            )
        } else {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = product.name.take(1).uppercase(),
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
        }

        Spacer(modifier = Modifier.width(16.dp))

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = product.name,
                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground)
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = getCategoryIcon(product.category),
                    style = MaterialTheme.typography.bodySmall
                )
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = product.category.uppercase(),
                    style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold, letterSpacing = 1.sp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Spacer(modifier = Modifier.width(16.dp))

        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(MaterialTheme.colorScheme.primaryContainer)
                .padding(horizontal = 16.dp, vertical = 8.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = product.code,
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Black),
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
                Text(
                    text = product.unit.uppercase(),
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp, fontWeight = FontWeight.Black),
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }

        Spacer(modifier = Modifier.width(8.dp))
        androidx.compose.material3.IconButton(
            onClick = { viewModel.consultProductInfoAi(product) },
            modifier = Modifier.background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
        ) {
            Icon(Icons.Default.AutoAwesome, contentDescription = "IA Info", tint = MaterialTheme.colorScheme.onTertiaryContainer)
        }
    }
}


@Composable
fun MiniProductCard(product: Product, viewModel: MainViewModel) {
    val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)
    val vibrateOnFound by viewModel.userPreferences.vibrateOnFound.collectAsState(initial = true)
    val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)
    val boldOutline by viewModel.userPreferences.boldOutline.collectAsState(initial = false)
    val uppercaseBold by viewModel.userPreferences.uppercaseBold.collectAsState(initial = false)
    val context = LocalContext.current
    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator }
    fun triggerVibration() {
        if (!vibrateOnClick) return
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(50)
        }
    }

    Column(
        modifier = Modifier
            .width(160.dp)
            .height(100.dp)
            .clip(RoundedCornerShape(24.dp))
            .background(Color.White)
            .border(1.dp, MaterialTheme.colorScheme.surface, RoundedCornerShape(24.dp))
            .clickable { viewModel.onProductSearched(product) }
            .padding(16.dp),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (product.imageUrl != null) {
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(product.imageUrl)
                        .crossfade(true)
                        .build(),
                    contentDescription = product.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                )
            } else {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primaryContainer),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = product.name.take(1).uppercase(),
                        style = MaterialTheme.typography.titleMedium.copy(fontSize = 14.sp),
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            Text(
                text = product.unit.uppercase(),
                style = MaterialTheme.typography.labelMedium.copy(fontSize = 10.sp),
                color = MaterialTheme.colorScheme.primary
            )
        }
        
        Column {
            Text(
                text = product.name,
                style = MaterialTheme.typography.titleMedium.copy(fontSize = 14.sp),
                color = MaterialTheme.colorScheme.onBackground,
                maxLines = 1
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = getCategoryIcon(product.category),
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp)
                )
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = product.category.uppercase(),
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Text(
                text = product.code,
                style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, fontSize = 24.sp, letterSpacing = (-1).sp),
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

@Composable
fun HistoryItem(product: Product, viewModel: MainViewModel) {
    val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)
    val vibrateOnFound by viewModel.userPreferences.vibrateOnFound.collectAsState(initial = true)
    val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)
    val boldOutline by viewModel.userPreferences.boldOutline.collectAsState(initial = false)
    val uppercaseBold by viewModel.userPreferences.uppercaseBold.collectAsState(initial = false)
    val context = LocalContext.current
    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator }
    fun triggerVibration() {
        if (!vibrateOnClick) return
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator?.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
        } else {
            @Suppress("DEPRECATION")
            vibrator?.vibrate(50)
        }
    }

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

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.5f))
            .border(1.dp, MaterialTheme.colorScheme.primaryContainer, RoundedCornerShape(16.dp))
            .clickable { triggerVibration(); showDialog = true }
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                imageVector = Icons.Default.History,
                contentDescription = "Histórico",
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(20.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium.copy(fontSize = 14.sp),
                    color = MaterialTheme.colorScheme.onBackground
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = getCategoryIcon(product.category),
                        style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = product.category.uppercase(),
                        style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp),
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Text(
                    text = "Código: ${product.code}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
fun NordestaoLogo() {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        // The 4 circles
        Row(
            horizontalArrangement = Arrangement.spacedBy(4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            LogoCircle(color = Color(0xFFD32F2F), icon = Icons.Default.Eco)
            LogoCircle(color = Color(0xFF388E3C), icon = Icons.Default.Restaurant)
            LogoCircle(color = Color(0xFFF57C00), icon = Icons.Default.BakeryDining)
            LogoCircle(color = Color(0xFF1976D2), icon = Icons.Default.LocalLaundryService)
        }
        
        Spacer(modifier = Modifier.width(8.dp))
        
        // Text
        Column(horizontalAlignment = Alignment.Start) {
            Text(
                text = "supermercado",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp,
                    fontSize = 8.sp
                ),
                color = Color.DarkGray
            )
            Text(
                text = "Nordestão",
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.ExtraBold,
                    letterSpacing = (-0.5).sp
                ),
                color = Color(0xFF424242)
            )
        }
    }
}

@Composable
fun LogoCircle(color: Color, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Box(
        modifier = Modifier
            .size(28.dp)
            .background(color = color, shape = CircleShape)
            .border(width = 1.dp, color = Color.White, shape = CircleShape),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Color.White,
            modifier = Modifier.size(16.dp)
        )
    }
}

fun getCategoryIcon(category: String): String {
    return when (category.lowercase()) {
        "padaria" -> "🥖"
        "açougue" -> "🥩"
        "hortifruti" -> "🥬"
        "frios" -> "🧀"
        "confeitaria" -> "🍰"
        "rotisserie" -> "🍗"
        "bebidas" -> "🥤"
        else -> "🏷️"
    }
}

fun generateBarcodeBitmap(data: String): ImageBitmap? {
    try {
        val writer = MultiFormatWriter()
        val hints = EnumMap<EncodeHintType, Any>(EncodeHintType::class.java)
        hints[EncodeHintType.MARGIN] = 0 // we handle margin in Compose
        
        // Generate with higher horizontal resolution to prevent artifacts, 
        // but even with FilterQuality.None, drawing sharp is best
        val bitMatrix = writer.encode(data, BarcodeFormat.CODE_128, 1024, 256, hints)
        val width = bitMatrix.width
        val height = bitMatrix.height
        val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        for (x in 0 until width) {
            for (y in 0 until height) {
                bitmap.setPixel(x, y, if (bitMatrix.get(x, y)) android.graphics.Color.BLACK else android.graphics.Color.WHITE)
            }
        }
        return bitmap.asImageBitmap()
    } catch (e: Exception) {
        return null
    }
}
