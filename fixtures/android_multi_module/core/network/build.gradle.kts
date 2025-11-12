plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.multimodule.core.network"
    compileSdk = 34

    defaultConfig {
        minSdk = 24
    }
}
