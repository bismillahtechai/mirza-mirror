package com.mirzamirror.app.model

import java.util.Date
import java.util.UUID

/**
 * Data model for a Thought
 */
data class Thought(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val source: String,
    val createdAt: Date,
    val updatedAt: Date,
    val audioFile: String? = null,
    val documentFile: String? = null,
    val summary: String? = null,
    val tags: List<Tag> = emptyList(),
    val links: List<Link> = emptyList(),
    val actions: List<Action> = emptyList()
)

/**
 * Data model for a Tag
 */
data class Tag(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
    val type: String,
    val confidence: Float? = null
)

/**
 * Data model for a Link between thoughts
 */
data class Link(
    val id: String = UUID.randomUUID().toString(),
    val sourceThoughtId: String,
    val targetThoughtId: String,
    val relationship: String,
    val strength: Float
)

/**
 * Data model for an Action extracted from a thought
 */
data class Action(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val priority: String,
    val dueDate: String? = null,
    val completed: Boolean = false
)

/**
 * Data model for a Document
 */
data class Document(
    val id: String = UUID.randomUUID().toString(),
    val filePath: String,
    val content: String? = null,
    val contentType: String,
    val createdAt: Date,
    val updatedAt: Date
)
