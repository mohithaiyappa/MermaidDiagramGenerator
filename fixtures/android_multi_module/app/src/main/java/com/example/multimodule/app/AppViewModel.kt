package com.example.multimodule.app

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.multimodule.feature.profile.ProfileRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class AppViewModel(
    private val repository: ProfileRepository,
    private val navigator: AppNavigator
) : ViewModel() {
    private val _isProfileVisible = MutableStateFlow(false)
    val isProfileVisible: StateFlow<Boolean> = _isProfileVisible

    fun loadProfile(userId: String) {
        viewModelScope.launch {
            val profile = repository.loadProfile(userId)
            _isProfileVisible.value = profile != null
            if (profile != null) {
                navigator.navigateTo("profile")
            }
        }
    }
}
