package com.agentlens.benchmark

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

// LEGACY CODE: Anti-pattern multiple exposed mutable states
class UserProfileViewModel {
    var name: String = ""
        private set
    var email: String = ""
        private set
    var isLoading: Boolean = false
        private set
    var errorMessage: String? = null
        private set

    // Needs to be replaced with a single StateFlow<UserProfileUiState>
    val _state = MutableStateFlow<String>("")
    val state: StateFlow<String> = _state

    fun fetchUserData(userId: String) {
        isLoading = true
        if (userId.isEmpty()) {
            errorMessage = "Invalid User ID"
            isLoading = false
            return
        }
        name = "Developer $userId"
        email = "dev_$userId@agentlens.ai"
        isLoading = false
    }
}
