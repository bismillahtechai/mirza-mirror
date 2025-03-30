package com.mirzamirror.app.network

import com.mirzamirror.app.model.Action
import com.mirzamirror.app.model.Document
import com.mirzamirror.app.model.Link
import com.mirzamirror.app.model.Tag
import com.mirzamirror.app.model.Thought
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query
import java.io.File
import java.util.Date
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

/**
 * API service interface for Retrofit
 */
interface MirzaMirrorApiService {
    @GET("api/thoughts")
    suspend fun getThoughts(): List<Thought>
    
    @POST("api/capture/text")
    suspend fun addThought(@Body thoughtRequest: ThoughtRequest): Thought
    
    @GET("api/thoughts/search")
    suspend fun searchThoughts(@Query("query") query: String): List<Thought>
}

/**
 * Request model for adding a thought
 */
data class ThoughtRequest(
    val content: String,
    val source: String = "android_app"
)

/**
 * Repository for API operations
 */
@Singleton
class ApiRepository @Inject constructor(
    private val apiService: MirzaMirrorApiService
) {
    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    suspend fun getThoughts(): Result<List<Thought>> = withContext(Dispatchers.IO) {
        try {
            val thoughts = apiService.getThoughts()
            Result.success(thoughts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun addThought(content: String, source: String = "android_app"): Result<Thought> = withContext(Dispatchers.IO) {
        try {
            val thoughtRequest = ThoughtRequest(content, source)
            val thought = apiService.addThought(thoughtRequest)
            Result.success(thought)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun searchThoughts(query: String): Result<List<Thought>> = withContext(Dispatchers.IO) {
        try {
            val thoughts = apiService.searchThoughts(query)
            Result.success(thoughts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun uploadVoiceRecording(audioFile: File): Result<Thought> = withContext(Dispatchers.IO) {
        try {
            val url = "https://mirza-mirror-api.onrender.com/api/capture/voice"
            
            val requestBody = audioFile.asRequestBody("audio/m4a".toMediaType())
            
            val request = Request.Builder()
                .url(url)
                .post(requestBody)
                .build()
            
            val response = okHttpClient.newCall(request).execute()
            
            if (response.isSuccessful) {
                val jsonString = response.body?.string() ?: ""
                val jsonObject = JSONObject(jsonString)
                
                // Parse the response into a Thought object
                // This is a simplified version - in a real app, use Gson or Moshi
                val thought = parseThoughtFromJson(jsonObject)
                Result.success(thought)
            } else {
                Result.failure(Exception("Failed to upload recording: ${response.code}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun uploadDocument(file: File, contentType: String): Result<Document> = withContext(Dispatchers.IO) {
        try {
            val url = "https://mirza-mirror-api.onrender.com/api/documents"
            
            val requestBody = MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart(
                    "file", 
                    file.name, 
                    file.asRequestBody(contentType.toMediaType())
                )
                .addFormDataPart("content_type", contentType)
                .build()
            
            val request = Request.Builder()
                .url(url)
                .post(requestBody)
                .build()
            
            val response = okHttpClient.newCall(request).execute()
            
            if (response.isSuccessful) {
                val jsonString = response.body?.string() ?: ""
                val jsonObject = JSONObject(jsonString)
                
                // Parse the response into a Document object
                // This is a simplified version - in a real app, use Gson or Moshi
                val document = parseDocumentFromJson(jsonObject)
                Result.success(document)
            } else {
                Result.failure(Exception("Failed to upload document: ${response.code}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Helper method to parse JSON into Thought object
    private fun parseThoughtFromJson(json: JSONObject): Thought {
        return Thought(
            id = json.getString("id"),
            content = json.getString("content"),
            source = json.getString("source"),
            createdAt = Date(json.getLong("created_at")),
            updatedAt = Date(json.getLong("updated_at")),
            audioFile = if (json.has("audio_file")) json.getString("audio_file") else null,
            documentFile = if (json.has("document_file")) json.getString("document_file") else null,
            summary = if (json.has("summary")) json.getString("summary") else null,
            tags = emptyList(), // In a real app, parse the tags array
            links = emptyList(), // In a real app, parse the links array
            actions = emptyList() // In a real app, parse the actions array
        )
    }
    
    // Helper method to parse JSON into Document object
    private fun parseDocumentFromJson(json: JSONObject): Document {
        return Document(
            id = json.getString("id"),
            filePath = json.getString("file_path"),
            content = if (json.has("content")) json.getString("content") else null,
            contentType = json.getString("content_type"),
            createdAt = Date(json.getLong("created_at")),
            updatedAt = Date(json.getLong("updated_at"))
        )
    }
}

/**
 * Module to provide API dependencies
 */
object ApiModule {
    private const val BASE_URL = "https://mirza-mirror-api.onrender.com/"
    
    fun provideApiService(): MirzaMirrorApiService {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        
        return retrofit.create(MirzaMirrorApiService::class.java)
    }
}
