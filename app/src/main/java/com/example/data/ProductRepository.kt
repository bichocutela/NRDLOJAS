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

    suspend fun getAllProductsSync() = dao.getAllProductsSync()

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
    suspend fun deleteProduct(product: Product) {
        dao.deleteProduct(product)
    }

    suspend fun deleteProducts(products: List<Product>) {
        dao.deleteProducts(products)
    }

    suspend fun insertProduct(product: Product) {
        dao.insertProduct(product)
        FirebaseService.saveProduct(product)
    }

    suspend fun updateProduct(product: Product) {
        dao.updateProduct(product)
        FirebaseService.saveProduct(product)
    }

    suspend fun populateInitialDataIfNeeded() {
        dao.deleteDuplicates()

        // Force add new products if they don't exist
        val imageProductsToForceAdd = listOf(
            Product(code = "255351", name = "Brioche de Creme", searchName = "bri creme pao doce", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255351-E", name = "Brioche Especial", searchName = "bri especial pao doce", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255351-L", name = "Brioche Leite Pó", searchName = "bri leite po pao doce", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
            Product(code = "250664", name = "Baguete", searchName = "baguete", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "250662", name = "Baguete com Gergelim", searchName = "baguete ger gergelim", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "250663", name = "Baguete Integral", searchName = "baguete inte integral", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "257806", name = "Pão Baguete com Queijo", searchName = "pao baguete com queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "257822", name = "Pão Delícia Trançada Queijo", searchName = "pao delicia trancada queijo", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255345", name = "Pão Parmesão Ervas", searchName = "pao parmesao ervas", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255475", name = "Pão Tomate Seco", searchName = "pao tomate seco", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255474", name = "Pão Azeitona", searchName = "pao azeitona", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255473", name = "Pão Gorgonzola", searchName = "pao gorgonzola", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "255476", name = "Pão Calabresa", searchName = "pao calabresa", category = "Padaria", unit = "un", searchCount = 0, imageUrl = "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254304", name = "Filé de Peito Bom Todo", searchName = "file peito frango bom todo", category = "Açougue", unit = "kg", searchCount = 10, imageUrl = "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254311", name = "Asa de Frango Bom Todo", searchName = "asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 9, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "256088", name = "Pé de Frango", searchName = "pe frango", category = "Açougue", unit = "kg", searchCount = 8, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254307", name = "Coração Bom Todo", searchName = "coracao frango bom todo", category = "Açougue", unit = "kg", searchCount = 7, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254306", name = "Moela de Frango Bom Todo", searchName = "moela frango bom todo", category = "Açougue", unit = "kg", searchCount = 6, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254297", name = "Sobrecoxa Sem Pele Bom Todo", searchName = "sobrecoxa sem pele frango bom todo", category = "Açougue", unit = "kg", searchCount = 5, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254331", name = "Coxa de Frango", searchName = "coxa frango", category = "Açougue", unit = "kg", searchCount = 4, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254308", name = "Filé de Sobrecoxa Bom Todo", searchName = "file sobrecoxa frango bom todo", category = "Açougue", unit = "kg", searchCount = 3, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254293", name = "Coxinha da Asa Bom Todo", searchName = "coxinha asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 2, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "256087", name = "Fígado de Frango", searchName = "figado frango", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "254305", name = "Meio da Asa Bom Todo", searchName = "meio asa frango bom todo", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80"),
            Product(code = "256075", name = "Coxa e Sobrecoxa de Frango", searchName = "coxa sobrecoxa frango", category = "Açougue", unit = "kg", searchCount = 1, imageUrl = "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?auto=format&fit=crop&w=150&q=80")
        ,
            Product(code = "250092", name = "ABACAXI DESC INTEIRO VACUO CFLV KG", searchName = "abacaxi desc inteiro vacuo cflv", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898366000139", name = "ABACAXI PREMIUM DOCE MEL UN", searchName = "abacaxi premium doce mel", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250094", name = "ABACAXI RODELAS VCO CFLV KG", searchName = "abacaxi rodelas vco cflv", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898366000092", name = "ABACAXI GOLD DOCE MEL", searchName = "abacaxi gold doce mel", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250098", name = "ABOBORA MORANGA KG", searchName = "abobora moranga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250104", name = "ACELGA KG", searchName = "acelga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898949599289", name = "AGRIAO UND", searchName = "agriao", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "254866", name = "ALCACHOFRA KG", searchName = "alcachofra", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898140981982", name = "ALHO PREMIUM", searchName = "alho premium", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251191", name = "ALECRIM UND", searchName = "alecrim", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7899090119609", name = "ALFACE AMERICANO PEDRA DE FOGO UND.", searchName = "alface americano pedra de fogo", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7899090119616", name = "ALFACE AMERICANA UN", searchName = "alface americana", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140981128", name = "ALFACE LISA HIDROPONICA UN", searchName = "alface lisa hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599333", name = "ALFACE LISA SEMPRE UND", searchName = "alface lisa sempre", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599340", name = "ALFACE MIMOSA UND", searchName = "alface mimosa", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "253975", name = "AMENDOIM JAPONES KG", searchName = "amendoim japones", category = "Mercearia", unit = "kg", searchCount = 0),
            Product(code = "251221", name = "ATEMOIA KG", searchName = "atemoia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252860", name = "BANANA MAÇA MELICIA", searchName = "banana maca melicia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250166", name = "BATATA APERITIVO KG", searchName = "batata aperitivo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250169", name = "BATATA IAKON KG", searchName = "batata iakon", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898929773623", name = "BATATA YACON 500G", searchName = "batata yacon", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140980114", name = "BROCOLIS HORTIFRIOS UN", searchName = "brocolis hortifrios", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250087", name = "CAMARAO KG", searchName = "camarao", category = "Peixaria", unit = "kg", searchCount = 0),
            Product(code = "251261", name = "CAQUI IMPORTADO KG", searchName = "caqui importado", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250279", name = "CAQUI RAMA FORTE KG", searchName = "caqui rama forte", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250281", name = "CARA PAULISTA KG", searchName = "cara paulista", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251262", name = "CARAMBOLA KG", searchName = "carambola", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252184", name = "CEREJA FRESCA", searchName = "cereja fresca", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254769", name = "CEBOLA IMPORTADA KG", searchName = "cebola importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254770", name = "CEBOLA BRANCA IMPORTADA KG", searchName = "cebola branca importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252762", name = "CEBOLA COLOSSAL KG", searchName = "cebola colossal", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "751320889027", name = "CEBOLINHA HIDROPONICA UN", searchName = "cebolinha hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251285", name = "CHICORIA HIDROPONICA UN", searchName = "chicoria hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250355", name = "COCO SECO KG", searchName = "coco seco", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898681940011", name = "COCO VERDE AQUACOCO DESC UND", searchName = "coco verde aquacoco desc", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251331", name = "COUVE FOLHA UN", searchName = "couve folha", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7751320889058", name = "ESPINAFRE HIDROPONICO UN", searchName = "espinafre hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250039", name = "FEIJAO VERDE DEBULHADO KG", searchName = "feijao verde debulhado", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250440", name = "GRAVIOLA KG", searchName = "graviola", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253417", name = "JABUTICABA KG", searchName = "jabuticaba", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250451", name = "JILO KG", searchName = "jilo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251484", name = "MANGA KEIT KG", searchName = "manga keit", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254455", name = "MAÇA CRIPPYS", searchName = "maca crippys", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7896304000012", name = "MACA NACIONAL TURMA MONICA PC 1KG", searchName = "maca nacional turma monica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250568", name = "MELANCIA BABY KG", searchName = "melancia baby", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250571", name = "MELANCIA CEPI KG IND", searchName = "melancia cepi ind", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252791", name = "MELANCIA PINGO DOCE KG", searchName = "melancia pingo doce", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250579", name = "MELAO CEPI KG", searchName = "melao cepi", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250574", name = "MELAO ESPANHOL FAMOSA REDINHA KG", searchName = "melao espanhol famosa redinha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252322", name = "MELÃO YELLORANGE MELUNA KG", searchName = "melao yellorange meluna", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250599", name = "MELAO REI REDINHA DOCE MEL KG", searchName = "melao rei redinha doce mel", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7804643270003", name = "MIRTILO 125G", searchName = "mirtilo", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599944", name = "MILHO VERDE BD 5 UNIDADES", searchName = "milho verde bd 5 unidades", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "252865", name = "MUDA DE ORQUÍDEA UM", searchName = "muda de orquidea", category = "Floricultura", unit = "un", searchCount = 0),
            Product(code = "7898949599517", name = "MOSTARDA", searchName = "mostarda", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140982118", name = "NABO HORTIFRIOS UND.", searchName = "nabo hortifrios", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250763", name = "PEPINO JAPONES SEMPRE VERDE KG", searchName = "pepino japones sempre verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250769", name = "PERA PACKAN`S", searchName = "pera packans", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254836", name = "CACAU KG", searchName = "cacau", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250774", name = "PERA WILLIAMS KG", searchName = "pera williams", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253650", name = "PIMENTA SERRANO VERDE KG", searchName = "pimenta serrano verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251613", name = "PIMENTÃO LARANJA KG", searchName = "pimentao laranja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "7898915681024", name = "PHYSALIS", searchName = "physalis", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250817", name = "PIMENTAO VERMELHO KG", searchName = "pimentao vermelho", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251615", name = "PINHAO KG", searchName = "pinhao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251025", name = "ROMA KG", searchName = "roma", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "751320518538", name = "RUCULA HIDROPONICA UN", searchName = "rucula hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251839", name = "SALSINHA HIDROPONICA RANCHO GRANDE", searchName = "salsinha hidroponica rancho grande", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251079", name = "SAPOTI KG", searchName = "sapoti", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250027", name = "TANGERINA MURCOTE KG", searchName = "tangerina murcote", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250018", name = "TANGERINA NACIONAL KG", searchName = "tangerina nacional", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250475", name = "TANGERINA PONKAN KG", searchName = "tangerina ponkan", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251137", name = "UVA BENITAKA KG", searchName = "uva benitaka", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251856", name = "UVA IMPORTADA RED GLOBE KG", searchName = "uva importada red globe", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "20222", name = "AGUA SANTA MARIA 20L PREMIUM", searchName = "agua santa maria 20l premium", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898049880225", name = "GARRAFÃO SANTA MARIA 20L PREMIUM", searchName = "garrafao santa maria 20l premium", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898049880287", name = "AGUA SANTA MARIA 20L PLUS", searchName = "agua santa maria 20l plus", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "20248", name = "GARRAFÃO SANTA MARIA 20L PLUS", searchName = "garrafao santa maria 20l plus", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065907067", name = "SACOLA NORDESTÃO 50 ANOS", searchName = "sacola nordestao 50 anos", category = "Bazar", unit = "un", searchCount = 0),
            Product(code = "7898065900600", name = "SUCO BETERRABA NORDESTÃO 500ML", searchName = "suco beterraba nordestao 500ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065902437", name = "SUCO DETOX NORDESTÃO 500ML", searchName = "suco detox nordestao 500ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065900617", name = "SUCO DE LARANJA 300ML", searchName = "suco de laranja 300ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065900662", name = "PIZZA ASSADA CALABRESA FAB PROPRIA", searchName = "pizza assada calabresa fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900655", name = "PIZZA ASSADA FRANGO FAB PROPRIA", searchName = "pizza assada frango fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900631", name = "PIZZA ASSADA SERTANEJA FAB PROPRIA", searchName = "pizza assada sertaneja fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900624", name = "PIZZA ASSADA PRESUNTO FAB PROPRIA", searchName = "pizza assada presunto fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900648", name = "PIZZA ASSADA PRESUNTO/CALABRESA FAB PROPRIA", searchName = "pizza assada presunto calabresa fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900679", name = "PIZZA ASSADA MUSSARELA FAB PROPRIA", searchName = "pizza assada mussarela fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "250682", name = "PÃO CEIA FAB PROPRIA", searchName = "pao ceia fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902154", name = "SALGADO FOLHADO QUEIJO FAB PROPRIA", searchName = "salgado folhado queijo fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902130", name = "SALGADO FOLHADO FRANGO FAB PROPRIA", searchName = "salgado folhado frango fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902147", name = "SALGADO FOLHADO PRESUNTO/QUEIJO FAB PROPRIA", searchName = "salgado folhado presunto queijo fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902161", name = "SALGADO FOLHADO SALSICHA FAB PROPRIA", searchName = "salgado folhado salsicha fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "251059", name = "SALGADO COXINHA FRANGO UND. FAB PROPRIA", searchName = "salgado coxinha frango und fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253365", name = "SALGADO COXINHA FRANGO/REQUEIJÃO FAB PROPRIA", searchName = "salgado coxinha frango requeijao fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253373", name = "SALGADO CARNE/REQUEIJÃO FAB PROPRIA", searchName = "salgado carne requeijao fab propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "000000202340", name = "CESTA BASICA SOLAR ALTAVISTA", searchName = "cesta basica solar altavista", category = "Mercearia", unit = "un", searchCount = 0),
            Product(code = "7896029094038", name = "WHISKAS CARNE 10.1KG", searchName = "whiskas carne 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029051833", name = "WHISKAS CARNE 3KG", searchName = "whiskas carne 3kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029051819", name = "WHISKAS PEIXE 3KG", searchName = "whiskas peixe 3kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029094069", name = "WHISKAS PEIXE 10.1KG", searchName = "whiskas peixe 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029043234", name = "WHISKAS CASTRADOS 1KG", searchName = "whiskas castrados 1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029043135", name = "WHISKAS CARNE 1KG", searchName = "whiskas carne 1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029043173", name = "WHISKAS FILHOTE CARNE 1KG", searchName = "whiskas filhote carne 1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045719", name = "PEDIGREE RAÇAS PEQUENAS 10.1KG", searchName = "pedigree racas pequenas 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045610", name = "PEDIGREE RAÇAS PEQUENAS 3KG", searchName = "pedigree racas pequenas 3kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045474", name = "PEDIGREE RAÇAS PEQUENAS 1KG", searchName = "pedigree racas pequenas 1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045702", name = "PEDIGREE FILHOTE 10.1KG", searchName = "pedigree filhote 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045665", name = "PEDIGREE ADULTO CARNE 10.1KG", searchName = "pedigree adulto carne 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045764", name = "PEDIGREE NUTRIÇÃO ESSENCIAL CARNE 10.1KG", searchName = "pedigree nutricao essencial carne 10.1kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029045634", name = "PEDIGREE ADULTO CARNE 3KG", searchName = "pedigree adulto carne 3kg", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029046754", name = "PEDIGREE SACHÊ FILHOTE CARNE 100G", searchName = "pedigree sache filhote carne 100g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029046730", name = "PEDIGREE SACHÊ RAÇAS PEQUENAS CARNE 100G", searchName = "pedigree sache racas pequenas carne 100g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029046808", name = "PEDIGREE SACHÊ ADULTO FRANGO 100G", searchName = "pedigree sache adulto frango 100g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029046747", name = "PEDIGREE SACHÊ ADULTO CARNE 100G", searchName = "pedigree sache adulto carne 100g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029037806", name = "PEDIGREE LATA CARNE 280G", searchName = "pedigree lata carne 280g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057866", name = "WHISKAS SACHÊ FILHOTE CARNE 85G", searchName = "whiskas sache filhote carne 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057859", name = "WHISKAS SACHÊ FILHOTE FRANGO 85G", searchName = "whiskas sache filhote frango 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057811", name = "WHISKAS SACHÊ ADULTO SALMÃO 85G", searchName = "whiskas sache adulto salmao 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057835", name = "WHISKAS SACHÊ ADULTO ATUM 85G", searchName = "whiskas sache adulto atum 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057842", name = "WHISKAS SACHÊ ADULTO FRANGO 85G", searchName = "whiskas sache adulto frango 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029057804", name = "WHISKAS SACHÊ ADULTO CARNE 85G", searchName = "whiskas sache adulto carne 85g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029051512", name = "WHISKAS LATA ADULTO ATUM 290G", searchName = "whiskas lata adulto atum 290g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "7896029051543", name = "WHISKAS LATA ADULTO SARDINHA 290G", searchName = "whiskas lata adulto sardinha 290g", category = "Pet Shop", unit = "un", searchCount = 0),
            Product(code = "0000000204110", name = "RACAO GATOS WHISKAS ADULT CARNE AG KG", searchName = "racao gatos whiskas adult carne ag kg", category = "Pet Shop", unit = "kg", searchCount = 0),
            Product(code = "0000000204130", name = "RACAO GATOS WHISKAS GATO CAST CAR AG KG", searchName = "racao gatos whiskas gato cast car ag kg", category = "Pet Shop", unit = "kg", searchCount = 0),
            Product(code = "0000000204170", name = "RACAO GATOS WHISKAS ADULT PEIXE AG KG", searchName = "racao gatos whiskas adult peixe ag kg", category = "Pet Shop", unit = "kg", searchCount = 0),
            Product(code = "0751320164551", name = "ABOBRINHA VERDE ORGANICO 1KG", searchName = "abobrinha verde organico 1kg", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599029", name = "ALFACE AMERICANA ORGANICA UN", searchName = "alface americana organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599036", name = "ALFACE CRESPA ORGANICA UN", searchName = "alface crespa organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599050", name = "ALFACE LISA ORGANICA UN", searchName = "alface lisa organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599067", name = "ALFACE MIMOSA ORGANICO UND", searchName = "alface mimosa organico und", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599043", name = "ALFACE ROXA ORGANICA UN", searchName = "alface roxa organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251234", name = "BANANA ORGANICA PACOVAN KG", searchName = "banana organica pacovan kg", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251235", name = "BATATA DOCE ORGANICA HORTAVIVA KG", searchName = "batata doce organica hortaviva kg", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "0751320164568", name = "BATATA DOCE ORGANICO 500G", searchName = "batata doce organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "0751320164629", name = "BETERRABA ORGANICO 500G", searchName = "beterraba organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "0751320888518", name = "CEBOLA ORGANICA 500G", searchName = "cebola organica 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599111", name = "CEBOLINHA ORGANICA UND", searchName = "cebolinha organica und", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133100", name = "CENOURA ORGANICO 600G", searchName = "cenoura organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133209", name = "CHUCHU ORGANICO 600G", searchName = "chuchu organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251291", name = "COENTRO ORGANICO UN", searchName = "coentro organico un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251332", name = "COUVE FOLHA ORGANICA UN", searchName = "couve folha organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "789894959166", name = "ESPINAFRE ORGANICO UN", searchName = "espinafre organico un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898910185121", name = "GOMA FRESCA DELICIA POTIGUAR ORGANICO", searchName = "goma fresca delicia potiguar organico", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "0751320164469", name = "GOIABA ORGANICA 500G", searchName = "goiaba organica 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599180", name = "HORTELA ORGANICO UND", searchName = "hortela organico und", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "253303", name = "MANGA ROSA ORGANICA KG", searchName = "manga rosa organica kg", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253282", name = "MAMAO FORMOSA ORGANICO", searchName = "mamao formosa organico", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253295", name = "MANGA TOMMY ORGANICA KG", searchName = "manga tommy organica kg", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251486", name = "MANJERICAO ORGANICO UND", searchName = "manjericao organico und", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2019355", name = "MILHO ORGANICO 600G", searchName = "milho organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "0751320164490", name = "PIMENTA CHEIRO ORGANICA 100G", searchName = "pimenta cheiro organica 100g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2017843", name = "PIMENTA CHEIRO ORGANICA 150G", searchName = "pimenta cheiro organica 150g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "0751320164513", name = "PIMENTA DEDO MOCA ORGANICA 200G", searchName = "pimenta dedo moca organica 200g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133247", name = "PIMENTAO VERDE ORGANICO 300G", searchName = "pimentao verde organico 300g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599210", name = "RUCULA ORGANICA UN", searchName = "rucula organica un", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599227", name = "SALSA ORGANICA MOLHO", searchName = "salsa organica molho", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "0751320164544", name = "TOMATE ORGANICO 500G", searchName = "tomate organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251008", name = "QUIABO HORTAVIVA", searchName = "quiabo hortaviva", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251094", name = "TOMATE CEREJA HORTAVIVA", searchName = "tomate cereja hortaviva", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250173", name = "BERINGELA HORTAVIVA", searchName = "beringela hortaviva", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "000000090513", name = "COLETE PROMOTOR TACTEL AZUL UND.", searchName = "colete promotor tactel azul und", category = "Promotores", unit = "un", searchCount = 0),
            Product(code = "7898065906053", name = "VALE REFEIÇÃO PROMOTOR", searchName = "vale refeicao promotor", category = "Promotores", unit = "un", searchCount = 0),
            Product(code = "7898065905964", name = "VALE DESJEJUM PROMOTOR", searchName = "vale desjejum promotor", category = "Promotores", unit = "un", searchCount = 0)
        )
        val importedProducts = listOf(
            Product(code = "2000290", name = "Cesta Basica Fabricação Própria N01", searchName = "cesta basica fabricacao propria n01", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2000291", name = "Cesta Basica Fabricação Própria N02", searchName = "cesta basica fabricacao propria n02", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2000292", name = "Cesta Basica Fabricação Própria N03", searchName = "cesta basica fabricacao propria n03", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2000293", name = "Cesta Basica Fabricação Própria Simas", searchName = "cesta basica fabricacao propria simas", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2000622", name = "Água Mineral Santa Maria Sem Gás Galão 10L", searchName = "agua mineral santa maria sem gas galao 10l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2000623", name = "Água Mineral Santa Maria Sem Gás Galão 20L", searchName = "agua mineral santa maria sem gas galao 20l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2000637", name = "Água Mineral Ster Bom Sem Gás Galão 10L", searchName = "agua mineral ster bom sem gas galao 10l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2000642", name = "Água Mineral Ster Bom Vasilhame 10L", searchName = "agua mineral ster bom vasilhame 10l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2000643", name = "Água Mineral Ster Bom Vasilhame 20L", searchName = "agua mineral ster bom vasilhame 20l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2004053", name = "Garrafão Pvc Indaia 20L Vasilhame Unidade", searchName = "garrafao pvc indaia 20l vasilhame", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2004054", name = "Garrafão Pvc Santa Maria 10L Unidade", searchName = "garrafao pvc santa maria 10l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2004055", name = "Garrafão Pvc Santa Maria Com Rosca 20L Unidade", searchName = "garrafao pvc santa maria com rosca 20l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2004056", name = "Garrafão Pvc Ster Bom 10L Unidade", searchName = "garrafao pvc ster bom 10l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2004057", name = "Garrafão Pvc Ster Bom 20L Unidade", searchName = "garrafao pvc ster bom 20l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "2014350", name = "Cesta Basica Fabricação Própria Produmar", searchName = "cesta basica fabricacao propria produmar", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014413", name = "Colete Promotor Tactel Az Unidade", searchName = "colete promotor tactel az", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2014600", name = "Cesta Natalina Ametista Fabricação Própria", searchName = "cesta natalina ametista fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014601", name = "Cesta Natalina Cristal Fabricação Própria", searchName = "cesta natalina cristal fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014602", name = "Cesta Natalina Esmeralda Fabricação Própria", searchName = "cesta natalina esmeralda fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014603", name = "Cesta Natalina Opala Fabricação Própria", searchName = "cesta natalina opala fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014604", name = "Cesta Natalina Perola Fabricação Própria", searchName = "cesta natalina perola fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014745", name = "Cesta Natalina Quartzo Fabricação Própria", searchName = "cesta natalina quartzo fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014746", name = "Cesta Natalina Rubi Fabricação Própria", searchName = "cesta natalina rubi fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014747", name = "Cesta Natalina Safira Fabricação Própria", searchName = "cesta natalina safira fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014748", name = "Cesta Natalina Topazio Fabricação Própria", searchName = "cesta natalina topazio fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2014749", name = "Cesta Natalina Turmalina Fabricação Própria", searchName = "cesta natalina turmalina fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2015182", name = "Cesta Natalina Quartzo 2 Fabricação Própria", searchName = "cesta natalina quartzo 2 fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2017738", name = "Cesta Natalina Quartzo S/F Fabricação Própria", searchName = "cesta natalina quartzo s/f fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2017739", name = "Cesta Natalina Turmalina S/F Fabricação Própria", searchName = "cesta natalina turmalina s/f fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2017795", name = "Cesta Natalina Cristal S/F Fabricação Própria", searchName = "cesta natalina cristal s/f fabricacao propria", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "2017843", name = "Pimenta Cheiro Organica 150G", searchName = "pimenta cheiro organica 150g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2019355", name = "Milho Organico 600G", searchName = "milho organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "20222", name = "Água Santa Maria 20L Premium", searchName = "agua santa maria 20l premium", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "202340", name = "Cesta Basica Solar Altavista", searchName = "cesta basica solar altavista", category = "Cestas", unit = "un", searchCount = 0),
            Product(code = "20248", name = "Garrafão Santa Maria 20L Plus", searchName = "garrafao santa maria 20l plus", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "204564", name = "Camarao Inteiro Congelado Camanor Ag Quilograma", searchName = "camarao inteiro congelado camanor ag", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "20575", name = "Melao Turma Da Monica", searchName = "melao turma da monica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2255428000004", name = "Pizza Quatro Queijos Ferm Natural 450G", searchName = "pizza quatro queijos ferm natural 450g", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "250001", name = "Laranja Pera Quilograma", searchName = "laranja pera", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250002", name = "Abacaxi Quilograma", searchName = "abacaxi", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250003", name = "Melancia Quilograma", searchName = "melancia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250004", name = "Cebola Branca Quilograma", searchName = "cebola branca", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250005", name = "Batata Inglesa Lisa Quilograma", searchName = "batata inglesa lisa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250006", name = "Macaxeira Quilograma", searchName = "macaxeira", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250008", name = "Tomate Santa Adelia Quilograma", searchName = "tomate santa adelia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250009", name = "Cenoura Quilograma", searchName = "cenoura", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250010", name = "Melao Japones Quilograma", searchName = "melao japones", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250011", name = "Tomate Longa Vida Quilograma", searchName = "tomate longa vida", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250015", name = "Chuchu Quilograma", searchName = "chuchu", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250016", name = "Limao Tahity Quilograma", searchName = "limao tahity", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250017", name = "Jerimum Leite Quilograma", searchName = "jerimum leite", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250018", name = "Tangerina Nacional Quilograma", searchName = "tangerina nacional", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250019", name = "Goiaba Quilograma", searchName = "goiaba", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250020", name = "Maracuja Quilograma", searchName = "maracuja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250021", name = "Pimentao Verde Quilograma", searchName = "pimentao verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250023", name = "Repolho Branco Quilograma", searchName = "repolho branco", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250024", name = "Cebola Roxa Quilograma", searchName = "cebola roxa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250027", name = "Tangerina Murcote Quilograma", searchName = "tangerina murcote", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250028", name = "Uva Italia Quilograma", searchName = "uva italia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250029", name = "Pera Danjou Importada Quilograma", searchName = "pera danjou importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250030", name = "Melao Espanhol Quilograma", searchName = "melao espanhol", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250031", name = "Manga Tommy Quilograma", searchName = "manga tommy", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250032", name = "Cara Sao Tome Quilograma", searchName = "cara sao tome", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250035", name = "Beterraba Quilograma", searchName = "beterraba", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250036", name = "Inhame Quilograma", searchName = "inhame", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250037", name = "Limao Comum Quilograma", searchName = "limao comum", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250038", name = "Laranja Mimo Quilograma", searchName = "laranja mimo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250039", name = "Feijao Verde Debulhado Quilograma", searchName = "feijao verde debulhado", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250040", name = "Caju Anao Precoce Quilograma", searchName = "caju anao precoce", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250041", name = "Kiwi Importado Quilograma", searchName = "kiwi importado", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250042", name = "Pepino Quilograma", searchName = "pepino", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250044", name = "Jerimum Caboclo Quilograma", searchName = "jerimum caboclo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250045", name = "Pera Portuguesa Quilograma", searchName = "pera portuguesa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250080", name = "Pão Frances Fabricação Própria Quilograma", searchName = "pao frances fabricacao propria", category = "Padaria", unit = "kg", searchCount = 0),
            Product(code = "250087", name = "Camarao Quilograma", searchName = "camarao", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "250092", name = "Abacaxi Descascado Inteiro Vacuo Central De Frutas Legumes E Verduras Quilograma", searchName = "abacaxi descascado inteiro vacuo central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250094", name = "Abacaxi Rodelas Vácuo Central De Frutas Legumes E Verduras Quilograma", searchName = "abacaxi rodelas vacuo central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250098", name = "Abobora Moranga Quilograma", searchName = "abobora moranga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250104", name = "Acelga Quilograma", searchName = "acelga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250166", name = "Batata Aperitivo Quilograma", searchName = "batata aperitivo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "2501660", name = "Batata Aperitivo Quilograma", searchName = "batata aperitivo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250169", name = "Batata Iakon Quilograma", searchName = "batata iakon", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250173", name = "Beringela Hortaviva", searchName = "beringela hortaviva", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250175", name = "Berinjela Quilograma", searchName = "berinjela", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250272", name = "Caja Quilograma", searchName = "caja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250279", name = "Caqui Rama Forte Quilograma", searchName = "caqui rama forte", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250281", name = "Cara Paulista Quilograma", searchName = "cara paulista", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250337", name = "Cebola Aperitivo Para Churrasco Quilograma", searchName = "cebola aperitivo para churrasco", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250341", name = "Cenoura Cubos Vácuo Central De Frutas Legumes E Verduras Quilograma", searchName = "cenoura cubos vacuo central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250343", name = "Cenoura Ralada Central De Frutas Legumes E Verduras Quilograma", searchName = "cenoura ralada central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250355", name = "Coco Seco Quilograma", searchName = "coco seco", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250374", name = "Couve Folha Fatiada Central De Frutas Legumes E Verduras Quilograma", searchName = "couve folha fatiada central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250390", name = "Endivia Branca Quilograma", searchName = "endivia branca", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250392", name = "Ervilha Torta Quilograma", searchName = "ervilha torta", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250437", name = "Gengibre Quilograma", searchName = "gengibre", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250440", name = "Graviola Quilograma", searchName = "graviola", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250447", name = "Jerimum Jacarezinho Quilograma", searchName = "jerimum jacarezinho", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250450", name = "Jerimum Leite Pedacos Central De Frutas Legumes E Verduras Vácuo Quilograma", searchName = "jerimum leite pedacos central de frutas legumes e verduras vacuo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250451", name = "Jilo Quilograma", searchName = "jilo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250470", name = "Lima Da Persia Quilograma", searchName = "lima da persia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250475", name = "Tangerina Ponkan Quilograma", searchName = "tangerina ponkan", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250518", name = "Maçã Importada Verde Quilograma", searchName = "maca importada verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250520", name = "Maçã Importada Vermelha Quilograma", searchName = "maca importada vermelha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250523", name = "Maçã Pink Lady Quilograma", searchName = "maca pink lady", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250527", name = "Mamão Formosa Quilograma", searchName = "mamao formosa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250541", name = "Mamão Partido Ao Meio Sem Casca Quilograma", searchName = "mamao partido ao meio sem casca", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250546", name = "Mandioquinha Quilograma", searchName = "mandioquinha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250548", name = "Manga Cubos Central De Frutas Legumes E Verduras Quilograma", searchName = "manga cubos central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250549", name = "Manga Espada Quilograma", searchName = "manga espada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250551", name = "Manga Palmer Quilograma", searchName = "manga palmer", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250553", name = "Manga Rosa Quilograma", searchName = "manga rosa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250559", name = "Maxixe Quilograma", searchName = "maxixe", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250568", name = "Melancia Baby Quilograma", searchName = "melancia baby", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250571", name = "Melancia Cepi Quilograma Individual", searchName = "melancia cepi individual", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250573", name = "Melao Amarelo Espanhol Sem Casca Fatiado Central De Frutas Legumes E Verduras Quilograma", searchName = "melao amarelo espanhol sem casca fatiado central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250574", name = "Melao Espanhol Famosa Redinha Quilograma", searchName = "melao espanhol famosa redinha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250577", name = "Melao Cantaloupe Quilograma", searchName = "melao cantaloupe", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250579", name = "Melao Cepi Quilograma", searchName = "melao cepi", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250581", name = "Melao Charentais Quilograma", searchName = "melao charentais", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250585", name = "Melao Galia Quilograma", searchName = "melao galia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250588", name = "Melao Japones Sem Casca Fatiado Central De Frutas Legumes E Verduras Quilograma", searchName = "melao japones sem casca fatiado central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250591", name = "Melao Orange Fresh Quilograma", searchName = "melao orange fresh", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250595", name = "Melao Portugues Quilograma", searchName = "melao portugues", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250599", name = "Melao Rei Redinha Doce Mel Quilograma", searchName = "melao rei redinha doce mel", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250662", name = "Baguete Gergelim", searchName = "baguete gergelim", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250663", name = "Baguete Integral", searchName = "baguete integral", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250664", name = "Baguete", searchName = "baguete", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2506740", name = "Pão Brioche Fabricação Própria Com Creme Quilograma", searchName = "pao brioche fabricacao propria com creme", category = "Padaria", unit = "kg", searchCount = 0),
            Product(code = "250682", name = "Pão Ceia Fabricação Própria", searchName = "pao ceia fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "250759", name = "Pepino Organico Quilograma", searchName = "pepino organico", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250763", name = "Pepino Japones Sempre Verde Quilograma", searchName = "pepino japones sempre verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250769", name = "Pera Packan'S", searchName = "pera packan's", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "250772", name = "Pera Red Quilograma", searchName = "pera red", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250774", name = "Pera Willians Quilograma", searchName = "pera willians", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250789", name = "Pessego Quilograma", searchName = "pessego", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250802", name = "Pimenta Biquinho Quilograma", searchName = "pimenta biquinho", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250806", name = "Pimenta De Cheiro Quilograma", searchName = "pimenta de cheiro", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250812", name = "Pimentao Amarelo Quilograma", searchName = "pimentao amarelo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250817", name = "Pimentao Vermelho Quilograma", searchName = "pimentao vermelho", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250819", name = "Pinha Quilograma", searchName = "pinha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250821", name = "Pitaya Quilograma", searchName = "pitaya", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "250827", name = "Polpa Maracuja Central De Frutas Legumes E Verduras Quilograma", searchName = "polpa maracuja central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251008", name = "Quiabo Hortaviva", searchName = "quiabo hortaviva", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251010", name = "Quiabo", searchName = "quiabo", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251017", name = "Repolho Roxo Quilograma", searchName = "repolho roxo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251025", name = "Roma Quilograma", searchName = "roma", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251028", name = "Salada 4 Cores Ralada Central De Frutas Legumes E Verduras Quilograma", searchName = "salada 4 cores ralada central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251029", name = "Salada De Frutas Central De Frutas Legumes E Verduras Quilograma", searchName = "salada de frutas central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251031", name = "Salada Vinagrete Central De Frutas Legumes E Verduras Quilograma", searchName = "salada vinagrete central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251059", name = "Salgado Coxinha Frango Unidade. Fabricação Própria", searchName = "salgado coxinha frango. fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "251069", name = "Salsao Branco Quilograma", searchName = "salsao branco", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251079", name = "Sapoti Quilograma", searchName = "sapoti", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251083", name = "Seleta Legumes Ralada Central De Frutas Legumes E Verduras Quilograma", searchName = "seleta legumes ralada central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251091", name = "Termo Funcionario", searchName = "termo funcionario", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251094", name = "Tomate Cereja Hortaviva", searchName = "tomate cereja hortaviva", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251096", name = "Tomate Grape Quilograma", searchName = "tomate grape", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251115", name = "Abacate Manteiga Quilograma", searchName = "abacate manteiga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251137", name = "Uva Benitaka Quilograma", searchName = "uva benitaka", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251139", name = "Uva Crimson Sem Semente Quilograma", searchName = "uva crimson sem semente", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251141", name = "Uva Isabel Quilograma", searchName = "uva isabel", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251153", name = "Vale Água Mineral Santa Maria 20L", searchName = "vale agua mineral santa maria 20l", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "251156", name = "Vale Gas Brasilgas", searchName = "vale gas brasilgas", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251160", name = "Vale Refeicao Promotor", searchName = "vale refeicao promotor", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251191", name = "Alecrim Unidade", searchName = "alecrim", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2512190", name = "Asa Frango Resfriado Quilograma", searchName = "asa frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "251221", name = "Atemoia Quilograma", searchName = "atemoia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251234", name = "Banana Organica Pacovan Quilograma", searchName = "banana organica pacovan", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251235", name = "Batata Doce Organica Hortaviva Quilograma", searchName = "batata doce organica hortaviva", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251261", name = "Caqui Importado Quilograma", searchName = "caqui importado", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251262", name = "Carambola Quilograma", searchName = "carambola", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251277", name = "Cebolinha Unidade", searchName = "cebolinha", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251278", name = "Cebolinha Organica Unidade", searchName = "cebolinha organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251285", name = "Chicoria Hidroponica Unidade", searchName = "chicoria hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251286", name = "Chicoria Organica Unidade", searchName = "chicoria organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251289", name = "Coco Verde Unidade", searchName = "coco verde", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251291", name = "Coentro Organico Unidade", searchName = "coentro organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251292", name = "Coentro Unidade", searchName = "coentro", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251293", name = "Coentro Hidroponico Unidade", searchName = "coentro hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251331", name = "Couve Folha Unidade", searchName = "couve folha", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251332", name = "Couve Folha Organica Unidade", searchName = "couve folha organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251333", name = "Couve Folha Hidropônico Unidade", searchName = "couve folha hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2513340", name = "Coxa Frango Resfriado Quilograma", searchName = "coxa frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "2513520", name = "Coxinha Asa Frango Resfriado Quilograma", searchName = "coxinha asa frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "251365", name = "Espinafre Organico Unidade", searchName = "espinafre organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251366", name = "Espinafre Unidade", searchName = "espinafre", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251367", name = "Fava Verde Quilograma", searchName = "fava verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "2513720", name = "Figado Frango Resfriado Quilograma", searchName = "figado frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "2513860", name = "File Peito Frango Resfriado Quilograma", searchName = "file peito frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "2513950", name = "File Sobrecoxa Frango Sem Pele Resfriado Quilograma", searchName = "file sobrecoxa frango sem pele resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "251432", name = "Hortela Unidade", searchName = "hortela", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251433", name = "Hortela Hidroponico Unidade", searchName = "hortela hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251483", name = "Manga Coite Quilograma", searchName = "manga coite", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251484", name = "Manga Keit Quilograma", searchName = "manga keit", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251486", name = "Manjericao Organico Unidade", searchName = "manjericao organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251487", name = "Manjericao Unidade", searchName = "manjericao", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251488", name = "Manjericao Hidroponico Unidade", searchName = "manjericao hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251490", name = "Mastruz Molho", searchName = "mastruz molho", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2514940", name = "Meio Da Asa Bom Todo Resfriado K G", searchName = "meio da asa bom todo resfriado k g", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251495", name = "Melancia Magali Turma Da Monica Quilograma", searchName = "melancia magali turma da monica", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251500", name = "Melao Dino Melicia Quilograma", searchName = "melao dino melicia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251543", name = "Nectarina Quilograma", searchName = "nectarina", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251611", name = "Pimenta Dedo De Moca Quilograma", searchName = "pimenta dedo de moca", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251613", name = "Pimentão Laranja Quilograma", searchName = "pimentao laranja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251615", name = "Pinhao Quilograma", searchName = "pinhao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251819", name = "Rucula Unidade", searchName = "rucula", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251820", name = "Rucula Organica Unidade", searchName = "rucula organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251822", name = "Salsa Unidade", searchName = "salsa", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251823", name = "Salsa Organica Molho", searchName = "salsa organica molho", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251839", name = "Salsinha Hidroponica Rancho Grande", searchName = "salsinha hidroponica rancho grande", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "251843", name = "Seriguela Quilograma", searchName = "seriguela", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "2518450", name = "Sobrecoxa Frango Resfriado Quilograma", searchName = "sobrecoxa frango resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "251851", name = "Tamarindo Quilograma", searchName = "tamarindo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251856", name = "Uva Importada Red Globe Quilograma", searchName = "uva importada red globe", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "251859", name = "Vagem Quilograma", searchName = "vagem", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252170", name = "Lichia Quilograma", searchName = "lichia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252184", name = "Cereja Fresca", searchName = "cereja fresca", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "252190", name = "Castanha Portuguesa Quilograma", searchName = "castanha portuguesa", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252244", name = "Grapefruit Quilograma", searchName = "grapefruit", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252322", name = "Melão Yellorange Meluna Quilograma", searchName = "melao yellorange meluna", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252605", name = "Limao Siciliano Quilograma", searchName = "limao siciliano", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252668", name = "Cenoura Inteiro Sem Casca Vácuo Central De Frutas Legumes E Verduras Quilograma", searchName = "cenoura inteiro sem casca vacuo central de frutas legumes e verduras", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252687", name = "Pera Asiatica Quilograma", searchName = "pera asiatica", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252742", name = "Goiaba Crocante Quilograma", searchName = "goiaba crocante", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252762", name = "Cebola Colossal Quilograma", searchName = "cebola colossal", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252791", name = "Melancia Pingo Doce Quilograma", searchName = "melancia pingo doce", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "252860", name = "Banana Maçã Melicia", searchName = "banana maca melicia", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "252865", name = "Muda De Orquídea Um", searchName = "muda de orquidea um", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "252956", name = "Coco Seco Partido Ao Meio Quilograma", searchName = "coco seco partido ao meio", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253056", name = "Tangerina Importada Bandeja Quilograma", searchName = "tangerina importada bandeja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253057", name = "Laranja Pera Bandeja Quilograma", searchName = "laranja pera bandeja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253070", name = "Grapefruit Bandeja Quilograma", searchName = "grapefruit bandeja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253071", name = "Cereja Bandeja Quilograma", searchName = "cereja bandeja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253280", name = "Salgado Folhado Fabricação Própria Queijo Unidade", searchName = "salgado folhado fabricacao propria queijo", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253281", name = "Salgado Folhado Fabricação Própria Frango Unidade", searchName = "salgado folhado fabricacao propria frango", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253282", name = "Mamão Formosa Organico", searchName = "mamao formosa organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "253295", name = "Manga Tommy Organica Quilograma", searchName = "manga tommy organica", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253303", name = "Manga Rosa Organica Quilograma", searchName = "manga rosa organica", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253365", name = "Salgado Coxinha Frango E Requeijão Fabricação Própria", searchName = "salgado coxinha frango e requeijao fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253370", name = "Pimenta Bico Doce Quilograma", searchName = "pimenta bico doce", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253373", name = "Salgado Carne E Requeijão Fabricação Própria", searchName = "salgado carne e requeijao fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "253395", name = "Pimenta Habanero Vermelha Quilograma", searchName = "pimenta habanero vermelha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253396", name = "Pimenta Jalapenos Quilograma", searchName = "pimenta jalapenos", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253408", name = "Pimenta Habanero Laranja Quilograma", searchName = "pimenta habanero laranja", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253409", name = "Pimenta Jolokia Quilograma", searchName = "pimenta jolokia", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253412", name = "Pimenta Habanero Amarela Quilograma", searchName = "pimenta habanero amarela", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253413", name = "Pimenta Habanero Chocolate Quilograma", searchName = "pimenta habanero chocolate", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253417", name = "Jabuticaba Quilograma", searchName = "jabuticaba", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253427", name = "Mix De Legumes Para Yakissoba Quilograma", searchName = "mix de legumes para yakissoba", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253626", name = "Cenoura E Beterraba Ralados Nordestão Quilograma", searchName = "cenoura e beterraba ralados nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253627", name = "Mamão Formosa Cubos Nordestão Quilograma", searchName = "mamao formosa cubos nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253636", name = "Mamão Formosa Ao Meio Nordestão Quilograma", searchName = "mamao formosa ao meio nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253638", name = "Mix De Repolhos Nordestão Quilograma", searchName = "mix de repolhos nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253640", name = "Pimenta Fildalga Quilograma", searchName = "pimenta fildalga", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253648", name = "Pimenta De Cheiro Ardida Quilograma", searchName = "pimenta de cheiro ardida", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253650", name = "Pimenta Serrano Verde Quilograma", searchName = "pimenta serrano verde", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253651", name = "Mix Para Molho Nordestão", searchName = "mix para molho nordestao", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "253652", name = "Batata E Cenoura Cubos Nordestão Quilograma", searchName = "batata e cenoura cubos nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253661", name = "Pimenta Bode Vermelha Quilograma", searchName = "pimenta bode vermelha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253662", name = "Batata Inglesa Cubos Nordestão Quilograma", searchName = "batata inglesa cubos nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253663", name = "Pimenta Bode Amarela Quilograma", searchName = "pimenta bode amarela", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253729", name = "Batata, Cenoura, Vagem E Abóbora Nordestão Quilograma", searchName = "batata, cenoura, vagem e abobora nordestao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253853", name = "Mamão Formosa Cubos Nordestão Pote Quilograma", searchName = "mamao formosa cubos nordestao pote", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253875", name = "Nozes Quilograma", searchName = "nozes", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253888", name = "Cupuacu Quilograma", searchName = "cupuacu", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "253975", name = "Amendoim Japones Quilograma", searchName = "amendoim japones", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254012", name = "Curcuma Acafrao Quilograma", searchName = "curcuma acafrao", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254014", name = "Milho Espanhol Pizza Quilograma", searchName = "milho espanhol pizza", category = "Padaria", unit = "kg", searchCount = 0),
            Product(code = "254134", name = "Taxa De Entrega Municipal", searchName = "taxa de entrega municipal", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "254220", name = "Taxa De Entrega Intermunicipal Ii", searchName = "taxa de entrega intermunicipal ii", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "254455", name = "Maçã Crippys", searchName = "maca crippys", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "254469", name = "Pão Italiano Fabricação Própria Quilograma", searchName = "pao italiano fabricacao propria", category = "Padaria", unit = "kg", searchCount = 0),
            Product(code = "254514", name = "Salada De Frutas Mamão/Manga/Abacaxi/Kiwi Quilograma", searchName = "salada de frutas mamao/manga/abacaxi/kiwi", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254526", name = "Salada De Frutas Mamão/Melão/Abacaxi/Uva Quilograma", searchName = "salada de frutas mamao/melao/abacaxi/uva", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254701", name = "Nabo Quilograma", searchName = "nabo", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254769", name = "Cebola Importada Quilograma", searchName = "cebola importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254835", name = "Maracuja Doce Quilograma", searchName = "maracuja doce", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254836", name = "Cacau Quilograma", searchName = "cacau", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254866", name = "Alcachofra Quilograma", searchName = "alcachofra", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254937", name = "Pitaya Amarela Importada Quilograma", searchName = "pitaya amarela importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254955", name = "Tomatinho Rama Trebeschi Quilograma", searchName = "tomatinho rama trebeschi", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254966", name = "Pimenta Jalapeno Vermelha Quilograma", searchName = "pimenta jalapeno vermelha", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "254967", name = "Limao Siciliano Nacional Quilograma", searchName = "limao siciliano nacional", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "255117", name = "Maçã Vermelha Gala Quilograma", searchName = "maca vermelha gala", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "255131", name = "Tangerina Importada Quilograma", searchName = "tangerina importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "255132", name = "Laranja Bahia Importada Quilograma", searchName = "laranja bahia importada", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "255345", name = "Parmesao Ervas", searchName = "parmesao ervas", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "255351", name = "Brioche Creme", searchName = "brioche creme", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "255373", name = "Pão Especial Fabricação Própria Quilograma", searchName = "pao especial fabricacao propria", category = "Padaria", unit = "kg", searchCount = 0),
            Product(code = "255383", name = "Jaca Quilograma Individual", searchName = "jaca individual", category = "Hortifruti", unit = "kg", searchCount = 0),
            Product(code = "255473", name = "Gorgonzola", searchName = "gorgonzola", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "255474", name = "Azeitona", searchName = "azeitona", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "255475", name = "Tomate Seco", searchName = "tomate seco", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "255476", name = "Calabresa", searchName = "calabresa", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "2557270", name = "Coxa/Sobre Frango Bom Todo R Esf Quilograma", searchName = "coxa/sobre frango bom todo r esf", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "2557280", name = "Pe Frango Bom Todo Resfriado Quilograma", searchName = "pe frango bom todo resfriado", category = "Açougue", unit = "kg", searchCount = 0),
            Product(code = "751320164469", name = "Goiaba Organica 500G", searchName = "goiaba organica 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164490", name = "Pimenta Cheiro Organica100G", searchName = "pimenta cheiro organica100g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164513", name = "Pimenta Dedo Moca Organica 200G", searchName = "pimenta dedo moca organica 200g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164544", name = "Tomate Organico 500G", searchName = "tomate organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164551", name = "Abobrinha Verde Organico 1Kg", searchName = "abobrinha verde organico 1kg", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164568", name = "Batata Doce Organico 500G", searchName = "batata doce organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320164629", name = "Beterraba Organico 500G", searchName = "beterraba organico 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320518538", name = "Rucula Hidroponica Unidade", searchName = "rucula hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320888518", name = "Cebola Organica 500G", searchName = "cebola organica 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "751320889027", name = "Cebolinha Hidroponica Unidade", searchName = "cebolinha hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7751320889058", name = "Espinafre Hidroponico Unidade", searchName = "espinafre hidroponico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7804643270003", name = "Mirtilo 125G", searchName = "mirtilo 125g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7896304000012", name = "Maçã Nacional Turma Monica Pacote 1Kg", searchName = "maca nacional turma monica pacote 1kg", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898049880225", name = "Garrafão Santa Maria 20L Premium", searchName = "garrafao santa maria 20l premium", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898049880287", name = "Água Santa Maria 20L Plus", searchName = "agua santa maria 20l plus", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065900600", name = "Suco Beterraba Nordestão 500Ml", searchName = "suco beterraba nordestao 500ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065900617", name = "Suco De Laranja 300Ml", searchName = "suco de laranja 300ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065900624", name = "Pizza Assada Presunto Fabricação Própria", searchName = "pizza assada presunto fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900631", name = "Pizza Assada Sertaneja Fabricação Própria", searchName = "pizza assada sertaneja fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900648", name = "Pizza Assada Presunto E Calabresa Fabricação Própria", searchName = "pizza assada presunto e calabresa fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900655", name = "Pizza Assada Frango Fabricação Própria", searchName = "pizza assada frango fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900662", name = "Pizza Assada Calabresa Fabricação Própria", searchName = "pizza assada calabresa fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065900679", name = "Pizza Asada Mussarela Fabricação Própria", searchName = "pizza asada mussarela fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902130", name = "Salgado Folhado Frango Fabricação Própria", searchName = "salgado folhado frango fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902147", name = "Salgado Folhado Presunto/Queijo Fabricação Própria", searchName = "salgado folhado presunto/queijo fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902154", name = "Salgado Folhado Queijo Fabricação Própria", searchName = "salgado folhado queijo fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902161", name = "Salgado Folhado Salsicha Fabricação Própria", searchName = "salgado folhado salsicha fabricacao propria", category = "Padaria", unit = "un", searchCount = 0),
            Product(code = "7898065902437", name = "Suco Detox Nordestão 500Ml", searchName = "suco detox nordestao 500ml", category = "Bebidas", unit = "un", searchCount = 0),
            Product(code = "7898065905964", name = "Vale Desjejum Promotor", searchName = "vale desjejum promotor", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898065906053", name = "Vale Refeição Promotor", searchName = "vale refeicao promotor", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898065907067", name = "Sacola Nordestão 50 Anos", searchName = "sacola nordestao 50 anos", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140980114", name = "Brocolis Hortifrios Unidade", searchName = "brocolis hortifrios", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140981128", name = "Alface Lisa Hidroponica Unidade", searchName = "alface lisa hidroponica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140981982", name = "Alho Premium", searchName = "alho premium", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898140982118", name = "Nabo Hortifrios Unidade.", searchName = "nabo hortifrios.", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898366000092", name = "Abacaxi Gold Doce Mel", searchName = "abacaxi gold doce mel", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898366000139", name = "Abacaxi Premium Doce Mel Unidade", searchName = "abacaxi premium doce mel", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898681940011", name = "Coco Verde Aquacoco Descascado Unidade", searchName = "coco verde aquacoco descascado", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898910185121", name = "Goma Fresca Delicia Potiguar Organico", searchName = "goma fresca delicia potiguar organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898915681024", name = "Physalis", searchName = "physalis", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898929773623", name = "Batata Yacon 500G", searchName = "batata yacon 500g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "789894959166", name = "Espinafre Organico Unidade", searchName = "espinafre organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599029", name = "Alface Americana Organica Unidade", searchName = "alface americana organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599036", name = "Alface Crespa Organica Unidade", searchName = "alface crespa organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599043", name = "Alface Roxa Organica Unidade", searchName = "alface roxa organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599050", name = "Alface Lisa Organica Unidade", searchName = "alface lisa organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599067", name = "Alface Mimosa Organico Unidade", searchName = "alface mimosa organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599111", name = "Cebolinha Organica Unidade", searchName = "cebolinha organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599180", name = "Hortela Organico Unidade", searchName = "hortela organico", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599210", name = "Rucula Organica Unidade", searchName = "rucula organica", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599227", name = "Salsa Organica Molho", searchName = "salsa organica molho", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599289", name = "Agriao Unidade", searchName = "agriao", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599333", name = "Alface Lisa Sempre Unidade", searchName = "alface lisa sempre", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599340", name = "Alface Mimosa Unidade", searchName = "alface mimosa", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599517", name = "Mostarda", searchName = "mostarda", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898949599944", name = "Milho Verde Bandeja 5 Unidades", searchName = "milho verde bandeja 5s", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133100", name = "Cenoura Organico 600G", searchName = "cenoura organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133209", name = "Chuchu Organico 600G", searchName = "chuchu organico 600g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7898963133247", name = "Pimentao Verde Organico 300G", searchName = "pimentao verde organico 300g", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "7899090119609", name = "Alface Americano Pedra De Fogo Unidade.", searchName = "alface americano pedra de fogo.", category = "Hortifruti", unit = "un", searchCount = 0),
            Product(code = "90513", name = "Colete Promotor Tactel Azul Unidade.", searchName = "colete promotor tactel azul.", category = "Hortifruti", unit = "un", searchCount = 0)
        )
        val allProductsToForceAdd = imageProductsToForceAdd + importedProducts
        val missingProducts = allProductsToForceAdd.filter { p -> 
            dao.searchProductsSync(p.code).none { it.name == p.name }
        }
        if (missingProducts.isNotEmpty()) {
            dao.insertProducts(missingProducts)
            // Removed FirebaseService.saveProduct(it) to prevent local defaults from overwriting remote
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
                Product(code = "5501", name = "Picanha Bovina", searchName = "picanha bovina carne", category = "Açougue", unit = "kg", searchCount = 45, imageUrl = "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=150&q=80")
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
