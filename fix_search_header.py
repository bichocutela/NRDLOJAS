import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Make sure we have painterResource import
if "import androidx.compose.ui.res.painterResource" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.res.painterResource\nimport androidx.compose.foundation.Image\nimport com.example.R")

old_header = r"""        // App Bar / Header
        Row\(
            verticalAlignment = Alignment\.CenterVertically,
            modifier = Modifier
                \.fillMaxWidth\(\)
                \.padding\(top = 48\.dp, start = 8\.dp, end = 16\.dp, bottom = 16\.dp\)
        \) \{
            IconButton\(onClick = \{
                viewModel\.clearNewProductsCount\(\)
                onOpenDrawer\(\)
            \}\) \{
                BadgedBox\(
                    badge = \{
                        if \(newProductsCount > 0\) \{
                            Badge \{ Text\(newProductsCount\.toString\(\)\) \}
                        \}
                    \}
                \) \{
                    Icon\(Icons\.Default\.Menu, contentDescription = "Menu"\)
                \}
            \}
            Spacer\(modifier = Modifier\.weight\(1f\)\)
            NordestaoLogo\(\)
            Spacer\(modifier = Modifier\.weight\(1f\)\)
            // Empty box to balance the menu icon
            Box\(modifier = Modifier\.size\(48\.dp\)\)
        \}"""

new_header = """        // App Bar / Header (Hero Image)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(180.dp) // Adjust height as needed for immersion
        ) {
            Image(
                painter = painterResource(id = R.drawable.hero_banner),
                contentDescription = "Banner Nordestão",
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
            
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
        Spacer(modifier = Modifier.height(16.dp))"""

content = re.sub(old_header, new_header, content)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
