package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource

import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.Icon
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import kotlinx.coroutines.delay
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Modifier
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.platform.LocalDensity

import androidx.room.Room
import com.example.data.AppDatabase
import com.example.data.ProductRepository
import com.example.data.UserPreferences
import com.example.ui.AppNavGraph
import com.example.ui.MainViewModel
import com.example.ui.MainViewModelFactory
import com.example.ui.theme.MyApplicationTheme

import com.example.util.NotificationHelper

class MainActivity : ComponentActivity() {

    private val db by lazy {
        Room.databaseBuilder(
            applicationContext,
            AppDatabase::class.java, "products.db"
        ).fallbackToDestructiveMigration().build()
    }
    
    private val repository by lazy {
        ProductRepository(db.productDao(), db.dynamicTabDao())
    }
    private val userPreferences by lazy {
        UserPreferences(applicationContext)
    }

    private val viewModel: MainViewModel by viewModels {
        MainViewModelFactory(repository, userPreferences)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val crashLog = CrashReporter.getCrashLog(this)
        if (crashLog != null) {
            CrashReporter.clearCrashLog(this)
            setContent {
                androidx.compose.material3.MaterialTheme {
                    androidx.compose.foundation.layout.Box(modifier = Modifier.fillMaxSize().padding(16.dp)) {
                        androidx.compose.foundation.lazy.LazyColumn(modifier = Modifier.fillMaxSize()) {
                            item {
                                androidx.compose.material3.Text("App crashed previously with error:\n\n$crashLog", color = Color.Red)
                            }
                        }
                    }
                }
            }
            return
        }
        

        
        NotificationHelper.createNotificationChannel(this)
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.app.ActivityCompat.checkSelfPermission(
                    this,
                    android.Manifest.permission.POST_NOTIFICATIONS
                ) != android.content.pm.PackageManager.PERMISSION_GRANTED
            ) {
                androidx.core.app.ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.POST_NOTIFICATIONS),
                    101
                )
            }
        }
        
        enableEdgeToEdge()
        setContent {

            val fontScale by userPreferences.fontScale.collectAsState(initial = 1.0f)
            val currentDensity = LocalDensity.current
            val customDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density,
                fontScale = currentDensity.fontScale * fontScale
            )

            CompositionLocalProvider(LocalDensity provides customDensity) {
                MyApplicationTheme {

                var showSplash by remember { mutableStateOf(true) }
                
                LaunchedEffect(Unit) {
                    delay(1500)
                    showSplash = false
                }
                
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        AppNavGraph(viewModel)
                        
                        AnimatedVisibility(
                            visible = showSplash,
                            enter = fadeIn(animationSpec = tween(500)),
                            exit = fadeOut(animationSpec = tween(500))
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .background(Color.White),
                                contentAlignment = Alignment.Center
                            ) {
                                Image(
                                    painter = painterResource(id = R.drawable.splash_logo),
                                    contentDescription = "Logo",
                                    modifier = Modifier.size(150.dp)
                                )
                            }
                        }
                    }
                }
            }
            }
        }
    }
}
