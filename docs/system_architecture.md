# Mirza Mirror: System Architecture

## Overview

Mirza Mirror is an AI-powered thought externalization system designed to capture, organize, and retrieve thoughts across different formats. The system consists of several interconnected components that work together to provide a seamless experience for the user.

## System Components

### 1. Capture Service
Responsible for collecting thoughts from various sources and formats.

- **Voice Capture**: Records and processes voice notes from iPhone
- **Text Capture**: Collects text notes from iPhone
- **Import Service**: Imports existing notes and conversations from other platforms

### 2. Processing Service
Transforms raw input into structured thought data.

- **Transcription Service**: Uses OpenAI Whisper to convert voice to text
- **Preprocessing Pipeline**: Cleans and normalizes text data
- **Embedding Generator**: Creates vector embeddings for semantic search

### 3. Memory Store
Central database for storing all thought data and metadata.

- **Relational Database**: Stores structured thought data and metadata (PostgreSQL/SQLite)
- **Vector Database**: Stores embeddings for semantic search (Chroma)
- **File Storage**: Stores original audio files and other binary data

### 4. Agent Orchestrator
Manages the AI agents that process and organize thoughts.

- **Agent Manager**: Coordinates agent workflows and schedules processing
- **Context Provider**: Supplies relevant context to agents for processing
- **Result Integrator**: Incorporates agent outputs back into the memory store

### 5. Agent Services
Specialized AI services that process thoughts in different ways.

- **Tagging Agent**: Classifies thoughts by project, emotion, category
- **Linking Agent**: Identifies connections between thoughts
- **Reflection Agent**: Generates insights and identifies patterns
- **Action Agent**: Extracts tasks and action items

### 6. Retrieval Service
Provides access to stored thoughts and generated insights.

- **Search Service**: Enables keyword and semantic search
- **Digest Generator**: Creates daily/weekly summaries of important thoughts
- **Project View Service**: Organizes thoughts by project or category
- **Pattern Recognition**: Identifies recurring themes and patterns

### 7. API Layer
Exposes system functionality to the frontend application.

- **REST API**: Provides endpoints for all system functions
- **WebSocket Service**: Enables real-time updates and notifications
- **Authentication Service**: Manages user authentication and security

### 8. Mobile Application
iPhone app that serves as the primary user interface.

- **Capture Interface**: UI for recording voice and text notes
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
  "source": "voice_note|text_note|chat|import",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "audio_file": "path/to/audio.mp3",  // if source is voice_note
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
- `POST /api/import` - Import thoughts from external sources

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
1. User captures a thought via voice or text
2. System saves raw thought data to database
3. If voice, Transcription Service converts to text
4. Embedding Generator creates vector embedding
5. Agent Orchestrator queues thought for processing
6. Tagging Agent analyzes and assigns tags
7. Linking Agent finds connections to other thoughts
8. Action Agent extracts potential tasks
9. System updates thought record with all agent results
10. Mobile app receives notification of completed processing

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
- **Agent Framework**: LangChain or custom with OpenAI Assistants API
- **Authentication**: JWT
- **Deployment**: Docker, AWS/GCP/Azure

### Mobile App
- **Framework**: React Native + Expo or SwiftUI
- **State Management**: Redux or Context API
- **UI Components**: Custom or Material UI
- **Local Storage**: SQLite
- **Audio Recording**: Expo Audio or AVFoundation

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
