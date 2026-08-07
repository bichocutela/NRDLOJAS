#!/bin/bash
sed -i 's/_syncMessage.emit("Aviso: Nuvem não configurada. Impossível sincronizar.")/val msg = com.example.data.FirebaseService.lastError ?: "Configuração ausente."\n                    _syncMessage.emit("Nuvem não configurada: $msg")/g' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i 's/_syncMessage.emit("Aviso: Nuvem não configurada. Nenhum produto baixado.")/val msg = com.example.data.FirebaseService.lastError ?: "Configuração ausente."\n                _syncMessage.emit("Nuvem não configurada: $msg")/g' app/src/main/java/com/example/ui/MainViewModel.kt
