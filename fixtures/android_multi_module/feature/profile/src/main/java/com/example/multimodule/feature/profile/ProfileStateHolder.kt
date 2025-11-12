package com.example.multimodule.feature.profile

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class ProfileStateHolder(initialState: ProfileUiState = ProfileUiState()) {
    private val reducer = ProfileReducer()
    private val _state = MutableStateFlow(initialState)
    val state: StateFlow<ProfileUiState> = _state

    fun dispatch(event: ProfileEvent) {
        _state.value = reducer.reduce(_state.value, event)
    }
}
