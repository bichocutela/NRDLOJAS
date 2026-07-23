with open("app/src/main/java/com/example/ui/MainViewModel.kt", "r") as f:
    content = f.read()

replacement = """
    val dynamicTabs: kotlinx.coroutines.flow.StateFlow<List<com.example.data.DynamicTab>> = repository.getAllTabs()
        .stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.WhileSubscribed(5000), emptyList())

    fun insertTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.insertTab(tab) }
    fun updateTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.updateTab(tab) }
    fun deleteTab(tab: com.example.data.DynamicTab) = viewModelScope.launch { repository.deleteTab(tab) }
}"""

content = content.replace("\n}", replacement, 1)

with open("app/src/main/java/com/example/ui/MainViewModel.kt", "w") as f:
    f.write(content)
