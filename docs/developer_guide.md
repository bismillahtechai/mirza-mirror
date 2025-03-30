# Mirza Mirror Developer Guide

## Introduction

This guide provides information for developers who want to contribute to or extend the Mirza Mirror thought externalization system. It covers the system architecture, development setup, and guidelines for contributing to the project.

## System Architecture

Mirza Mirror follows a modern, modular architecture with these key components:

### Backend (FastAPI)

The backend is built with FastAPI and provides a RESTful API for all operations. Key components include:

1. **Memory Module**: Integrates with mem0 for intelligent memory management
   - `memory_engine.py`: Core memory operations
   - `search.py`: Advanced memory search capabilities

2. **Docling Module**: Handles document processing and analysis
   - `parser.py`: Document parsing for various formats
   - `ocr.py`: Optical character recognition for images

3. **Capture Module**: Processes text and voice thoughts
   - Handles transcription via Whisper API
   - Manages thought metadata and storage

4. **Agent Services**: OpenAI Agents with MCP integration
   - Tagging Agent: Categorizes thoughts
   - Linking Agent: Connects related thoughts
   - Reflection Agent: Generates insights and emotional context
   - Action Agent: Extracts actionable items

5. **Import Module**: Handles importing conversations from AI assistants
   - Supports ChatGPT, Claude, and Gemini
   - Handles both markdown and JSON formats

6. **API Layer**: RESTful endpoints for all operations
   - Follows standard REST conventions
   - Includes comprehensive validation and error handling

### Frontend Applications

1. **iOS App (Swift/SwiftUI)**
   - Native iOS application
   - Follows MVVM architecture
   - Includes voice recording capabilities

2. **Android App (Kotlin/Jetpack Compose)**
   - Native Android application
   - Follows MVVM architecture
   - Material Design 3 components

3. **Web App (React/Next.js)**
   - Modern React application with Next.js
   - Responsive design with Tailwind CSS
   - Progressive Web App capabilities

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- Docker and Docker Compose
- OpenAI API key
- Xcode (for iOS development)
- Android Studio (for Android development)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mirza-mirror.git
   cd mirza-mirror
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./mirza_mirror.db
   ENVIRONMENT=development
   LOG_LEVEL=debug
   CORS_ORIGINS=http://localhost:3000
   ```

5. Run the application:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

### Docker Setup

Alternatively, you can use Docker Compose:

1. Create a `.env` file in the root directory with your OpenAI API key.

2. Start the application:
   ```bash
   docker-compose up
   ```

### Web App Setup

1. Navigate to the web app directory:
   ```bash
   cd mobile/web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### iOS App Setup

1. Open the Xcode project:
   ```bash
   open mobile/ios/MirzaMirror/MirzaMirror.xcodeproj
   ```

2. Update the API URL in `APIService.swift` if needed.

3. Build and run the app in the simulator.

### Android App Setup

1. Open the project in Android Studio:
   ```bash
   cd mobile/android
   ```

2. Update the API URL in `ApiService.kt` if needed.

3. Build and run the app in the emulator.

## Code Structure

```
mirza_mirror/
│
├── app/                        # FastAPI backend
│   ├── main.py                 # App entry point
│   ├── api/                    # API routes
│   │   ├── capture.py
│   │   ├── search.py
│   │   └── agents.py
│   ├── services/               # Core logic
│   │   ├── transcription.py    # Whisper integration
│   │   ├── tagging_agent.py
│   │   ├── reflection_agent.py
│   │   ├── action_agent.py
│   │   └── linking_agent.py
│   ├── memory/                 # mem0 integration
│   │   ├── memory_engine.py
│   │   └── search.py
│   ├── docling/                # Docling integration
│   │   ├── parser.py
│   │   └── ocr.py
│   ├── models/                 # Pydantic models / schemas
│   │   ├── thought.py
│   │   ├── document.py
│   │   └── user.py
│   ├── db/                     # DB and storage layer
│   │   ├── database.py
│   │   └── schema.sql
│   └── utils/                  # Helper functions
│       └── logger.py
│
├── mobile/                     # Mobile apps
│   ├── ios/                    # iOS App (Swift/SwiftUI)
│   ├── android/                # Android App (Kotlin/Jetpack Compose)
│   └── web/                    # Web App (React/Next.js)
│
├── tests/                      # Test files
│   ├── test_agents.py
│   ├── test_memory.py
│   └── test_api.py
│
├── scripts/                    # One-off scripts
│   ├── import_chatgpt.py
│   └── convert_voice.py
│
├── docs/                       # Documentation
│   ├── user_guide.md
│   ├── api_documentation.md
│   ├── developer_guide.md
│   └── deployment_guide.md
│
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration
└── render.yaml                 # Render deployment configuration
```

## Development Guidelines

### Code Style

- Backend: Follow PEP 8 guidelines
- iOS: Follow Swift style guide
- Android: Follow Kotlin style guide
- Web: Follow ESLint configuration

### Testing

- Write unit tests for all new functionality
- Run tests before submitting pull requests:
  ```bash
  cd tests
  python -m unittest discover
  ```

### Git Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request on GitHub.

## API Integration

See the [API Documentation](api_documentation.md) for details on integrating with the Mirza Mirror API.

## Extending the System

### Adding a New Agent

1. Create a new agent class in `app/services/`:
   ```python
   class NewAgent:
       def __init__(self):
           # Initialize agent
           pass
           
       def process(self, input_data):
           # Process input data
           return result
   ```

2. Add the agent to the `AgentService` class in `app/agents.py`.

3. Create an API endpoint in `app/api/agents.py`.

4. Add tests for the new agent in `tests/test_agent_service.py`.

### Adding a New Frontend Feature

1. Identify which platforms need the feature (iOS, Android, Web).

2. Implement the feature in each platform following their respective patterns.

3. Update the API if necessary to support the new feature.

4. Add tests for the new feature.

5. Update documentation to reflect the new feature.

## Troubleshooting

### Common Development Issues

#### Backend Issues

- **Database connection errors**: Check your DATABASE_URL in the .env file.
- **OpenAI API errors**: Verify your API key and check OpenAI service status.
- **Import errors**: Ensure your Python path includes the app directory.

#### Frontend Issues

- **API connection errors**: Check the API URL in the frontend configuration.
- **Build errors**: Ensure all dependencies are installed correctly.
- **iOS simulator issues**: Try resetting the simulator or cleaning the build.

### Getting Help

- Create an issue on GitHub
- Contact the development team at dev@mirzamirror.com
