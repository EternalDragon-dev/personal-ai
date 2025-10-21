"""
API Server - FastAPI server for the Personal AI system.

This module provides REST API endpoints for interacting with the AI engine.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from loguru import logger
import time

from core.ai_engine import AIEngine


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[float] = None


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    timestamp: float
    model_info: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: float
    version: str
    model_status: str


def create_app(ai_engine: AIEngine) -> FastAPI:
    """Create and configure the FastAPI application.
    
    Args:
        ai_engine: Initialized AI engine instance
        
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="Personal AI API",
        description="REST API for the Personal AI system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Get CORS origins from AI engine config
    cors_origins = ai_engine.config.get('api', {}).get('cors_origins', ["*"])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/", response_model=Dict[str, str])
    async def root():
        """Root endpoint."""
        return {
            "message": "Personal AI API",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        model_info = ai_engine.get_model_info()
        
        return HealthResponse(
            status="healthy",
            timestamp=time.time(),
            version="1.0.0",
            model_status=model_info.get("status", "unknown")
        )
    
    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        """Chat endpoint for conversing with the AI.
        
        Args:
            request: Chat request containing message and optional history
            
        Returns:
            AI response with metadata
        """
        try:
            # Extract conversation history
            history = []
            if request.conversation_history:
                for msg in request.conversation_history[-10:]:  # Last 10 messages
                    history.append(f"{msg.role}: {msg.content}")
            
            # Generate response
            response = ai_engine.generate_response(
                request.message,
                conversation_history=history
            )
            
            # Get model info
            model_info = ai_engine.get_model_info()
            
            return ChatResponse(
                response=response,
                timestamp=time.time(),
                model_info=model_info
            )
            
        except Exception as e:
            logger.error(f"Chat API error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/model/info", response_model=Dict[str, Any])
    async def get_model_info():
        """Get information about the loaded AI model."""
        try:
            return ai_engine.get_model_info()
        except Exception as e:
            logger.error(f"Model info API error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/model/clear-cache")
    async def clear_model_cache():
        """Clear model cache (useful for GPU memory management)."""
        try:
            ai_engine.clear_cache()
            return {"status": "success", "message": "Cache cleared"}
        except Exception as e:
            logger.error(f"Clear cache API error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/config", response_model=Dict[str, Any])
    async def get_config():
        """Get current configuration (excluding sensitive data)."""
        try:
            config = ai_engine.config_manager.get_config().copy()
            
            # Remove sensitive sections
            config.pop('privacy', None)
            
            return config
        except Exception as e:
            logger.error(f"Config API error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        """Custom 404 handler."""
        return {
            "error": "Not found",
            "message": f"The endpoint {request.url.path} was not found",
            "available_endpoints": [
                "/",
                "/health",
                "/chat",
                "/model/info",
                "/model/clear-cache",
                "/config",
                "/docs"
            ]
        }
    
    return app