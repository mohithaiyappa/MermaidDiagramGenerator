package com.example.multimodule.feature.profile

class ProfileAnalytics(private val dispatcher: ProfileDispatcher) {
    fun trackLoaded(model: ProfileUiModel) {
        dispatcher.launchBackground {
            // pretend to send analytics
        }
    }
}
