package com.example.multimodule.feature.profile

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class ProfileDispatcher(
    val main: CoroutineDispatcher = Dispatchers.Main,
    private val io: CoroutineDispatcher = Dispatchers.IO
) {
    fun launchBackground(block: suspend CoroutineScope.() -> Unit) {
        CoroutineScope(io).launch(block = block)
    }
}
