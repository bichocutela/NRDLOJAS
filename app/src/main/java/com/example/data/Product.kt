package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class Product(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val code: String,
    val name: String,
    val searchName: String,
    val category: String,
    val isFavorite: Boolean = false,
    val searchCount: Int = 0,
    val lastSearchedAt: Long = 0,
    val unit: String = "un",
    val imageUrl: String? = null
)
