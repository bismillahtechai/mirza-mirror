package com.mirzamirror.app.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.AttachFile
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Description
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.mirzamirror.app.ui.viewmodels.ThoughtViewModel
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DocumentPickerScreen(
    navController: NavController,
    viewModel: ThoughtViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    var selectedFileUri by remember { mutableStateOf<Uri?>(null) }
    var selectedFileName by remember { mutableStateOf<String?>(null) }
    var selectedFileType by remember { mutableStateOf<String?>(null) }
    var isUploading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    
    val documentPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        uri?.let {
            selectedFileUri = it
            
            // Get file name
            context.contentResolver.query(it, null, null, null, null)?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val displayNameIndex = cursor.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                    if (displayNameIndex != -1) {
                        selectedFileName = cursor.getString(displayNameIndex)
                    }
                }
            }
            
            // Get file type
            selectedFileType = context.contentResolver.getType(it)
        }
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Document Upload") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxWidth()
            ) {
                // Document selection area
                if (selectedFileUri != null && selectedFileName != null) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier.padding(16.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Description,
                                contentDescription = "Document",
                                modifier = Modifier.size(64.dp),
                                tint = MaterialTheme.colorScheme.primary
                            )
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            Text(
                                text = selectedFileName ?: "Selected Document",
                                style = MaterialTheme.typography.titleMedium
                            )
                            
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Text(
                                text = "Ready to upload",
                                color = MaterialTheme.colorScheme.primary,
                                style = MaterialTheme.typography.bodyMedium
                            )
                        }
                    }
                } else {
                    Icon(
                        imageVector = Icons.Default.AttachFile,
                        contentDescription = "Attach Document",
                        modifier = Modifier.size(100.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = "Select a Document",
                        style = MaterialTheme.typography.headlineMedium
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    Text(
                        text = "Tap the button below to choose a document to upload",
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                
                // Error message
                errorMessage?.let {
                    Text(
                        text = it,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(16.dp)
                    )
                }
                
                // Document picker button
                Button(
                    onClick = {
                        documentPicker.launch("*/*")
                    },
                    enabled = !isUploading
                ) {
                    Icon(
                        imageVector = Icons.Default.AttachFile,
                        contentDescription = "Select Document"
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = if (selectedFileUri == null) "Select Document" else "Change Document"
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Upload button
                if (selectedFileUri != null) {
                    Button(
                        onClick = {
                            selectedFileUri?.let { uri ->
                                selectedFileType?.let { type ->
                                    isUploading = true
                                    errorMessage = null
                                    
                                    scope.launch {
                                        try {
                                            // Copy the file to a temporary location
                                            val tempFile = File(context.cacheDir, selectedFileName ?: "document")
                                            context.contentResolver.openInputStream(uri)?.use { input ->
                                                FileOutputStream(tempFile).use { output ->
                                                    input.copyTo(output)
                                                }
                                            }
                                            
                                            // Upload the file
                                            viewModel.uploadDocument(tempFile, type)
                                            
                                            // Navigate back
                                            navController.popBackStack()
                                        } catch (e: Exception) {
                                            errorMessage = "Failed to upload: ${e.message}"
                                            isUploading = false
                                        }
                                    }
                                }
                            }
                        },
                        enabled = !isUploading && selectedFileUri != null
                    ) {
                        Icon(
                            imageVector = Icons.Default.Check,
                            contentDescription = "Upload"
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Upload Document")
                    }
                }
                
                if (isUploading) {
                    Spacer(modifier = Modifier.height(16.dp))
                    CircularProgressIndicator()
                }
            }
        }
    }
}
