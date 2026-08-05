package com.example.util

object ImageUrlHelper {
    fun normalizeUrl(url: String): String {
        var cleanUrl = url.trim()
        val fileRegex = Regex("""drive\.google\.com/file/d/([^/]+)/?""")
        val openRegex = Regex("""drive\.google\.com/open\?id=([^&]+)""")
        
        val fileMatch = fileRegex.find(cleanUrl)
        if (fileMatch != null) {
            val id = fileMatch.groupValues[1]
            return "https://drive.google.com/uc?id=$id"
        }
        
        val openMatch = openRegex.find(cleanUrl)
        if (openMatch != null) {
            val id = openMatch.groupValues[1]
            return "https://drive.google.com/uc?id=$id"
        }
        
        return cleanUrl
    }
}
