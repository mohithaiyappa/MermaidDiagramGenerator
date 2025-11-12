package com.example.multimodule.feature.profile

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

class ProfileStateMachine(
    private val repository: ProfileRepository,
    private val scope: CoroutineScope,
    private val stateHolder: ProfileStateHolder
) {
    fun dispatch(action: ProfileAction) {
        when (action) {
            is ProfileAction.Load -> load(action.userId)
            ProfileAction.Follow -> stateHolder.dispatch(ProfileEvent.FollowClicked)
        }
    }

    private fun load(userId: String) {
        scope.launch {
            val model = repository.loadProfile(userId)
            stateHolder.dispatch(ProfileEvent.ProfileLoaded(model))
        }
    }
}
