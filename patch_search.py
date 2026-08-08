import re

with open('app/src/main/java/com/example/ui/SearchScreen.kt', 'r') as f:
    content = f.read()

# Remove PullToRefreshBox wrapper
pattern_refresh = re.compile(
    r'val isSyncing by viewModel\.isSyncing\.collectAsStateWithLifecycle\(\)\s*PullToRefreshBox\(\s*isRefreshing = isSyncing,\s*onRefresh = \{ viewModel\.syncProductsFromFirebase\(\) \},\s*modifier = Modifier\.fillMaxSize\(\)\.background\(Color\.White\)\s*\)\s*\{\s*Column\(',
    re.DOTALL
)

replacement_refresh = r'''Column('''

if pattern_refresh.search(content):
    content = pattern_refresh.sub(replacement_refresh, content)
    print("Replaced PullToRefreshBox start")
else:
    print("Could not find PullToRefreshBox start")

# Remove "Adicionado recentemente" item
pattern_recently = re.compile(
    r'val dispName = latestProductFirebase\?\.get\("name"\)\?\.toString\(\) \?: latestProductLocal\?\.name\s*val dispCode = latestProductFirebase\?\.get\("code"\)\?\.toString\(\) \?: latestProductLocal\?\.code\s*if \(dispName != null && dispCode != null\) \{\s*item \{\s*Row\([\s\S]*?\}\s*\}\s*\}',
    re.DOTALL
)

if pattern_recently.search(content):
    content = pattern_recently.sub('', content)
    print("Removed Adicionado recentemente")
else:
    print("Could not find Adicionado recentemente")

with open('app/src/main/java/com/example/ui/SearchScreen.kt', 'w') as f:
    f.write(content)

