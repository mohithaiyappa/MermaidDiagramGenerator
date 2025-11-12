package com.example.multimodule.feature.profile

sealed interface ProfileAction {
    data class Load(val userId: String) : ProfileAction
    data object Follow : ProfileAction
}
