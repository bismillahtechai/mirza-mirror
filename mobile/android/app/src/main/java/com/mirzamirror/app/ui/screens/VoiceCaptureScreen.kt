package com.mirzamirror.app.ui.screens

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import com.mirzamirror.app.ui.viewmodels.ThoughtViewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VoiceCaptureScreen(
    navController: NavController,
    viewModel: ThoughtViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    var isRecording by remember { mutableStateOf(false) }
    var recordingTime by remember { mutableStateOf(0) }
    var audioFile by remember { mutableStateOf<File?>(null) }
    var isUploading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var hasRecordingPermission by remember { 
        mutableStateOf(
            ContextCompat.checkSelfPermission(
                context, 
                Manifest.permission.RECORD_AUDIO
            ) == PackageManager.PERMISSION_GRANTED
        ) 
    }
    
    val mediaRecorder = remember { MediaRecorderWrapper() }
    
    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasRecordingPermission = isGranted
    }
    
    LaunchedEffect(isRecording) {
        if (isRecording) {
            recordingTime = 0
            while (isRecording) {
                delay(100)
                recordingTime += 100
            }
        }
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Voice Capture") },
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
                // Recording indicator
                if (isRecording) {
                    Text(
                        text = "Recording...",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.error
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = formatTime(recordingTime),
                        style = MaterialTheme.typography.headlineLarge
                    )
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    
                    // Waveform visualization
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                        modifier = Modifier.height(60.dp)
                    ) {
                        repeat(20) { index ->
                            val infiniteTransition = rememberInfiniteTransition()
                            val height by infiniteTransition.animateFloat(
                                initialValue = 10f,
                                targetValue = 50f,
                                animationSpec = infiniteRepeatable(
                                    animation = tween(
                                        durationMillis = 500,
                                        easing = FastOutSlowInEasing,
                                        delayMillis = index * 50
                                    ),
                                    repeatMode = RepeatMode.Reverse
                                )
                            )
                            
                            Box(
                                modifier = Modifier
                                    .width(6.dp)
                                    .height(height.dp)
                                    .clip(RoundedCornerShape(3.dp))
                                    .background(MaterialTheme.colorScheme.error)
                            )
                        }
                    }
                } else {
                    Icon(
                        imageVector = Icons.Default.Mic,
                        contentDescription = "Microphone",
                        modifier = Modifier.size(100.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = "Tap to Start Recording",
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
                
                // Recording button
                FloatingActionButton(
                    onClick = {
                        if (!hasRecordingPermission) {
                            permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                        } else if (isRecording) {
                            stopRecording(mediaRecorder) { file ->
                                audioFile = file
                                isRecording = false
                            }
                        } else {
                            startRecording(context, mediaRecorder) { success, error ->
                                if (success) {
                                    isRecording = true
                                    errorMessage = null
                                } else {
                                    errorMessage = error
                                }
                            }
                        }
                    },
                    modifier = Modifier.size(80.dp)
                ) {
                    Icon(
                        imageVector = if (isRecording) Icons.Default.Stop else Icons.Default.Mic,
                        contentDescription = if (isRecording) "Stop Recording" else "Start Recording",
                        modifier = Modifier.size(32.dp)
                    )
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                
                // Upload button
                if (!isRecording && audioFile != null) {
                    Button(
                        onClick = {
                            audioFile?.let { file ->
                                isUploading = true
                                scope.launch {
                                    try {
                                        viewModel.uploadVoiceRecording(file)
                                        navController.popBackStack()
                                    } catch (e: Exception) {
                                        errorMessage = "Failed to upload: ${e.message}"
                                        isUploading = false
                                    }
                                }
                            }
                        },
                        enabled = !isUploading
                    ) {
                        Text("Upload Recording")
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

private fun formatTime(timeInMillis: Int): String {
    val totalSeconds = timeInMillis / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    val tenths = (timeInMillis % 1000) / 100
    return String.format("%02d:%02d.%01d", minutes, seconds, tenths)
}

private fun startRecording(
    context: Context,
    mediaRecorderWrapper: MediaRecorderWrapper,
    callback: (Boolean, String?) -> Unit
) {
    try {
        val outputFile = createOutputFile(context)
        mediaRecorderWrapper.start(context, outputFile.absolutePath)
        callback(true, null)
    } catch (e: IOException) {
        callback(false, "Failed to start recording: ${e.message}")
    }
}

private fun stopRecording(
    mediaRecorderWrapper: MediaRecorderWrapper,
    callback: (File) -> Unit
) {
    val file = mediaRecorderWrapper.stop()
    file?.let { callback(it) }
}

private fun createOutputFile(context: Context): File {
    val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
    val fileName = "VOICE_$timestamp.m4a"
    return File(context.cacheDir, fileName)
}

class MediaRecorderWrapper {
    private var mediaRecorder: MediaRecorder? = null
    private var outputPath: String? = null
    
    fun start(context: Context, outputPath: String) {
        this.outputPath = outputPath
        
        mediaRecorder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            MediaRecorder(context)
        } else {
            @Suppress("DEPRECATION")
            MediaRecorder()
        }
        
        mediaRecorder?.apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            setAudioEncodingBitRate(128000)
            setAudioSamplingRate(44100)
            setOutputFile(outputPath)
            prepare()
            start()
        }
    }
    
    fun stop(): File? {
        try {
            mediaRecorder?.apply {
                stop()
                release()
            }
            mediaRecorder = null
            
            return outputPath?.let { File(it) }
        } catch (e: Exception) {
            return null
        }
    }
}
