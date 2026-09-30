package com.agentlens.benchmark

// Target state representation that the agent must implement
data class UserProfileUiState(
    val name: String = "",
    val email: String = "",
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)
