package com.example.multimodule.feature.profile

sealed interface ProfileEvent {
    data object FollowClicked : ProfileEvent
    data class ProfileLoaded(val model: ProfileUiModel) : ProfileEvent
}
