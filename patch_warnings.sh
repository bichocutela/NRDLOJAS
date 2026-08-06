sed -i 's/fallbackToDestructiveMigration()/fallbackToDestructiveMigration(true)/g' app/src/main/java/com/example/MainActivity.kt
sed -i 's/Icons.Filled.Send/Icons.AutoMirrored.Filled.Send/g' app/src/main/java/com/example/ui/ProductBarcodeDialog.kt
sed -i 's/Divider(/HorizontalDivider(/g' app/src/main/java/com/example/ui/ProductBarcodeDialog.kt
sed -i 's/Context.VIBRATOR_SERVICE/android.content.Context.VIBRATOR_MANAGER_SERVICE/g' app/src/main/java/com/example/ui/SearchScreen.kt
