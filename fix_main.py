import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "import com.example.data.UserPreferences" not in content:
    content = content.replace("import com.example.data.ProductRepository", "import com.example.data.ProductRepository\nimport com.example.data.UserPreferences")

old_repo = """    private val repository by lazy {
        ProductRepository(db.productDao())
    }"""

new_repo = """    private val repository by lazy {
        ProductRepository(db.productDao())
    }
    private val userPreferences by lazy {
        UserPreferences(applicationContext)
    }"""

if "private val userPreferences" not in content:
    content = content.replace(old_repo, new_repo)
    
old_vm = """    private val viewModel: MainViewModel by viewModels {
        MainViewModelFactory(repository)
    }"""
new_vm = """    private val viewModel: MainViewModel by viewModels {
        MainViewModelFactory(repository, userPreferences)
    }"""
content = content.replace(old_vm, new_vm)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
