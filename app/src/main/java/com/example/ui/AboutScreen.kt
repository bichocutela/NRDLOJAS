package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.text.ClickableText

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen(onNavigateBack: () -> Unit) {
    val uriHandler = LocalUriHandler.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Sobre") },
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
                .padding(16.dp)
        ) {
            Text(
                text = "Sobre o Aplicativo\n\nEste aplicativo foi desenvolvido por Alessandro P., Operador de Caixa, com o objetivo de auxiliar os colaboradores da Frente de Loja na consulta rápida de códigos correlatos, contribuindo para mais agilidade, precisão e eficiência no atendimento aos clientes.\n\nEste projeto nasceu da vivência diária na operação de caixa e da necessidade de tornar a rotina de trabalho mais prática, oferecendo uma ferramenta de apoio aos profissionais da equipe.\n\nRegistro meu sincero agradecimento aos Fiscais de Caixa, pela confiança, incentivo e apoio durante o desenvolvimento desta iniciativa, bem como aos colegas de trabalho, que compartilharam sugestões, experiências e conhecimentos que contribuíram para o aprimoramento do aplicativo.\n\nEste aplicativo foi desenvolvido exclusivamente como uma ferramenta de apoio operacional interno e não substitui os procedimentos, normas, orientações ou sistemas oficiais da empresa.\n\nTodas as marcas, nomes, logotipos, códigos, informações e demais conteúdos relacionados ao Supermercado Nordestão pertencem aos seus respectivos proprietários. Todos os direitos são reservados à empresa. O desenvolvedor não reivindica qualquer direito de propriedade sobre essas informações, utilizando-as unicamente para fins de apoio às atividades internas dos colaboradores.\n\n© 2026 Alessandro P. Todos os direitos do aplicativo são reservados ao autor. O conteúdo institucional e as informações pertencentes ao Supermercado Nordestão permanecem de propriedade exclusiva da empresa.\n\nVersão: 1.0\nDesenvolvedor: Alessandro Paulo\n@bichocutela @haydendanex",
                style = MaterialTheme.typography.bodyMedium
            )

            Spacer(modifier = Modifier.height(16.dp))
            
            LinkText(
                text = "Site: ",
                linkText = "https://www.nordestaomaisvoce.com.br/",
                url = "https://www.nordestaomaisvoce.com.br/",
                uriHandler = uriHandler
            )
            
            LinkText(
                text = "App Nossa Gente: ",
                linkText = "https://app.nordestao.com.br/",
                url = "https://app.nordestao.com.br/",
                uriHandler = uriHandler
            )
            
            LinkText(
                text = "Nordestão Pra Você: ",
                linkText = "https://pravoce.nordestao.com.br/home",
                url = "https://pravoce.nordestao.com.br/home",
                uriHandler = uriHandler
            )
            
            LinkText(
                text = "Encarte: ",
                linkText = "https://pravoce.nordestao.com.br/tabloids",
                url = "https://pravoce.nordestao.com.br/tabloids",
                uriHandler = uriHandler
            )
        }
    }
}

@Composable
fun LinkText(text: String, linkText: String, url: String, uriHandler: androidx.compose.ui.platform.UriHandler) {
    val annotatedString = buildAnnotatedString {
        withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.onBackground)) {
            append(text)
        }
        pushStringAnnotation(tag = "URL", annotation = url)
        withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary, textDecoration = TextDecoration.Underline, fontWeight = FontWeight.Bold)) {
            append(linkText)
        }
        pop()
    }

    ClickableText(
        text = annotatedString,
        style = MaterialTheme.typography.bodyMedium,
        onClick = { offset ->
            annotatedString.getStringAnnotations(tag = "URL", start = offset, end = offset)
                .firstOrNull()?.let { annotation ->
                    uriHandler.openUri(annotation.item)
                }
        },
        modifier = Modifier.padding(vertical = 4.dp)
    )
}
