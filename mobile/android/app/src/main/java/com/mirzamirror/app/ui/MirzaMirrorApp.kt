package com.mirzamirror.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.mirzamirror.app.model.Thought
import com.mirzamirror.app.ui.screens.*
import com.mirzamirror.app.ui.viewmodels.ThoughtViewModel
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun MirzaMirrorApp() {
    val navController = rememberNavController()
    
    NavHost(navController = navController, startDestination = "thoughts") {
        composable("thoughts") {
            ThoughtsScreen(navController)
        }
        composable("thought/{thoughtId}") { backStackEntry ->
            val thoughtId = backStackEntry.arguments?.getString("thoughtId") ?: ""
            ThoughtDetailScreen(thoughtId, navController)
        }
        composable("add_thought") {
            AddThoughtScreen(navController)
        }
        composable("voice_capture") {
            VoiceCaptureScreen(navController)
        }
        composable("document_picker") {
            DocumentPickerScreen(navController)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ThoughtsScreen(
    navController: NavController,
    viewModel: ThoughtViewModel = hiltViewModel()
) {
    val thoughts by viewModel.thoughts.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    var searchQuery by remember { mutableStateOf("") }
    var showSearchBar by remember { mutableStateOf(false) }
    
    LaunchedEffect(key1 = true) {
        viewModel.fetchThoughts()
    }
    
    Scaffold(
        topBar = {
            if (showSearchBar) {
                SearchBar(
                    query = searchQuery,
                    onQueryChange = { searchQuery = it },
                    onSearch = { 
                        viewModel.searchThoughts(searchQuery)
                        showSearchBar = false
                    },
                    onClose = { 
                        showSearchBar = false
                        searchQuery = ""
                        viewModel.fetchThoughts()
                    },
                    active = true,
                    onActiveChange = { showSearchBar = it },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    // Search suggestions could go here
                }
            } else {
                TopAppBar(
                    title = { Text("Mirza Mirror") },
                    actions = {
                        IconButton(onClick = { showSearchBar = true }) {
                            Icon(Icons.Default.Search, contentDescription = "Search")
                        }
                    }
                )
            }
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = { 
                    // Show a menu with options
                    // For simplicity, we'll just navigate to add_thought
                    navController.navigate("add_thought")
                },
                icon = { Icon(Icons.Filled.Add, "Add Thought") },
                text = { Text("Add") },
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center)
                )
            } else if (error != null) {
                Column(
                    modifier = Modifier
                        .align(Alignment.Center)
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        Icons.Default.Warning,
                        contentDescription = "Error",
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.error
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = error ?: "An unknown error occurred",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.error
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { viewModel.fetchThoughts() }) {
                        Text("Try Again")
                    }
                }
            } else if (thoughts.isEmpty()) {
                Column(
                    modifier = Modifier
                        .align(Alignment.Center)
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        Icons.Default.Info,
                        contentDescription = "No thoughts",
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "No thoughts found",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { navController.navigate("add_thought") }) {
                        Text("Add Your First Thought")
                    }
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(thoughts) { thought ->
                        ThoughtItem(thought = thought, onClick = {
                            navController.navigate("thought/${thought.id}")
                        })
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ThoughtItem(thought: Thought, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = thought.content,
                style = MaterialTheme.typography.bodyLarge,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = formatDate(thought.createdAt),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Row {
                    thought.tags.take(3).forEach { tag ->
                        Chip(
                            onClick = { /* Handle tag click */ },
                            label = { Text(tag.name) },
                            modifier = Modifier.padding(end = 4.dp)
                        )
                    }
                }
            }
        }
    }
}

private fun formatDate(date: Date): String {
    val formatter = SimpleDateFormat("MMM d, yyyy h:mm a", Locale.getDefault())
    return formatter.format(date)
}
