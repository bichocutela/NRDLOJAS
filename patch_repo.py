import re

with open('app/src/main/java/com/example/data/ProductRepository.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'if \(missingProducts\.isNotEmpty\(\)\) \{\s*dao\.insertProducts\(missingProducts\)\s*missingProducts\.forEach \{ FirebaseService\.saveProduct\(it\) \}\s*\}')
replacement = '''if (missingProducts.isNotEmpty()) {
            dao.insertProducts(missingProducts)
            // Removed FirebaseService.saveProduct(it) to prevent local defaults from overwriting remote
        }'''

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/data/ProductRepository.kt', 'w') as f:
    f.write(content)
print("Patched ProductRepository")
