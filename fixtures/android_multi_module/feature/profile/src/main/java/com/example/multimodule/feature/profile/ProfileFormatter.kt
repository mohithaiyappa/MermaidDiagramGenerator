package com.example.multimodule.feature.profile

class ProfileFormatter {
    fun formatResponse(response: RawProfile): ProfileResponse {
        return ProfileResponse(
            id = response.id,
            displayName = "${response.firstName} ${response.lastName}",
            email = "${response.id}@example.com"
        )
    }
}
