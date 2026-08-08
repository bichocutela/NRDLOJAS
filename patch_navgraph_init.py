with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """    var isLoggedIn by remember { mutableStateOf(sharedPref.getBoolean("is_logged_in", false)) }
    var userRole by remember { mutableStateOf(sharedPref.getString("user_role", "admin") ?: "admin") }"""

replacement = """    val currentUser = remember { FirebaseAuth.getInstance().currentUser }
    var isLoggedIn by remember { 
        mutableStateOf(sharedPref.getBoolean("is_logged_in", false) || currentUser != null) 
    }
    var userRole by remember { 
        mutableStateOf(
            if (currentUser != null) {
                val email = currentUser.email ?: ""
                when (email) {
                    "mestre@nrdlojas.com" -> "mestre"
                    "admin@nrdlojas.com" -> "admin"
                    else -> sharedPref.getString("user_role", "admin") ?: "admin"
                }
            } else {
                sharedPref.getString("user_role", "admin") ?: "admin"
            }
        )
    }

    LaunchedEffect(isLoggedIn, userRole) {
        if (isLoggedIn) {
            sharedPref.edit()
                .putBoolean("is_logged_in", true)
                .putString("user_role", userRole)
                .apply()
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
        f.write(content)
    print("AppNavGraph init patched.")
else:
    print("Target init not found in AppNavGraph")
