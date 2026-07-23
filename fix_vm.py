import re

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "r") as f:
    content = f.read()

if "import com.example.data.UserPreferences" not in content:
    content = content.replace("import com.example.data.ProductRepository", "import com.example.data.ProductRepository\nimport com.example.data.UserPreferences")

old_class = "class MainViewModel(private val repository: ProductRepository) : ViewModel() {"
new_class = "class MainViewModel(private val repository: ProductRepository, val userPreferences: UserPreferences) : ViewModel() {"
content = content.replace(old_class, new_class)

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "w") as f:
    f.write(content)
