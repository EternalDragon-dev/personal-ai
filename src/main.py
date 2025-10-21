#!/usr/bin/env python3
"""
Personal AI - Main Application Entry Point

This is the main entry point for the Personal AI system.
It initializes the AI core, loads configuration, and starts the application.
"""

import os
import sys
from pathlib import Path
import yaml
import click
from loguru import logger

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.ai_engine import AIEngine
from core.config_manager import ConfigManager
from utils.logger_setup import setup_logging


class PersonalAI:
    """Main Personal AI application class."""
    
    def __init__(self, config_path: str = None):
        """Initialize the Personal AI application.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or "config/config.yaml"
        self.config_manager = ConfigManager(self.config_path)
        self.ai_engine = None
        
        # Setup logging
        setup_logging(self.config_manager.get_config())
        logger.info("Personal AI initializing...")
    
    def initialize(self):
        """Initialize all components of the AI system."""
        try:
            # Initialize AI engine
            self.ai_engine = AIEngine(self.config_manager)
            logger.info("AI Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Personal AI: {e}")
            sys.exit(1)
    
    def start_interactive_mode(self):
        """Start interactive conversation mode."""
        logger.info("Starting interactive mode...")
        print("\\n🤖 Personal AI Assistant")
        print("Type 'quit' or 'exit' to end the session.\\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("AI: Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                response = self.ai_engine.generate_response(user_input)
                print(f"AI: {response}")
                
            except KeyboardInterrupt:
                print("\\n\\nAI: Goodbye! 👋")
                break
            except Exception as e:
                logger.error(f"Error during conversation: {e}")
                print(f"AI: Sorry, I encountered an error: {e}")
    
    def start_api_server(self):
        """Start the API server."""
        from api.server import create_app
        
        config = self.config_manager.get_config()
        app = create_app(self.ai_engine)
        
        import uvicorn
        uvicorn.run(
            app,
            host=config['api']['host'],
            port=config['api']['port'],
            log_level=config['logging']['level'].lower()
        )


@click.command()
@click.option('--config', '-c', default=None, help='Path to configuration file')
@click.option('--mode', '-m', default='interactive', 
              type=click.Choice(['interactive', 'api']), 
              help='Mode to run the application in')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(config, mode, verbose):
    """Personal AI Assistant - Your intelligent companion."""
    
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    
    # Initialize Personal AI
    ai = PersonalAI(config_path=config)
    ai.initialize()
    
    # Start in selected mode
    if mode == 'interactive':
        ai.start_interactive_mode()
    elif mode == 'api':
        ai.start_api_server()


if __name__ == "__main__":
    main()