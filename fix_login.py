import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

content = content.replace('''                    } else if (username == "admin" && password == "nrdlojas") {
                        loginStatus = "Login Admin realizado!"
                        onLoginSuccess("admin")
                    } else {''', '''                    } else if (username == "admin" && password == "nrdlojas") {
                        loginStatus = "Login Admin realizado!"
                        onLoginSuccess("admin")
                    } else if (username == "teste" && password == "teste") {
                        loginStatus = "Login Teste realizado!"
                        onLoginSuccess("teste")
                    } else {''')

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
