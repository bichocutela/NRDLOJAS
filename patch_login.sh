cat app/src/main/java/com/example/ui/AppNavGraph.kt | awk '
/if \(role == "mestre"\) \{/ {
    print $0
    next
}
/navController\.navigate\("mestre"\)/ {
    print $0
    next
}
/\} else \{/ {
    if (in_nav == 0) {
        in_nav = 1
        print "                        } else if (role == \"admin\") {"
        next
    }
}
/navController\.navigate\("admin"\)/ {
    if (in_nav == 1) {
        in_nav = 2
        print $0
        print "                        } else if (role == \"teste\") {"
        print "                            navController.navigate(\"search\")"
        next
    }
}
/if \(username == "mestre" && password == "nrdlojas"\) \{/ {
    print $0
    next
}
/\} else if \(username == "admin" && password == "nrdlojas"\) \{/ {
    print $0
    next
}
/onLoginSuccess\("admin"\)/ {
    print $0
    next
}
/\} else \{/ {
    if (in_login == 0 && in_nav == 2) {
        in_login = 1
        print "                    } else if (username == \"teste\" && password == \"teste\") {"
        print "                        loginStatus = \"Login Teste realizado!\""
        print "                        onLoginSuccess(\"teste\")"
        print "                    } else {"
        next
    }
}
{ print $0 }
' > AppNavGraph_new.kt
mv AppNavGraph_new.kt app/src/main/java/com/example/ui/AppNavGraph.kt
