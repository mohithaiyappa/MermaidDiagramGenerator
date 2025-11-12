package com.example.multimodule.feature.profile

class ProfileValidator {
    fun validate(response: ProfileResponse) {
        require(response.displayName.isNotBlank()) { "Display name required" }
    }
}
