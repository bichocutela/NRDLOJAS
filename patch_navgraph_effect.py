with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """    LaunchedEffect(isLoggedIn, userRole) {
        if (isLoggedIn) {
            sharedPref.edit()
                .putBoolean("is_logged_in", true)
                .putString("user_role", userRole)
                .apply()
        }
    }"""

replacement = """    LaunchedEffect(isLoggedIn, userRole) {
        if (isLoggedIn) {
            sharedPref.edit()
                .putBoolean("is_logged_in", true)
                .putString("user_role", userRole)
                .apply()
        }
    }
    
    LaunchedEffect(Unit) {
        val currentUserNow = FirebaseAuth.getInstance().currentUser
        if (currentUserNow != null) {
            val email = currentUserNow.email ?: ""
            android.util.Log.d("LoginDebug", "Inicializando com currentUser: $email")
            if (email == "mestre@nrdlojas.com") {
                navController.navigate("mestre")
            } else if (email == "admin@nrdlojas.com") {
                navController.navigate("admin")
            }
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
        f.write(content)
    print("AppNavGraph LaunchEffect patched.")
else:
    print("Target effect not found in AppNavGraph")
