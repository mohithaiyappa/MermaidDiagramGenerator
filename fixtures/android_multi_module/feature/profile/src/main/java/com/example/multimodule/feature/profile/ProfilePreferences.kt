package com.example.multimodule.feature.profile

class ProfilePreferences {
    private val persisted = mutableMapOf<String, ProfileUiModel>()

    fun restore(userId: String): ProfileUiModel? = persisted[userId]

    fun persist(model: ProfileUiModel) {
        persisted[model.id] = model
    }
}
