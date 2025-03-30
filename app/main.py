"""
Main application module for Mirza Mirror.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.db.database import init_db, get_db
from app.api import memory, document, documents, import_conversation, capture, agents
from app.utils.logger import log_info

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Mirza Mirror API",
    description="API for Mirza Mirror thought externalization system",
    version="0.1.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(memory.router)
app.include_router(document.router)
app.include_router(documents.router)
app.include_router(import_conversation.router)
app.include_router(capture.router)
app.include_router(agents.router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    log_info("Starting Mirza Mirror API")
    init_db()

@app.get("/")
async def root():
    """
    Root endpoint for health check.
    """
    return {
        "status": "ok",
        "message": "Mirza Mirror API is running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "memory": "operational",
            "document": "operational",
            "import": "operational",
            "capture": "operational",
            "agents": "operational"
        }
    }
