package com.example.multimodule.feature.profile

class ProfileRepository(
    private val remoteDataSource: ProfileRemoteDataSource,
    private val localDataSource: ProfileLocalDataSource,
    private val mapper: ProfileMapper
) {
    suspend fun loadProfile(userId: String): ProfileUiModel {
        val cached = localDataSource.get(userId)
        if (cached != null) {
            return cached
        }
        val remote = remoteDataSource.fetch(userId)
        val mapped = mapper.map(remote)
        localDataSource.save(mapped)
        return mapped
    }
}
