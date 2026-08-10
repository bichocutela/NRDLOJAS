import re
content = open("app/src/main/java/com/example/data/ProductRepository.kt").read()

target = r"    suspend fun insertProduct\(product: Product\) \{(.+?)\}"
match = re.search(target, content, re.DOTALL)
if match:
    pass

def replace_method(name):
    global content
    pattern = r"suspend fun " + name + r"\(product: Product\) \{[\s\S]*?\}"
    replacement = f"suspend fun {name}(product: Product) {{\n        dao.{name}(product)\n    }}"
    content = re.sub(pattern, replacement, content)

replace_method("insertProduct")
replace_method("updateProduct")

open("app/src/main/java/com/example/data/ProductRepository.kt", "w").write(content)
print("Success")
