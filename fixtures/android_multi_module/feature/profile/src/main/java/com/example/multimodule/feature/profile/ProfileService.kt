package com.example.multimodule.feature.profile

class ProfileService(
    private val api: ProfileApi,
    private val formatter: ProfileFormatter
) {
    suspend fun fetchProfile(userId: String): ProfileResponse {
        val response = api.loadProfile(userId)
        return formatter.formatResponse(response)
    }
}
