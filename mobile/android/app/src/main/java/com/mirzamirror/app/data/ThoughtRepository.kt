package com.mirzamirror.app.data

import com.mirzamirror.app.model.Thought
import com.mirzamirror.app.network.ApiRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository for Thought data
 */
@Singleton
class ThoughtRepository @Inject constructor(
    private val apiRepository: ApiRepository
) {
    // State flows for UI
    private val _thoughts = MutableStateFlow<List<Thought>>(emptyList())
    val thoughts: StateFlow<List<Thought>> = _thoughts.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()
    
    suspend fun fetchThoughts() {
        _isLoading.value = true
        _error.value = null
        
        apiRepository.getThoughts()
            .onSuccess { thoughtsList ->
                _thoughts.value = thoughtsList
                _isLoading.value = false
            }
            .onFailure { exception ->
                _error.value = exception.message
                _isLoading.value = false
            }
    }
    
    suspend fun addThought(content: String, source: String = "android_app") {
        _isLoading.value = true
        _error.value = null
        
        apiRepository.addThought(content, source)
            .onSuccess { thought ->
                val currentList = _thoughts.value.toMutableList()
                currentList.add(0, thought)
                _thoughts.value = currentList
                _isLoading.value = false
            }
            .onFailure { exception ->
                _error.value = exception.message
                _isLoading.value = false
            }
    }
    
    suspend fun searchThoughts(query: String) {
        _isLoading.value = true
        _error.value = null
        
        apiRepository.searchThoughts(query)
            .onSuccess { thoughtsList ->
                _thoughts.value = thoughtsList
                _isLoading.value = false
            }
            .onFailure { exception ->
                _error.value = exception.message
                _isLoading.value = false
            }
    }
    
    suspend fun uploadVoiceRecording(audioFile: File) {
        _isLoading.value = true
        _error.value = null
        
        apiRepository.uploadVoiceRecording(audioFile)
            .onSuccess { thought ->
                val currentList = _thoughts.value.toMutableList()
                currentList.add(0, thought)
                _thoughts.value = currentList
                _isLoading.value = false
            }
            .onFailure { exception ->
                _error.value = exception.message
                _isLoading.value = false
            }
    }
    
    suspend fun uploadDocument(file: File, contentType: String) {
        _isLoading.value = true
        _error.value = null
        
        apiRepository.uploadDocument(file, contentType)
            .onSuccess { document ->
                // In a real app, we might want to refresh the thoughts list
                // or add a new thought with this document attached
                _isLoading.value = false
            }
            .onFailure { exception ->
                _error.value = exception.message
                _isLoading.value = false
            }
    }
}
