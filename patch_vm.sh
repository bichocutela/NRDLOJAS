sed -i '/val remoteProducts = com.example.data.FirebaseService.getAllProducts()/i \
                val bannerUrl = com.example.data.FirebaseService.getBannerUrl()\
                if (bannerUrl != null) {\
                    userPreferences.setBannerImageUri(bannerUrl)\
                }' app/src/main/java/com/example/ui/MainViewModel.kt
