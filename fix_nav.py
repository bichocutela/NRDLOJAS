import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Fix onGoToAdmin
content = content.replace('''                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        if (userRole == "mestre") {
                            navController.navigate("mestre")
                    } else if (username == "teste" && password == "teste") {
                        loginStatus = "Login Teste realizado!"
                        onLoginSuccess("teste")
                    } else {
                            navController.navigate("admin")
                        }
                    },''', '''                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        if (userRole == "mestre") {
                            navController.navigate("mestre")
                        } else {
                            navController.navigate("admin")
                        }
                    },''')

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
