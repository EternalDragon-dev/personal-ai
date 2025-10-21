"""
AI Engine - Core AI functionality for the Personal AI system.

This module handles the main AI operations including model loading,
inference, and response generation.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from loguru import logger
from typing import Optional, Dict, Any
import time

from .config_manager import ConfigManager


class AIEngine:
    """Main AI engine for processing and generating responses."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the AI engine with configuration.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.config = config_manager.get_config()
        
        self.tokenizer = None
        self.model = None
        self.device = self._get_device()
        
        self._load_model()
        logger.info("AI Engine initialized successfully")
    
    def _get_device(self) -> str:
        """Determine the best device to use for inference."""
        device_config = self.config['model']['device']
        
        if device_config == "auto":
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
        else:
            device = device_config
        
        logger.info(f"Using device: {device}")
        return device
    
    def _load_model(self):
        """Load the AI model and tokenizer."""
        try:
            model_name = self.config['model'].get('name', 'microsoft/DialoGPT-small')
            
            logger.info(f"Loading model: {model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                low_cpu_mem_usage=True
            )
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Fallback to a simple response system
            self._setup_fallback_system()
    
    def _setup_fallback_system(self):
        """Setup a fallback system when model loading fails."""
        logger.warning("Setting up fallback response system")
        self.model = None
        self.tokenizer = None
        
        self.fallback_responses = [
            "I'm currently in development mode. How can I help you today?",
            "I'm learning and growing! What would you like to discuss?",
            "I'm here to assist you. What's on your mind?",
            "Thank you for your patience as I develop my capabilities.",
        ]
    
    def generate_response(self, user_input: str, conversation_history: list = None) -> str:
        """Generate a response to user input.
        
        Args:
            user_input: The user's input text
            conversation_history: Optional conversation history
            
        Returns:
            Generated response string
        """
        if not user_input.strip():
            return "I didn't catch that. Could you please repeat?"
        
        try:
            if self.model is None:
                return self._fallback_response(user_input)
            
            return self._generate_model_response(user_input, conversation_history)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error. Please try again."
    
    def _fallback_response(self, user_input: str) -> str:
        """Generate a fallback response when model is not available."""
        import random
        
        # Simple keyword-based responses
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your personal AI assistant. How can I help you today?"
        elif any(word in user_lower for word in ['how are you', 'how do you feel']):
            return "I'm doing well, thank you for asking! I'm here and ready to help."
        elif any(word in user_lower for word in ['what can you do', 'help', 'capabilities']):
            return "I'm currently in development, but I'm designed to be your personal AI assistant. I can chat with you and help with various tasks as I continue to learn!"
        else:
            return random.choice(self.fallback_responses)
    
    def _generate_model_response(self, user_input: str, conversation_history: list = None) -> str:
        """Generate response using the loaded model."""
        # Prepare input
        if conversation_history:
            # Include conversation context
            context = " ".join(conversation_history[-5:])  # Last 5 exchanges
            full_input = f"{context} {user_input}"
        else:
            full_input = user_input
        
        # Tokenize input
        inputs = self.tokenizer.encode(
            full_input, 
            return_tensors="pt", 
            max_length=self.config['model']['max_length'],
            truncation=True
        ).to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=self.config['inference']['max_new_tokens'],
                temperature=self.config['model']['temperature'],
                top_p=self.config['model']['top_p'],
                do_sample=self.config['inference']['do_sample'],
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode response
        response = self.tokenizer.decode(
            outputs[0][inputs.shape[1]:], 
            skip_special_tokens=True
        ).strip()
        
        return response if response else "I'm not sure how to respond to that."
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self.model is None:
            return {"status": "fallback", "model_name": "none"}
        
        return {
            "status": "loaded",
            "model_name": self.config['model'].get('name'),
            "device": self.device,
            "parameters": sum(p.numel() for p in self.model.parameters()),
        }
    
    def clear_cache(self):
        """Clear GPU cache if using CUDA."""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            logger.info("GPU cache cleared")