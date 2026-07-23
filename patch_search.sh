sed -i '/fun SearchScreen/a \
    val bannerImageUri by viewModel.userPreferences.bannerImageUri.collectAsState(initial = null)' app/src/main/java/com/example/ui/SearchScreen.kt

sed -i 's/model = R.drawable.hero_banner,/model = bannerImageUri ?: R.drawable.hero_banner,/g' app/src/main/java/com/example/ui/SearchScreen.kt
