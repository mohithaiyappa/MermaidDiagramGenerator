package com.example.androidsample.data

import com.example.androidsample.model.User

class UserRepository {
    private val cache = mutableListOf<User>()

    fun getUsers(): List<User> = cache.toList()

    fun addUser(user: User) {
        cache.add(user)
    }
}
