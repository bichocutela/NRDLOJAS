import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# find the dashboard lazycolumn end
old_code = """                                MiniProductCard(product, viewModel)
                            }
                        }
                    }
                }
                if (history.isNotEmpty()) {"""
new_code = """                                MiniProductCard(product, viewModel)
                            }
                        }
                    }
                }
                if (history.isNotEmpty()) {"""
# Actually, I can just inject an item at the end of the dashboard LazyColumn
footer_item = """                    item {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 32.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                "Feito com muito amor, para a frente de loja",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Icon(
                                imageVector = Icons.Default.Favorite,
                                contentDescription = "Amor",
                                tint = Color.Red,
                                modifier = Modifier.size(24.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}"""
# Let's use regex to find the end of the dashboard LazyColumn
# It ends with:
#                 if (history.isNotEmpty()) {
#                     item {
#                         SectionHeader("Histórico")
#                         Column(
#                             modifier = Modifier.padding(horizontal = 16.dp),
#                             verticalArrangement = Arrangement.spacedBy(12.dp)
#                         ) {
#                             history.forEach { product ->
#                                 HistoryItem(product, viewModel)
#                             }
#                         }
#                     }
#                 }
#             }
#         }

content = re.sub(
    r'(history\.forEach \{ product ->\n\s*HistoryItem\(product, viewModel\)\n\s*\}\n\s*\}\n\s*\}\n\s*\}\n\s*)(\}\n\s*\})',
    r'\1    item { Column(modifier=Modifier.fillMaxWidth().padding(32.dp), horizontalAlignment=Alignment.CenterHorizontally) { androidx.compose.material3.Text("Feito com muito amor, para a frente de loja", style=MaterialTheme.typography.bodyMedium, color=MaterialTheme.colorScheme.onSurfaceVariant); Spacer(modifier=Modifier.height(8.dp)); Icon(imageVector=Icons.Default.Favorite, contentDescription="Amor", tint=Color.Red, modifier=Modifier.size(24.dp)) } }\n\2',
    content
)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
