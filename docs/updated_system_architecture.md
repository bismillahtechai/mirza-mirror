# Mirza Mirror: Updated System Architecture with Docling Integration

## Overview

Mirza Mirror is an AI-powered thought externalization system designed to capture, organize, and retrieve thoughts across different formats. The system now incorporates Docling for advanced document processing and linguistic analysis capabilities.

## System Components

### 1. Capture Service
Responsible for collecting thoughts from various sources and formats.

- **Voice Capture**: Records and processes voice notes from iPhone
- **Text Capture**: Collects text notes from iPhone
- **Document Capture**: Handles images of receipts, business cards, screenshots, etc.

### 2. Docling Integration
Leverages Docling's document processing capabilities.

- **Document Parser**: Uses Docling to parse various document formats (PDF, DOCX, images)
- **Document Analyzer**: Extracts structured information from documents
- **OCR Service**: Processes scanned documents and images with text

### 3. Import Service
Handles importing conversations from AI assistants.

- **Conversation Parser**: Processes exported conversations from ChatGPT, Claude, Gemini
- **Format Handler**: Supports both markdown and JSON formats
- **Content Extractor**: Extracts meaningful content from conversations

### 4. Processing Service
Transforms raw input into structured thought data.

- **Transcription Service**: Uses OpenAI Whisper to convert voice to text
- **Preprocessing Pipeline**: Cleans and normalizes text data
- **Embedding Generator**: Creates vector embeddings for semantic search

### 5. Memory Store
Central database for storing all thought data and metadata.

- **Relational Database**: Stores structured thought data and metadata (PostgreSQL/SQLite)
- **Vector Database**: Stores embeddings for semantic search (Chroma)
- **File Storage**: Stores original audio files, documents, and other binary data

### 6. Agent Orchestrator
Manages the AI agents that process and organize thoughts.

- **Agent Manager**: Coordinates agent workflows and schedules processing
- **Context Provider**: Supplies relevant context to agents for processing
- **Result Integrator**: Incorporates agent outputs back into the memory store

### 7. Agent Services
Specialized AI services that process thoughts in different ways.

- **Tagging Agent**: Classifies thoughts by project, emotion, category
- **Linking Agent**: Identifies connections between thoughts
- **Reflection Agent**: Generates insights and identifies patterns
- **Action Agent**: Extracts tasks and action items

### 8. Retrieval Service
Provides access to stored thoughts and generated insights.

- **Search Service**: Enables keyword and semantic search
- **Digest Generator**: Creates daily/weekly summaries of important thoughts
- **Project View Service**: Organizes thoughts by project or category
- **Pattern Recognition**: Identifies recurring themes and patterns

### 9. API Layer
Exposes system functionality to the frontend application.

- **REST API**: Provides endpoints for all system functions
- **WebSocket Service**: Enables real-time updates and notifications
- **Authentication Service**: Manages user authentication and security

### 10. Mobile Application
iPhone app that serves as the primary user interface.

- **Capture Interface**: UI for recording voice, text notes, and documents
- **Browse Interface**: UI for viewing and searching past thoughts
- **Digest View**: UI for viewing AI-generated insights and summaries
- **Settings Interface**: UI for configuring system preferences

## Data Models

### Thought
The core data entity representing a captured thought.

```json
{
  "id": "uuid",
  "content": "text content of the thought",
  "source": "voice_note|text_note|document|import",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "audio_file": "path/to/audio.mp3",  // if source is voice_note
  "document_file": "path/to/document.pdf",  // if source is document
  "embedding_id": "reference to vector embedding",
  "summary": "AI-generated summary",
  "metadata": {
    "device": "iphone|computer",
    "app_version": "1.0.0",
    "location": "coordinates",  // optional
    "context_hint": "user-provided context"  // optional
  }
}
```

### Document
Represents a document processed by Docling.

```json
{
  "id": "uuid",
  "thought_id": "reference to thought",
  "file_path": "path/to/document",
  "file_type": "pdf|docx|image|etc",
  "content": "extracted text content",
  "docling_representation": "DoclingDocument JSON",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### ImportedConversation
Represents an imported conversation from an AI assistant.

```json
{
  "id": "uuid",
  "source": "chatgpt|claude|gemini",
  "format": "markdown|json",
  "original_file": "path/to/original.md",
  "imported_at": "timestamp",
  "metadata": {
    "title": "conversation title",
    "date": "original conversation date",
    "assistant": "assistant name/model"
  }
}
```

### ConversationThought
Links imported conversations to thoughts.

```json
{
  "conversation_id": "reference to imported conversation",
  "thought_id": "reference to thought",
  "segment_index": 0,  // position in conversation
  "role": "user|assistant",
  "created_at": "timestamp"
}
```

### Tag
Represents a category, project, emotion, or other classification.

```json
{
  "id": "uuid",
  "name": "tag name",
  "type": "project|emotion|category|custom",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### ThoughtTag
Associates thoughts with tags (many-to-many relationship).

```json
{
  "thought_id": "reference to thought",
  "tag_id": "reference to tag",
  "confidence": 0.95,  // AI confidence in this tag
  "created_at": "timestamp"
}
```

### Link
Represents a connection between two thoughts.

```json
{
  "source_thought_id": "reference to source thought",
  "target_thought_id": "reference to target thought",
  "relationship": "similar|continuation|contradiction|inspiration",
  "strength": 0.87,  // similarity or relationship strength
  "created_at": "timestamp"
}
```

### Action
Represents a task or action item extracted from a thought.

```json
{
  "id": "uuid",
  "thought_id": "reference to source thought",
  "content": "description of the action",
  "status": "pending|completed|dismissed",
  "due_date": "timestamp",  // optional
  "priority": "high|medium|low",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Reflection
Represents an AI-generated insight or pattern.

```json
{
  "id": "uuid",
  "type": "insight|pattern|summary",
  "content": "text content of the reflection",
  "related_thoughts": ["array of thought ids"],
  "created_at": "timestamp"
}
```

## API Endpoints

### Capture Endpoints
- `POST /api/thoughts` - Create a new thought (text)
- `POST /api/thoughts/voice` - Create a new thought from voice
- `POST /api/thoughts/document` - Create a new thought from document
- `POST /api/import` - Import thoughts from external sources

### Docling Endpoints
- `POST /api/docling/parse` - Parse a document using Docling
- `GET /api/docling/formats` - Get supported document formats
- `GET /api/docling/document/{id}` - Get Docling representation of a document

### Import Endpoints
- `POST /api/import/conversation` - Import an AI assistant conversation
- `GET /api/import/formats` - Get supported import formats
- `GET /api/import/conversations` - Get all imported conversations

### Retrieval Endpoints
- `GET /api/thoughts` - Get all thoughts (paginated)
- `GET /api/thoughts/{id}` - Get a specific thought
- `GET /api/thoughts/search` - Search thoughts by keyword
- `GET /api/thoughts/similar/{id}` - Find thoughts similar to a given thought
- `GET /api/projects/{project_id}/thoughts` - Get thoughts for a specific project
- `GET /api/digest/daily` - Get daily thought digest
- `GET /api/digest/weekly` - Get weekly thought digest

### Agent Endpoints
- `POST /api/thoughts/{id}/process` - Manually trigger processing for a thought
- `GET /api/thoughts/{id}/tags` - Get tags for a thought
- `GET /api/thoughts/{id}/links` - Get links for a thought
- `GET /api/thoughts/{id}/actions` - Get actions for a thought

### Management Endpoints
- `GET /api/tags` - Get all tags
- `POST /api/tags` - Create a new tag
- `GET /api/actions` - Get all actions
- `PUT /api/actions/{id}` - Update an action
- `GET /api/stats` - Get system statistics

## Agent Workflows

### Thought Processing Workflow
1. User captures a thought via voice, text, or document
2. System saves raw thought data to database
3. If voice, Transcription Service converts to text
4. If document, Docling parses and extracts content
5. Embedding Generator creates vector embedding
6. Agent Orchestrator queues thought for processing
7. Tagging Agent analyzes and assigns tags
8. Linking Agent finds connections to other thoughts
9. Action Agent extracts potential tasks
10. System updates thought record with all agent results
11. Mobile app receives notification of completed processing

### Import Workflow
1. User uploads AI assistant conversation file
2. System identifies format (markdown or JSON)
3. Import Service parses conversation
4. System extracts individual messages and metadata
5. Each message is processed as a separate thought
6. Thoughts are linked to the original conversation
7. Normal thought processing workflow is triggered for each thought

### Reflection Generation Workflow
1. Scheduled job triggers daily/weekly reflection
2. System collects recent thoughts and metadata
3. Reflection Agent analyzes thoughts for patterns
4. System generates digest with insights and summaries
5. Digest is stored in database and available via API
6. Mobile app displays digest in Daily Mirror view

### Search Workflow
1. User enters search query in mobile app
2. Query is sent to Search Service
3. Service performs keyword and semantic search
4. Results are ranked by relevance
5. Mobile app displays search results
6. User can filter results by tag, date, source, etc.

## Technology Stack

### Backend
- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Database**: PostgreSQL or SQLite
- **Vector Database**: Chroma
- **AI**: OpenAI API (GPT-4, Whisper)
- **Document Processing**: Docling
- **Agent Framework**: LangChain or custom with OpenAI Assistants API
- **Authentication**: JWT
- **Deployment**: Docker, AWS/GCP/Azure

### Mobile App
- **Framework**: React Native + Expo or SwiftUI
- **State Management**: Redux or Context API
- **UI Components**: Custom or Material UI
- **Local Storage**: SQLite
- **Audio Recording**: Expo Audio or AVFoundation
- **Document Scanning**: React Native Camera or AVFoundation

## Security Considerations

- **Data Encryption**: All data encrypted at rest and in transit
- **Authentication**: Secure user authentication with JWT
- **API Security**: Rate limiting, input validation, CORS
- **Privacy**: All processing done on server, no third-party data sharing
- **Backup**: Regular database backups

## Scalability Considerations

- **Database Sharding**: For handling large volumes of thoughts
- **Caching**: Redis for caching frequent queries
- **Async Processing**: Queue-based processing for agents
- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Cost Optimization**: Batched AI API calls to reduce costs
