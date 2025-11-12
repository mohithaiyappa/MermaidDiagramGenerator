package com.example.multimodule.feature.profile

class ProfileLocalDataSource(private val preferences: ProfilePreferences) {
    private val cache = mutableMapOf<String, ProfileUiModel>()

    fun get(userId: String): ProfileUiModel? {
        return cache[userId] ?: preferences.restore(userId)
    }

    fun save(model: ProfileUiModel) {
        cache[model.id] = model
        preferences.persist(model)
    }
}
