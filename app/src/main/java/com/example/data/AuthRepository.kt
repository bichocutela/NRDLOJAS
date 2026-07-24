package com.example.data

import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.FirebaseApp
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.tasks.await

class AuthRepository {
    private val _authState = MutableStateFlow<AuthState>(AuthState.Initial)
    val authState: StateFlow<AuthState> = _authState

    val isConfigured: Boolean
        get() = try {
            FirebaseApp.getInstance()
            true
        } catch (e: Exception) {
            false
        }

    suspend fun login(email: String, pass: String): AuthResult {
        if (!isConfigured) return AuthResult.Error("Firebase não configurado. Adicione o google-services.json.")
        
        return try {
            _authState.value = AuthState.Loading
            val auth = FirebaseAuth.getInstance()
            val result = auth.signInWithEmailAndPassword(email, pass).await()
            _authState.value = AuthState.Authenticated(result.user?.email ?: "")
            AuthResult.Success(result.user?.email ?: "")
        } catch (e: Exception) {
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(e.message ?: "Erro desconhecido ao fazer login")
        }
    }
    
    suspend fun createAccount(email: String, pass: String): AuthResult {
         if (!isConfigured) return AuthResult.Error("Firebase não configurado.")
         
         return try {
            _authState.value = AuthState.Loading
            val auth = FirebaseAuth.getInstance()
            val result = auth.createUserWithEmailAndPassword(email, pass).await()
            _authState.value = AuthState.Authenticated(result.user?.email ?: "")
            AuthResult.Success(result.user?.email ?: "")
        } catch (e: Exception) {
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(e.message ?: "Erro desconhecido ao criar conta")
        }
    }

    fun logout() {
        if (isConfigured) {
            FirebaseAuth.getInstance().signOut()
        }
        _authState.value = AuthState.Unauthenticated
    }
}

sealed class AuthState {
    object Initial : AuthState()
    object Loading : AuthState()
    data class Authenticated(val email: String) : AuthState()
    object Unauthenticated : AuthState()
}

sealed class AuthResult {
    data class Success(val email: String) : AuthResult()
    data class Error(val message: String) : AuthResult()
}
