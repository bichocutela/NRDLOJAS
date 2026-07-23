import re

with open("app/src/main/java/com/example/data/AppDatabase.kt", "r") as f:
    content = f.read()

content = content.replace("entities = [Product::class]", "entities = [Product::class, DynamicTab::class]")
content = content.replace("version = 3", "version = 4")
content = content.replace("abstract fun productDao(): ProductDao", "abstract fun productDao(): ProductDao\n    abstract fun dynamicTabDao(): DynamicTabDao")

with open("app/src/main/java/com/example/data/AppDatabase.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

target = """class ProductRepository(private val productDao: ProductDao) {"""
replacement = """class ProductRepository(
    private val productDao: ProductDao,
    private val dynamicTabDao: DynamicTabDao? = null
) {
    fun getAllTabs() = dynamicTabDao?.getAllTabs() ?: kotlinx.coroutines.flow.flowOf(emptyList())
    suspend fun insertTab(tab: DynamicTab) { dynamicTabDao?.insertTab(tab) }
    suspend fun updateTab(tab: DynamicTab) { dynamicTabDao?.updateTab(tab) }
    suspend fun deleteTab(tab: DynamicTab) { dynamicTabDao?.deleteTab(tab) }
"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/data/ProductRepository.kt", "w") as f:
    f.write(content)
