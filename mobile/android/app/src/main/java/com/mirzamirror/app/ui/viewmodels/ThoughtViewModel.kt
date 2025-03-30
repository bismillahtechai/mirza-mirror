package com.mirzamirror.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mirzamirror.app.data.ThoughtRepository
import com.mirzamirror.app.model.Thought
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.io.File
import javax.inject.Inject

@HiltViewModel
class ThoughtViewModel @Inject constructor(
    private val thoughtRepository: ThoughtRepository
) : ViewModel() {
    
    // Expose state flows from repository
    val thoughts: StateFlow<List<Thought>> = thoughtRepository.thoughts
    val isLoading: StateFlow<Boolean> = thoughtRepository.isLoading
    val error: StateFlow<String?> = thoughtRepository.error
    
    fun fetchThoughts() {
        viewModelScope.launch {
            thoughtRepository.fetchThoughts()
        }
    }
    
    fun addThought(content: String, source: String = "android_app") {
        viewModelScope.launch {
            thoughtRepository.addThought(content, source)
        }
    }
    
    fun searchThoughts(query: String) {
        viewModelScope.launch {
            thoughtRepository.searchThoughts(query)
        }
    }
    
    fun uploadVoiceRecording(audioFile: File) {
        viewModelScope.launch {
            thoughtRepository.uploadVoiceRecording(audioFile)
        }
    }
    
    fun uploadDocument(file: File, contentType: String) {
        viewModelScope.launch {
            thoughtRepository.uploadDocument(file, contentType)
        }
    }
}
