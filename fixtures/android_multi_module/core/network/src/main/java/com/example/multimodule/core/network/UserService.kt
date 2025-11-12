package com.example.multimodule.core.network

class UserService(private val client: NetworkClient) {
    fun fetchUser(userId: String): String = client.get("/users/$userId")
}
