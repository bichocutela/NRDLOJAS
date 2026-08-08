import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

pattern = re.compile(
    r'LaunchedEffect\(latestFirebase,\s*latestLocal,\s*lastNotifiedCode\)\s*\{\s*if \(lastNotifiedCode == "___LOADING___"\) return@LaunchedEffect\s*val dispName = latestFirebase\?\.get\("name"\)\?\.toString\(\) \?: latestLocal\?\.name\s*val dispCode = latestFirebase\?\.get\("code"\)\?\.toString\(\) \?: latestLocal\?\.code\s*if \(dispName != null && dispCode != null && dispCode != lastNotifiedCode\)\s*\{\s*com\.example\.util\.NotificationHelper\.showNewProductNotification\(context, dispName\)\s*userPreferences\.setLastNotifiedProductCode\(dispCode\)\s*\}\s*\}',
    re.DOTALL
)

replacement = """LaunchedEffect(latestFirebase, lastNotifiedCode) {
                if (lastNotifiedCode == "___LOADING___") return@LaunchedEffect
                
                val dispName = latestFirebase?.get("name")?.toString()
                val eventId = latestFirebase?.get("timestamp")?.toString() ?: latestFirebase?.get("code")?.toString()
                
                if (dispName != null && eventId != null && eventId != lastNotifiedCode) {
                    if (lastNotifiedCode == null) {
                        // Primeiro acesso após instalação: apenas registra o evento atual para não notificar coisas antigas
                        userPreferences.setLastNotifiedProductCode(eventId)
                    } else {
                        com.example.util.NotificationHelper.showNewProductNotification(context, dispName)
                        userPreferences.setLastNotifiedProductCode(eventId)
                    }
                }
            }"""

if pattern.search(content):
    new_content = pattern.sub(replacement, content)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(new_content)
    print("Patched successfully")
else:
    print("Pattern not found")
