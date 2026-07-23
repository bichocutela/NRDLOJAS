import re

with open("app/src/main/java/com/example/data/Product.kt", "r") as f:
    content = f.read()

imports = """import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Index
"""

if "import androidx.room.Index" not in content:
    content = content.replace("import androidx.room.PrimaryKey", "import androidx.room.PrimaryKey\nimport androidx.room.Index")

old_entity = """@Entity(tableName = "products")"""
new_entity = """@Entity(
    tableName = "products",
    indices = [
        Index(value = ["searchName"]),
        Index(value = ["code"]),
        Index(value = ["category"])
    ]
)"""

if "indices =" not in content:
    content = content.replace(old_entity, new_entity)

with open("app/src/main/java/com/example/data/Product.kt", "w") as f:
    f.write(content)
