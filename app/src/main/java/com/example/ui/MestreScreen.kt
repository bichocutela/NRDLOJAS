package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.ColorLens
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.ViewCarousel
import androidx.compose.material.icons.filled.Inventory
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MestreScreen(
    viewModel: MainViewModel, 
    onNavigateToAdmin: () -> Unit,
    onNavigateToManageTabs: () -> Unit,
    onNavigateToManageProducts: () -> Unit,
    onNavigateBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Painel Mestre", color = MaterialTheme.colorScheme.primary) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Voltar"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(Icons.Default.Build, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Bem-vindo ao Painel Mestre", style = MaterialTheme.typography.headlineMedium, textAlign = TextAlign.Center)
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                "Aqui você tem controle total. Algumas configurações são feitas na interface e outras profundamente estruturais são feitas solicitando à IA.",
                textAlign = TextAlign.Center,
                style = MaterialTheme.typography.bodyMedium
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            OutlinedCard(
                modifier = Modifier.fillMaxWidth(),
                onClick = onNavigateToManageTabs
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.ViewCarousel, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Gerenciar Abas (Painel Mestre)", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text("Criar, editar, excluir ou reordenar abas de texto, imagem e vídeo.", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedCard(
                modifier = Modifier.fillMaxWidth(),
                onClick = onNavigateToManageProducts
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Inventory, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Editar Produtos Existentes", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text("Modificar código, foto e nome de produtos da base.", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedCard(
                modifier = Modifier.fillMaxWidth(),
                onClick = onNavigateToAdmin
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Build, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text("Adicionar Novos Produtos (IA)", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text("Adicionar usando Gemini ou manualmente.", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(16.dp))
            
            Text("Edições Estruturais (Via IA)", style = MaterialTheme.typography.titleMedium, modifier = Modifier.align(Alignment.Start))
            Spacer(modifier = Modifier.height(8.dp))
            
            InfoCard(
                icon = Icons.Default.ViewCarousel,
                title = "Adicionar Novas Abas",
                description = "Peça ao assistente no chat: 'Crie uma nova aba chamada X com a função Y'."
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            InfoCard(
                icon = Icons.Default.ColorLens,
                title = "Fundo e Tema do App",
                description = "Peça ao assistente no chat: 'Altere a cor de fundo para Z e o tema para escuro'."
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            InfoCard(
                icon = Icons.Default.Code,
                title = "Edição de Código e Textos",
                description = "Peça ao assistente no chat: 'Modifique o texto na tela inicial' ou 'Altere o comportamento do código'."
            )
        }
    }
}

@Composable
fun InfoCard(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, description: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(24.dp))
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(title, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(description, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
