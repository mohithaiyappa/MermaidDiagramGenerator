package com.example.multimodule.app

import kotlinx.coroutines.flow.StateFlow

class AppState(
    val navigator: AppNavigator,
    private val profileState: StateFlow<Boolean>
) {
    fun shouldShowProfile(): Boolean = profileState.value
}
