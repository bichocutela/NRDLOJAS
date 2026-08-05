sed -i '276,282d' app/src/main/java/com/example/ui/AppNavGraph.kt
sed -i 's/loginStatus = "Entrando no modo local..."/loginStatus = null/g' app/src/main/java/com/example/ui/AppNavGraph.kt
sed -i 's/loginStatus = "Login realizado com sucesso!"/loginStatus = null/g' app/src/main/java/com/example/ui/AppNavGraph.kt
