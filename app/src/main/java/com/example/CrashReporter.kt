package com.example

import android.app.Application
import android.content.Context
import android.content.Intent
import java.io.File
import java.io.PrintWriter
import java.io.StringWriter

object CrashReporter {
    fun setup(context: Context) {
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, exception ->
            try {
                val sw = StringWriter()
                exception.printStackTrace(PrintWriter(sw))
                val logFile = File(context.filesDir, "crash_log.txt")
                logFile.writeText(sw.toString())
            } catch (e: Exception) {
                // Ignore
            }
            defaultHandler?.uncaughtException(thread, exception)
        }
    }

    fun getCrashLog(context: Context): String? {
        val logFile = File(context.filesDir, "crash_log.txt")
        return if (logFile.exists()) logFile.readText() else null
    }

    fun clearCrashLog(context: Context) {
        val logFile = File(context.filesDir, "crash_log.txt")
        if (logFile.exists()) logFile.delete()
    }
}
