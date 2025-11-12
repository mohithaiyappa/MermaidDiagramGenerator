package com.example.multimodule.app

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class AppNavigator {
    private val _destination = MutableStateFlow("home")
    val destination: StateFlow<String> = _destination

    fun navigateTo(route: String) {
        _destination.value = route
    }
}
