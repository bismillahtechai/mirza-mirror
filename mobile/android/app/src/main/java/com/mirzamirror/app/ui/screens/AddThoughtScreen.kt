package com.mirzamirror.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.mirzamirror.app.ui.viewmodels.ThoughtViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddThoughtScreen(
    navController: NavController,
    viewModel: ThoughtViewModel = hiltViewModel()
) {
    var thoughtText by remember { mutableStateOf("") }
    var isSubmitting by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Thought") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    if (thoughtText.isNotBlank()) {
                        isSubmitting = true
                        viewModel.addThought(thoughtText)
                        // Navigate back after a short delay to simulate network request
                        // In a real app, we would observe the result and navigate back on success
                        navController.popBackStack()
                    }
                },
                enabled = thoughtText.isNotBlank() && !isSubmitting
            ) {
                Icon(Icons.Default.Send, contentDescription = "Save Thought")
            }
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                OutlinedTextField(
                    value = thoughtText,
                    onValueChange = { thoughtText = it },
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight()
                        .weight(1f),
                    placeholder = { Text("Enter your thought here...") },
                    colors = TextFieldDefaults.outlinedTextFieldColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                )
                
                if (isSubmitting) {
                    LinearProgressIndicator(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 16.dp)
                    )
                }
            }
        }
    }
}
