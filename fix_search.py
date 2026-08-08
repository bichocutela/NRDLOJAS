with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = lines[:158] + [
    "    val bannerModel = remember(appTheme, bannerImageUri) {\n",
    "        val supabaseUrl = com.example.BuildConfig.SUPABASE_URL\n",
    "        if (appTheme != \"red\") {\n",
    "            \"$supabaseUrl/storage/v1/object/public/nrdlojas-images/banners/themes/theme_${appTheme}.jpg\"\n",
    "        } else {\n",
    "            if (bannerImageUri != null && bannerImageUri!!.startsWith(\"data:image\")) {\n",
    "                val base64 = bannerImageUri!!.substringAfter(\"base64,\")\n",
    "                android.util.Base64.decode(base64, android.util.Base64.DEFAULT)\n",
    "            } else if (bannerImageUri != null && bannerImageUri!!.isNotEmpty()) {\n",
    "                bannerImageUri\n",
    "            } else {\n",
    "                null\n",
    "            }\n",
    "        }\n",
    "    }\n",
    "\n"
] + lines[173:]

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.writelines(new_lines)
