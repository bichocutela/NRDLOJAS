import re

with open("app/src/main/java/com/example/data/ProductRepository.kt", "r") as f:
    content = f.read()

target = """class ProductRepository(private val dao: ProductDao) {"""
replacement = """class ProductRepository(
    private val dao: ProductDao,
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
