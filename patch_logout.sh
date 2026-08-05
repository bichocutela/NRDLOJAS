sed -i 's/onClick = onLogout/onClick = { loginStatus = null; onLogout() }/g' app/src/main/java/com/example/ui/AppNavGraph.kt
