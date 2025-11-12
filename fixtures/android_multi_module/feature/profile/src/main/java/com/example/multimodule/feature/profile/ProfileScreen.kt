package com.example.multimodule.feature.profile

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.material3.Text
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Button

@Composable
fun ProfileScreen(userId: String, viewModel: ProfileViewModel = defaultProfileViewModel()) {
    val state by viewModel.state.collectAsState()
    Column {
        Text(text = "Viewing profile $userId")
        if (state.isLoading) {
            Text(text = "Loading...")
        } else {
            Text(text = state.displayName)
        }
        Button(onClick = { viewModel.onFollowClicked() }) {
            Text(text = "Follow")
        }
    }
}

fun defaultProfileViewModel(): ProfileViewModel {
    val dispatcher = ProfileDispatcher()
    val repository = ProfileRepository(
        remoteDataSource = ProfileRemoteDataSource(ProfileService(ProfileApi(), ProfileFormatter())),
        localDataSource = ProfileLocalDataSource(ProfilePreferences()),
        mapper = ProfileMapper(ProfileValidator(), ProfileAnalytics(dispatcher))
    )
    return ProfileViewModel(repository, dispatcher, ProfileLogger())
}
