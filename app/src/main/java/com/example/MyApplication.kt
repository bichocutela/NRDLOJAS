package com.example

import android.app.Application
import android.util.Log

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        CrashReporter.setup(this)
        Log.d("MyApplication", "Application started and CrashReporter setup")
    }
}
