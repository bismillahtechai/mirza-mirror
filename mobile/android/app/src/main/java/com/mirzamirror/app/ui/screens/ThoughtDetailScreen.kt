package com.mirzamirror.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.mirzamirror.app.model.Action
import com.mirzamirror.app.model.Link
import com.mirzamirror.app.model.Tag
import com.mirzamirror.app.model.Thought
import com.mirzamirror.app.ui.viewmodels.ThoughtViewModel
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ThoughtDetailScreen(
    thoughtId: String,
    navController: NavController,
    viewModel: ThoughtViewModel = hiltViewModel()
) {
    val thoughts by viewModel.thoughts.collectAsState()
    val thought = thoughts.find { it.id == thoughtId }
    var showMenu by remember { mutableStateOf(false) }
    
    LaunchedEffect(key1 = thoughtId) {
        if (thoughts.isEmpty()) {
            viewModel.fetchThoughts()
        }
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Thought Details") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { showMenu = true }) {
                        Icon(Icons.Default.MoreVert, contentDescription = "More Options")
                    }
                    DropdownMenu(
                        expanded = showMenu,
                        onDismissRequest = { showMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Share") },
                            onClick = { 
                                showMenu = false
                                // Share functionality would go here
                            },
                            leadingIcon = {
                                Icon(Icons.Default.Share, contentDescription = "Share")
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Edit") },
                            onClick = { 
                                showMenu = false
                                // Edit functionality would go here
                            },
                            leadingIcon = {
                                Icon(Icons.Default.Edit, contentDescription = "Edit")
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Delete") },
                            onClick = { 
                                showMenu = false
                                // Delete functionality would go here
                                navController.popBackStack()
                            },
                            leadingIcon = {
                                Icon(
                                    Icons.Default.Delete, 
                                    contentDescription = "Delete",
                                    tint = MaterialTheme.colorScheme.error
                                )
                            }
                        )
                    }
                }
            )
        }
    ) { paddingValues ->
        if (thought == null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .verticalScroll(rememberScrollState())
                    .padding(16.dp)
            ) {
                // Content section
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Text(
                            text = thought.content,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Default.AccessTime,
                                contentDescription = "Time",
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = formatDate(thought.createdAt),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            Icon(
                                imageVector = Icons.Default.Source,
                                contentDescription = "Source",
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = thought.source,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Tags section
                if (thought.tags.isNotEmpty()) {
                    Text(
                        text = "Tags",
                        style = MaterialTheme.typography.titleMedium
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    LazyRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(thought.tags) { tag ->
                            TagChip(tag)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                }
                
                // Summary section
                thought.summary?.let { summary ->
                    if (summary.isNotEmpty()) {
                        Text(
                            text = "Summary",
                            style = MaterialTheme.typography.titleMedium
                        )
                        
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text(
                                text = summary,
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.padding(16.dp)
                            )
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                    }
                }
                
                // Actions section
                if (thought.actions.isNotEmpty()) {
                    Text(
                        text = "Actions",
                        style = MaterialTheme.typography.titleMedium
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    thought.actions.forEach { action ->
                        ActionItem(action)
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                    
                    Spacer(modifier = Modifier.height(8.dp))
                }
                
                // Related thoughts section
                if (thought.links.isNotEmpty()) {
                    Text(
                        text = "Related Thoughts",
                        style = MaterialTheme.typography.titleMedium
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    thought.links.forEach { link ->
                        LinkItem(link)
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                    
                    Spacer(modifier = Modifier.height(8.dp))
                }
                
                // Attachments section
                if (thought.audioFile != null || thought.documentFile != null) {
                    Text(
                        text = "Attachments",
                        style = MaterialTheme.typography.titleMedium
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    thought.audioFile?.let { audioFile ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Default.AudioFile,
                                    contentDescription = "Audio Recording",
                                    tint = MaterialTheme.colorScheme.primary
                                )
                                
                                Spacer(modifier = Modifier.width(16.dp))
                                
                                Text(
                                    text = "Audio Recording",
                                    style = MaterialTheme.typography.bodyMedium,
                                    modifier = Modifier.weight(1f)
                                )
                                
                                IconButton(onClick = {
                                    // Play audio logic would go here
                                }) {
                                    Icon(
                                        imageVector = Icons.Default.PlayCircle,
                                        contentDescription = "Play",
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                }
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                    
                    thought.documentFile?.let { documentFile ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Description,
                                    contentDescription = "Document",
                                    tint = MaterialTheme.colorScheme.primary
                                )
                                
                                Spacer(modifier = Modifier.width(16.dp))
                                
                                Text(
                                    text = documentFile.substringAfterLast("/"),
                                    style = MaterialTheme.typography.bodyMedium,
                                    modifier = Modifier.weight(1f),
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                                
                                IconButton(onClick = {
                                    // View document logic would go here
                                }) {
                                    Icon(
                                        imageVector = Icons.Default.OpenInNew,
                                        contentDescription = "Open",
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TagChip(tag: Tag) {
    SuggestionChip(
        onClick = { /* Handle tag click */ },
        label = { Text(tag.name) },
        icon = {
            Icon(
                imageVector = Icons.Default.Tag,
                contentDescription = "Tag"
            )
        }
    )
}

@Composable
fun ActionItem(action: Action) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(8.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.Top
        ) {
            Checkbox(
                checked = action.completed,
                onCheckedChange = {
                    // Update action completion status logic would go here
                }
            )
            
            Spacer(modifier = Modifier.width(8.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = action.content,
                    style = MaterialTheme.typography.bodyMedium
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    PriorityChip(action.priority)
                    
                    action.dueDate?.let { dueDate ->
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "Due: $dueDate",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun PriorityChip(priority: String) {
    val (color, text) = when (priority.lowercase()) {
        "high" -> Pair(Color.Red, "High Priority")
        "medium" -> Pair(Color.Yellow, "Medium Priority")
        "low" -> Pair(Color.Blue, "Low Priority")
        else -> Pair(MaterialTheme.colorScheme.primary, priority.capitalize())
    }
    
    Surface(
        shape = RoundedCornerShape(4.dp),
        color = color.copy(alpha = 0.2f),
        modifier = Modifier.padding(vertical = 4.dp)
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.bodySmall,
            color = color,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
        )
    }
}

@Composable
fun LinkItem(link: Link) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(8.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = relationshipIcon(link.relationship),
                contentDescription = link.relationship,
                tint = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.width(16.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = link.relationship.capitalize(),
                    style = MaterialTheme.typography.bodyMedium
                )
                
                Text(
                    text = "Strength: ${(link.strength * 100).toInt()}%",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            IconButton(onClick = {
                // Navigate to linked thought logic would go here
            }) {
                Icon(
                    imageVector = Icons.Default.ArrowForward,
                    contentDescription = "View Linked Thought"
                )
            }
        }
    }
}

@Composable
fun relationshipIcon(relationship: String) = when (relationship.lowercase()) {
    "similar" -> Icons.Default.CompareArrows
    "continuation" -> Icons.Default.ArrowForward
    "contradiction" -> Icons.Default.Close
    "inspiration" -> Icons.Default.Lightbulb
    else -> Icons.Default.Link
}

private fun formatDate(date: Date): String {
    val formatter = SimpleDateFormat("MMM d, yyyy h:mm a", Locale.getDefault())
    return formatter.format(date)
}

private fun String.capitalize(): String {
    return this.replaceFirstChar { 
        if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() 
    }
}
