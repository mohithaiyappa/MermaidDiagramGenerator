package com.example.multimodule.core.network

class NetworkClient(private val config: NetworkConfig) {
    fun get(url: String): String = "GET $url with ${config.userAgent}"
    fun post(url: String, body: String): String = "POST $url with body length ${body.length}"
}
