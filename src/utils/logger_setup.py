"""
Logger Setup - Configures logging for the Personal AI system.

This module sets up structured logging using loguru with file rotation
and configurable levels.
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]):
    """Setup logging configuration based on config.
    
    Args:
        config: Configuration dictionary containing logging settings
    """
    # Remove default logger
    logger.remove()
    
    # Get logging configuration
    logging_config = config.get('logging', {})
    log_level = logging_config.get('level', 'INFO')
    log_format = logging_config.get('format', 
                                   '{time} | {level} | {name}:{function}:{line} - {message}')
    
    # Console logging
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # File logging
    paths_config = config.get('paths', {})
    logs_dir = Path(paths_config.get('logs_dir', './logs'))
    logs_dir.mkdir(exist_ok=True, parents=True)
    
    # Main log file with rotation
    logger.add(
        logs_dir / "personal_ai.log",
        format=log_format,
        level=log_level,
        rotation=logging_config.get('file_rotation', '1 day'),
        retention=logging_config.get('file_retention', '30 days'),
        compression="gz",
        backtrace=True,
        diagnose=True
    )
    
    # Error log file
    logger.add(
        logs_dir / "errors.log",
        format=log_format,
        level="ERROR",
        rotation="1 week",
        retention="60 days",
        compression="gz",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logging configured successfully")