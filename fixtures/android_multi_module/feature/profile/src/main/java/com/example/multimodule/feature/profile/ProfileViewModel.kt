package com.example.multimodule.feature.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ProfileViewModel(
    private val repository: ProfileRepository,
    private val dispatcher: ProfileDispatcher,
    private val logger: ProfileLogger
) : ViewModel() {
    private val _state = MutableStateFlow(ProfileUiState(isLoading = true))
    val state: StateFlow<ProfileUiState> = _state

    fun load(userId: String) {
        viewModelScope.launch(dispatcher.main) {
            logger.log("Loading $userId")
            try {
                val profile = repository.loadProfile(userId)
                _state.value = ProfileUiState(displayName = profile.displayName)
            } catch (error: Throwable) {
                _state.value = ProfileUiState(errorMessage = error.message)
            }
        }
    }

    fun onFollowClicked() {
        logger.log("Follow clicked")
    }
}
