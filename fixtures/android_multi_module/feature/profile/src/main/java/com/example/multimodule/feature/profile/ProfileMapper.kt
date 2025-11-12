package com.example.multimodule.feature.profile

class ProfileMapper(
    private val validator: ProfileValidator,
    private val analytics: ProfileAnalytics
) {
    fun map(response: ProfileResponse): ProfileUiModel {
        validator.validate(response)
        val uiModel = ProfileUiModel(
            id = response.id,
            displayName = response.displayName,
            email = response.email
        )
        analytics.trackLoaded(uiModel)
        return uiModel
    }
}
