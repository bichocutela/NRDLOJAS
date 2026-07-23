cat app/src/main/java/com/example/MyApplication.kt | awk '
/CrashReporter.setup\(this\)/ {
    print $0
    print "        try {"
    print "            com.google.firebase.FirebaseApp.initializeApp(this)"
    print "            Log.d(\"MyApplication\", \"Firebase initialized manually\")"
    print "        } catch (e: Exception) {"
    print "            Log.e(\"MyApplication\", \"Firebase initialization failed (missing google-services.json?)\", e)"
    print "        }"
    next
}
{ print $0 }
' > MyApplication_new.kt
mv MyApplication_new.kt app/src/main/java/com/example/MyApplication.kt
