import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

target1 = """    val bannerModel = remember(appTheme) {
        "${com.example.BuildConfig.SUPABASE_URL}/storage/v1/object/public/nrdlojas-images/banners/themes/theme_${appTheme}.jpg"
    }"""

replacement1 = """    val remoteBannerUrl = remember(appTheme) {
        "${com.example.BuildConfig.SUPABASE_URL}/storage/v1/object/public/nrdlojas-images/banners/themes/theme_${appTheme}.jpg"
    }
    val localBannerUrl = remember(appTheme) {
        "file:///android_asset/themes/theme_${appTheme}.jpg"
    }"""

target2 = """                var bannerFailed by remember(appTheme) { mutableStateOf(false) }
                val localBannerRes = remember(appTheme) {
                    when (appTheme) {
                        "gold" -> com.example.R.drawable.theme_gold
                        "green" -> com.example.R.drawable.theme_green
                        "blue" -> com.example.R.drawable.theme_blue
                        "orange" -> com.example.R.drawable.theme_orange
                        else -> com.example.R.drawable.theme_red
                    }
                }
                
                if (bannerFailed) {
                    Image(
                        painter = androidx.compose.ui.res.painterResource(id = localBannerRes),
                        contentDescription = "Banner padrão",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    coil.compose.AsyncImage(
                        model = bannerModel,
                        contentDescription = "Banner Nordestão",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize(),
                        onError = { state ->
                            bannerFailed = true
                            android.util.Log.e("BannerError", "Falha ao carregar o banner: $bannerModel, erro: ${state.result.throwable.message}")
                        }
                    )
                }"""

replacement2 = """                var useLocalBanner by remember(appTheme) { mutableStateOf(false) }
                var localBannerFailed by remember(appTheme) { mutableStateOf(false) }
                
                if (localBannerFailed) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(MaterialTheme.colorScheme.primaryContainer)
                    )
                } else if (useLocalBanner) {
                    coil.compose.AsyncImage(
                        model = localBannerUrl,
                        contentDescription = "Banner Nordestão (Local)",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize(),
                        onError = { state ->
                            localBannerFailed = true
                            android.util.Log.e("BannerError", "Falha ao carregar asset local: $localBannerUrl, erro: ${state.result.throwable.message}")
                        }
                    )
                } else {
                    coil.compose.AsyncImage(
                        model = remoteBannerUrl,
                        contentDescription = "Banner Nordestão",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize(),
                        onError = { state ->
                            useLocalBanner = true
                            android.util.Log.e("BannerError", "Falha ao carregar banner remoto: $remoteBannerUrl, erro: ${state.result.throwable.message}")
                        }
                    )
                }"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
