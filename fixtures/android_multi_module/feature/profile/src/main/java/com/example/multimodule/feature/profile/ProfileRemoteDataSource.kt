package com.example.multimodule.feature.profile

class ProfileRemoteDataSource(private val service: ProfileService) {
    suspend fun fetch(userId: String): ProfileResponse {
        return service.fetchProfile(userId)
    }
}
