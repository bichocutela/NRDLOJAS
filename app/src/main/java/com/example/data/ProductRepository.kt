package com.example.data

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.text.Normalizer
import kotlin.math.min

class ProductRepository(
    private val dao: ProductDao,
    private val dynamicTabDao: DynamicTabDao? = null
) {
    fun getAllTabs() = dynamicTabDao?.getAllTabs() ?: kotlinx.coroutines.flow.flowOf(emptyList())
    suspend fun insertTab(tab: DynamicTab) { dynamicTabDao?.insertTab(tab) }
    suspend fun updateTab(tab: DynamicTab) { dynamicTabDao?.updateTab(tab) }
    suspend fun deleteTab(tab: DynamicTab) { dynamicTabDao?.deleteTab(tab) }

    val allProducts: Flow<List<Product>> = dao.getAllProducts()
    val favorites: Flow<List<Product>> = dao.getFavorites()
    val mostUsed: Flow<List<Product>> = dao.getMostUsed()
    val history: Flow<List<Product>> = dao.getHistory()
    val productsCountByCategory: Flow<List<CategoryCount>> = dao.getProductsCountByCategory()
    val latestProductLocal = dao.getLatestProduct()

    fun searchProducts(query: String): Flow<List<Product>> {
        val normalizedQuery = query.unaccent().lowercase().trim()
        val tokens = normalizedQuery.split("\\s+".toRegex()).filter { it.isNotEmpty() }
        
        return dao.getAllProducts().map { products ->
            if (tokens.isEmpty()) return@map emptyList()
            
            products.filter { product ->
                val searchName = product.searchName
                val code = product.code
                val category = product.category.unaccent().lowercase()
                
                if (code.contains(normalizedQuery)) return@filter true
                
                tokens.all { token ->
                    searchName.contains(token) || isTypoMatch(token, searchName) || category.contains(token)
                }
            }.sortedWith(compareByDescending<Product> { it.searchCount }.thenBy { it.name })
        }
    }

    suspend fun searchProductsSync(query: String): List<Product> {
        val normalizedQuery = query.unaccent().lowercase().trim()
        val tokens = normalizedQuery.split("\\s+".toRegex()).filter { it.isNotEmpty() }
        
        val products = dao.getAllProductsSync()
        if (tokens.isEmpty()) return products
        
        return products.filter { product ->
            val searchName = product.searchName
            val code = product.code
            val category = product.category.unaccent().lowercase()
            
            if (code.contains(normalizedQuery)) return@filter true
            
            tokens.all { token ->
                searchName.contains(token) || isTypoMatch(token, searchName) || category.contains(token)
            }
        }.sortedWith(compareByDescending<Product> { it.searchCount }.thenBy { it.name })
    }
    
    fun getProductsByCategory(category: String): Flow<List<Product>> {
        return dao.getProductsByCategory(category)
    }

    suspend fun toggleFavorite(product: Product) {
        dao.updateProduct(product.copy(isFavorite = !product.isFavorite))
    }

    suspend fun registerSearch(product: Product) {
        dao.updateProduct(
            product.copy(
                searchCount = product.searchCount + 1,
                lastSearchedAt = System.currentTimeMillis()
            )
        )
    }

    suspend fun insertProducts(products: List<Product>) {
        val existingProducts = dao.getAllProductsSync().associateBy { it.code }
        val updatedProducts = products.map { remote ->
            val local = existingProducts[remote.code]
            if (local != null) {
                remote.copy(
                    id = local.id,
                    isFavorite = local.isFavorite,
                    searchCount = local.searchCount,
                    lastSearchedAt = local.lastSearchedAt
                )
            } else {
                remote
            }
        }
        dao.insertProducts(updatedProducts)
    }
    suspend fun insertProduct(product: Product) {
        dao.insertProduct(product)
    }

    suspend fun updateProduct(product: Product) {
        dao.updateProduct(product)
    }

    suspend fun populateInitialDataIfNeeded() {

        // Force add new products if they don't exist
        val existing1 = dao.searchProductsSync("257806")
        if (existing1.isEmpty()) {
            dao.insertProducts(listOf(Product(code = "257806", name = "Pão Baguete com Queijo", searchName = "pao baguete com queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80")))
        }
        val existing2 = dao.searchProductsSync("257822")
        if (existing2.isEmpty()) {
            dao.insertProducts(listOf(Product(code = "257822", name = "Pão Delícia Trançada Queijo", searchName = "pao delicia trancada queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80")))
        }

        if (dao.getProductCount() == 0) {
            val initialProducts = listOf(
                Product(code = "1205", name = "Pão Francês", searchName = "pao frances", category = "Padaria", unit = "kg", searchCount = 100, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
                Product(code = "8563", name = "Banana Prata", searchName = "banana prata", category = "Hortifruti", unit = "kg", searchCount = 95, imageUrl = "https://images.unsplash.com/photo-1603833665858-e61d17a86224?auto=format&fit=crop&w=150&q=80"),
                Product(code = "8564", name = "Banana Nanica", searchName = "banana nanica", category = "Hortifruti", unit = "kg", searchCount = 50, imageUrl = "https://images.unsplash.com/photo-1603833665858-e61d17a86224?auto=format&fit=crop&w=150&q=80"),
                Product(code = "8565", name = "Banana Maçã", searchName = "banana maca", category = "Hortifruti", unit = "kg", searchCount = 40, imageUrl = "https://images.unsplash.com/photo-1603833665858-e61d17a86224?auto=format&fit=crop&w=150&q=80"),
                Product(code = "4512", name = "Mamão Formosa", searchName = "mamao formosa", category = "Hortifruti", unit = "un", searchCount = 90),
                Product(code = "3321", name = "Alface Crespa", searchName = "alface crespa", category = "Hortifruti", unit = "un", searchCount = 85),
                Product(code = "3322", name = "Alface Americana", searchName = "alface americana", category = "Hortifruti", unit = "un", searchCount = 80),
                Product(code = "7890", name = "Tomate Carmem", searchName = "tomate carmem", category = "Hortifruti", unit = "kg", searchCount = 88),
                Product(code = "7891", name = "Cebola Nacional", searchName = "cebola nacional", category = "Hortifruti", unit = "kg", searchCount = 87),
                Product(code = "2015", name = "Queijo Mussarela", searchName = "queijo mussarela", category = "Frios", unit = "kg", searchCount = 86),
                Product(code = "2016", name = "Mortadela Defumada", searchName = "mortadela defumada", category = "Frios", unit = "kg", searchCount = 84),
                Product(code = "1101", name = "Refrigerante Coca-Cola 2L", searchName = "refrigerante coca cola 2l", category = "Bebidas", unit = "un", searchCount = 30),
                Product(code = "5501", name = "Picanha Bovina", searchName = "picanha bovina carne", category = "Açougue", unit = "kg", searchCount = 45, imageUrl = "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=150&q=80"),
                
                
                Product(code = "257806", name = "Pão Baguete com Queijo", searchName = "pao baguete com queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
                Product(code = "257822", name = "Pão Delícia Trançada Queijo", searchName = "pao delicia trancada queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
                // Produtos da imagem
                Product(code = "254304", name = "Filé de Peito Bom Todo", searchName = "file peito frango bom todo", category = "Açougue", unit = "kg", searchCount = 10, imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254311", name = "Asa de Frango Bom Todo", searchName = "asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 9, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "256088", name = "Pé de Frango", searchName = "pe frango", category = "Açougue", unit = "kg", searchCount = 8, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254307", name = "Coração Bom Todo", searchName = "coracao frango bom todo", category = "Açougue", unit = "kg", searchCount = 7, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254306", name = "Moela de Frango Bom Todo", searchName = "moela frango bom todo", category = "Açougue", unit = "kg", searchCount = 6, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254297", name = "Sobrecoxa S/ Pele Bom Todo", searchName = "sobrecoxa sem pele frango bom todo", category = "Açougue", unit = "kg", searchCount = 5, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254331", name = "Coxa de Frango", searchName = "coxa frango", category = "Açougue", unit = "kg", searchCount = 4, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254308", name = "Filé de Sobrecoxa Bom Todo", searchName = "file sobrecoxa frango bom todo", category = "Açougue", unit = "kg", searchCount = 3, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254293", name = "Coxinha da Asa Bom Todo", searchName = "coxinha asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 2, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "256087", name = "Fígado de Frango", searchName = "figado frango", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "254305", name = "Meio da Asa Bom Todo", searchName = "meio asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
                Product(code = "256075", name = "Coxa/Sobrecoxa", searchName = "coxa sobrecoxa frango", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80")
            )
            dao.insertProducts(initialProducts)
        }
    }
}

fun String.unaccent(): String {
    val regex = "\\p{InCombiningDiacriticalMarks}+".toRegex()
    val temp = Normalizer.normalize(this, Normalizer.Form.NFD)
    return regex.replace(temp, "")
}

fun isTypoMatch(token: String, target: String): Boolean {
    if (token.length <= 2) return target.contains(token)
    
    val targetWords = target.split("\\s+".toRegex())
    return targetWords.any { word ->
        if (word.contains(token) || token.contains(word)) return@any true
        
        // Allow up to 1 typo for words of length 3-4, and 2 typos for longer words
        val allowedTypos = if (token.length <= 4) 1 else 2
        val distance = levenshtein(token, word)
        distance <= allowedTypos
    }
}

fun levenshtein(lhs: CharSequence, rhs: CharSequence): Int {
    if (lhs == rhs) return 0
    if (lhs.isEmpty()) return rhs.length
    if (rhs.isEmpty()) return lhs.length

    val lhsLength = lhs.length + 1
    val rhsLength = rhs.length + 1

    var cost = IntArray(lhsLength)
    var newCost = IntArray(lhsLength)

    for (i in 0 until lhsLength) cost[i] = i

    for (j in 1 until rhsLength) {
        newCost[0] = j
        for (i in 1 until lhsLength) {
            val match = if (lhs[i - 1] == rhs[j - 1]) 0 else 1
            val costReplace = cost[i - 1] + match
            val costInsert = cost[i] + 1
            val costDelete = newCost[i - 1] + 1
            newCost[i] = min(min(costInsert, costDelete), costReplace)
        }
        val swap = cost
        cost = newCost
        newCost = swap
    }
    return cost[lhsLength - 1]
}
