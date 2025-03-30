# Mirza Mirror API Documentation

This document provides comprehensive documentation for the Mirza Mirror API, which allows developers to integrate with the thought externalization system.

## Base URL

```
https://mirza-mirror-api.onrender.com
```

## Authentication

All API requests require authentication using an API key.

```
Authorization: Bearer YOUR_API_KEY
```

To obtain an API key, contact the system administrator.

## API Endpoints

### Memory Endpoints

#### Get Memory

Retrieves a specific memory by ID.

```
GET /memories/{memory_id}
```

**Parameters:**
- `memory_id` (path parameter): The unique identifier of the memory to retrieve

**Response:**
```json
{
  "id": "string",
  "content": "string",
  "created_at": "string",
  "updated_at": "string",
  "source": "string",
  "tags": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "summary": "string",
  "emotion": "string",
  "links": [
    {
      "id": "string",
      "target_thought_id": "string",
      "relationship": "string",
      "strength": 0.95
    }
  ],
  "actions": [
    {
      "id": "string",
      "content": "string",
      "priority": "string",
      "due_date": "string",
      "completed": false
    }
  ]
}
```

#### Search Memories

Searches for memories based on a query.

```
GET /memories/search
```

**Parameters:**
- `query` (query parameter): The search query
- `limit` (query parameter, optional): Maximum number of results to return (default: 10)
- `offset` (query parameter, optional): Number of results to skip (default: 0)

**Response:**
```json
[
  {
    "id": "string",
    "content": "string",
    "created_at": "string",
    "source": "string",
    "tags": [
      {
        "id": "string",
        "name": "string"
      }
    ],
    "score": 0.95
  }
]
```

#### Add Memory

Adds a new memory.

```
POST /memories
```

**Request Body:**
```json
{
  "content": "string",
  "source": "string",
  "tags": ["string"]
}
```

**Response:**
```json
{
  "id": "string",
  "content": "string",
  "created_at": "string",
  "source": "string"
}
```

### Thought Endpoints

#### Get Thought

Retrieves a specific thought by ID.

```
GET /thoughts/{thought_id}
```

**Parameters:**
- `thought_id` (path parameter): The unique identifier of the thought to retrieve

**Response:**
```json
{
  "id": "string",
  "content": "string",
  "created_at": "string",
  "updated_at": "string",
  "source": "string",
  "tags": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "summary": "string",
  "emotion": "string",
  "links": [
    {
      "id": "string",
      "target_thought_id": "string",
      "relationship": "string",
      "strength": 0.95
    }
  ],
  "actions": [
    {
      "id": "string",
      "content": "string",
      "priority": "string",
      "due_date": "string",
      "completed": false
    }
  ],
  "audio_file": "string",
  "document_file": "string"
}
```

#### Create Thought

Creates a new text thought.

```
POST /thoughts
```

**Request Body:**
```json
{
  "content": "string",
  "source": "string"
}
```

**Response:**
```json
{
  "id": "string",
  "content": "string",
  "created_at": "string",
  "source": "string"
}
```

#### Create Voice Thought

Creates a new thought from a voice recording.

```
POST /thoughts/voice
```

**Request Body:**
Form data with:
- `audio` (file): The audio file containing the voice recording

**Response:**
```json
{
  "id": "string",
  "content": "string",
  "created_at": "string",
  "source": "string",
  "audio_file": "string"
}
```

#### Search Thoughts

Searches for thoughts based on a query.

```
GET /thoughts/search
```

**Parameters:**
- `query` (query parameter): The search query
- `limit` (query parameter, optional): Maximum number of results to return (default: 10)
- `offset` (query parameter, optional): Number of results to skip (default: 0)

**Response:**
```json
[
  {
    "id": "string",
    "content": "string",
    "created_at": "string",
    "source": "string",
    "tags": [
      {
        "id": "string",
        "name": "string"
      }
    ],
    "score": 0.95
  }
]
```

### Document Endpoints

#### Upload Document

Uploads a document.

```
POST /documents
```

**Request Body:**
Form data with:
- `document` (file): The document file to upload

**Response:**
```json
{
  "id": "string",
  "filename": "string",
  "content": "string",
  "created_at": "string",
  "metadata": {
    "title": "string",
    "author": "string",
    "created_date": "string",
    "type": "string"
  },
  "file_url": "string"
}
```

#### Get Document

Retrieves a specific document by ID.

```
GET /documents/{document_id}
```

**Parameters:**
- `document_id` (path parameter): The unique identifier of the document to retrieve

**Response:**
```json
{
  "id": "string",
  "filename": "string",
  "content": "string",
  "created_at": "string",
  "metadata": {
    "title": "string",
    "author": "string",
    "created_date": "string",
    "type": "string"
  },
  "file_url": "string"
}
```

### Import Endpoints

#### Import Conversation

Imports a conversation from an AI assistant.

```
POST /import
```

**Request Body:**
Form data with:
- `file` (file): The conversation file to import
- `source` (string): The source of the conversation (chatgpt, claude, gemini)

**Response:**
```json
{
  "imported_count": 0,
  "thoughts": [
    {
      "id": "string",
      "content": "string",
      "created_at": "string",
      "source": "string"
    }
  ]
}
```

### Agent Endpoints

#### Tag Thought

Tags a thought using the tagging agent.

```
POST /agents/tag
```

**Request Body:**
```json
{
  "content": "string"
}
```

**Response:**
```json
{
  "tags": ["string"]
}
```

#### Link Thought

Links a thought to related thoughts using the linking agent.

```
POST /agents/link
```

**Request Body:**
```json
{
  "content": "string",
  "thought_id": "string"
}
```

**Response:**
```json
{
  "links": [
    {
      "thought_id": "string",
      "relationship": "string",
      "strength": 0.95
    }
  ]
}
```

#### Generate Reflection

Generates a reflection for a thought using the reflection agent.

```
POST /agents/reflect
```

**Request Body:**
```json
{
  "content": "string"
}
```

**Response:**
```json
{
  "summary": "string",
  "emotion": "string",
  "insights": ["string"]
}
```

#### Extract Actions

Extracts actions from a thought using the action agent.

```
POST /agents/actions
```

**Request Body:**
```json
{
  "content": "string"
}
```

**Response:**
```json
{
  "actions": [
    {
      "content": "string",
      "priority": "string",
      "due_date": "string"
    }
  ]
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error responses include a JSON body with details:

```json
{
  "detail": "Error message"
}
```

## Rate Limiting

API requests are limited to 100 requests per minute per API key. If you exceed this limit, you will receive a `429 Too Many Requests` response.

## Webhooks

Mirza Mirror supports webhooks for real-time notifications of events. Contact the system administrator to set up webhooks for your application.
