package com.example.multimodule.feature.profile

import com.example.multimodule.core.network.NetworkClient
import com.example.multimodule.core.network.NetworkConfig

class ProfileApi(
    private val client: NetworkClient = NetworkClient(NetworkConfig(baseUrl = "https://example.com"))
) {
    suspend fun loadProfile(userId: String): RawProfile {
        client.get("/users/$userId")
        return RawProfile(id = userId, firstName = "Ada", lastName = "Lovelace")
    }
}
