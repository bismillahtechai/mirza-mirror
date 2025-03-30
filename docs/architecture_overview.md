# Mirza Mirror: System Architecture Overview

This document provides a visual and descriptive overview of the Mirza Mirror thought externalization system architecture.

## Architecture Diagram

![Architecture Diagram](architecture_diagram.md)

## System Components

### Frontend Applications

The system provides native applications for all major platforms:

1. **iOS App (Swift/SwiftUI)**
   - Native iOS application optimized for iPhone and iPad
   - Provides intuitive interface for thought capture and browsing
   - Includes voice recording with visualization
   - Supports offline mode with sync capabilities

2. **Android App (Kotlin/Jetpack Compose)**
   - Native Android application following Material Design 3 guidelines
   - Implements MVVM architecture pattern
   - Provides feature parity with iOS application
   - Optimized for various Android device sizes

3. **Web App (React/Next.js)**
   - Progressive Web App built with React and Next.js
   - Responsive design using Tailwind CSS
   - Provides core functionality accessible from any browser
   - Optimized for both desktop and mobile web experiences

### Backend API (FastAPI)

The backend is built with FastAPI and provides a RESTful API for all operations:

1. **API Layer**
   - RESTful endpoints for all system operations
   - Authentication and authorization
   - Request validation and error handling
   - Rate limiting and monitoring

2. **Memory Module**
   - Integration with mem0 for intelligent memory management
   - Vector database for semantic search capabilities
   - Relational database for structured data storage
   - Memory retrieval, storage, and search operations

3. **Docling Module**
   - Document parsing and processing
   - OCR for extracting text from images
   - Metadata extraction from various document formats
   - Integration with Docling service for linguistic analysis

4. **Capture Module**
   - Text thought processing
   - Voice recording and transcription via Whisper
   - Thought metadata management
   - Integration with agent services for enrichment

5. **Import Module**
   - Conversation import from various AI assistants
   - Support for both markdown and JSON formats
   - Parsing and normalization of different conversation structures
   - Integration with memory module for storage

6. **Agent Services**
   - Tagging Agent: Categorizes thoughts using AI
   - Linking Agent: Connects related thoughts
   - Reflection Agent: Generates insights and emotional context
   - Action Agent: Extracts actionable items from thoughts
   - Each agent has a dedicated MCP server for context management

### External Services

The system integrates with several external services:

1. **OpenAI API**
   - Used for AI agent capabilities
   - Provides embedding generation for vector search
   - Powers Whisper transcription for voice notes
   - Enables semantic understanding of thought content

2. **mem0 Memory System**
   - Provides intelligent memory management
   - Enables contextual retrieval of thoughts
   - Supports semantic search capabilities
   - Manages memory persistence and retrieval

3. **Docling Service**
   - Provides linguistic document processing
   - Enables metadata extraction from documents
   - Supports OCR for image-based documents
   - Assists with document categorization and analysis

## Data Flow

1. **Thought Capture Flow**
   - User inputs thought via text, voice, or document
   - Backend processes input (transcribes voice if needed)
   - Agents enrich thought with tags, links, reflections, and actions
   - Enriched thought is stored in memory system
   - Response is sent back to client application

2. **Thought Retrieval Flow**
   - User searches for thoughts or browses by category
   - Query is processed by memory module
   - Relevant thoughts are retrieved and ranked
   - Results are returned to client application
   - User can view detailed thought information

3. **Import Flow**
   - User uploads conversation export file
   - Import module parses the file based on format and source
   - Conversations are processed into individual thoughts
   - Thoughts are enriched by agent services
   - Processed thoughts are stored in memory system

## Deployment Architecture

The system is deployed on Render with the following components:

1. **API Service**
   - Hosts the FastAPI backend
   - Scales based on demand
   - Connects to database service

2. **Web Service**
   - Hosts the Next.js web application
   - Serves static assets
   - Communicates with API service

3. **Database Service**
   - PostgreSQL database for relational data
   - Managed by Render for reliability and backups

4. **Vector Database**
   - Integrated with the API service
   - Stores vector embeddings for semantic search

For local development, Docker Compose is used to replicate the production environment with all necessary services.
