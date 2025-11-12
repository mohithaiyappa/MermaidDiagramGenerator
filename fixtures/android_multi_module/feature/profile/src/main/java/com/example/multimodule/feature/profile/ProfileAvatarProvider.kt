package com.example.multimodule.feature.profile

class ProfileAvatarProvider {
    fun buildAvatarUrl(userId: String): String = "https://example.com/avatar/$userId.png"
}
