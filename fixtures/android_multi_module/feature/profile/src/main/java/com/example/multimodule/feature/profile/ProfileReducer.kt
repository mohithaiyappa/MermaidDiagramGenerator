package com.example.multimodule.feature.profile

class ProfileReducer {
    fun reduce(state: ProfileUiState, event: ProfileEvent): ProfileUiState {
        return when (event) {
            is ProfileEvent.FollowClicked -> state
            is ProfileEvent.ProfileLoaded -> state.copy(
                isLoading = false,
                displayName = event.model.displayName,
                errorMessage = null
            )
        }
    }
}
