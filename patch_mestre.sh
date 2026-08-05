sed -i '/com.example.util.NotificationHelper.showToast(context, "Fundo alterado com sucesso para todos!", android.widget.Toast.LENGTH_SHORT)/a \
                                        viewModel.userPreferences.setBannerImageUri(url)' app/src/main/java/com/example/ui/MestreScreen.kt
