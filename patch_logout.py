with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target_logout = """            OutlinedButton(
                onClick = { 
                    loginStatus = null
                    isLoggedIn = false
                    userRole = "admin"
                    onLogout() 
                },
                modifier = Modifier.fillMaxWidth()
            ) {"""

replacement_logout = """            OutlinedButton(
                onClick = { 
                    loginStatus = null
                    onLogout() 
                },
                modifier = Modifier.fillMaxWidth()
            ) {"""

if target_logout in content:
    content = content.replace(target_logout, replacement_logout)
    print("Logout patched")
else:
    print("Logout logic not found")

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)

