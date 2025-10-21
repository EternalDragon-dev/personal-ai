"""
Configuration Manager - Handles configuration loading and management.

This module provides centralized configuration management for the Personal AI system.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self._config = None
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as file:
                    self._config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Config file not found: {self.config_path}, using defaults")
                self._config = self._get_default_config()
                
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration when config file is not available."""
        return {
            'model': {
                'name': 'microsoft/DialoGPT-small',
                'architecture': 'transformer',
                'max_length': 1024,
                'temperature': 0.7,
                'top_p': 0.9,
                'device': 'auto'
            },
            'training': {
                'batch_size': 4,
                'learning_rate': 5e-5,
                'num_epochs': 3,
                'warmup_steps': 500,
                'gradient_checkpointing': True,
                'mixed_precision': True
            },
            'data': {
                'max_samples': 10000,
                'validation_split': 0.1,
                'preprocessing': {
                    'lowercase': False,
                    'remove_special_chars': False,
                    'max_token_length': 512
                }
            },
            'inference': {
                'batch_size': 1,
                'beam_size': 1,
                'max_new_tokens': 128,
                'do_sample': True,
                'early_stopping': True
            },
            'paths': {
                'data_dir': './data',
                'model_dir': './models',
                'logs_dir': './logs',
                'cache_dir': './cache'
            },
            'api': {
                'host': '0.0.0.0',
                'port': 8000,
                'cors_origins': ['http://localhost:3000']
            },
            'logging': {
                'level': 'INFO',
                'format': '{time} | {level} | {name}:{function}:{line} - {message}',
                'file_rotation': '1 day',
                'file_retention': '30 days'
            },
            'privacy': {
                'local_processing': True,
                'data_encryption': False,
                'anonymize_logs': True,
                'retention_days': 90
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get a specific configuration section.
        
        Args:
            section: Name of the configuration section
            
        Returns:
            Configuration section dictionary
        """
        return self._config.get(section, {})
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to the configuration value (e.g., 'model.temperature')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_value(self, key_path: str, value: Any):
        """Set a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to the configuration value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self._config
        
        # Navigate to the parent dictionary
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key_path} = {value}")
    
    def save_config(self, config_path: Optional[str] = None):
        """Save current configuration to file.
        
        Args:
            config_path: Optional path to save config, uses default if None
        """
        save_path = Path(config_path) if config_path else self.config_path
        
        try:
            # Ensure directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w') as file:
                yaml.dump(self._config, file, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def reload_config(self):
        """Reload configuration from file."""
        logger.info("Reloading configuration...")
        self._load_config()
    
    def validate_config(self) -> bool:
        """Validate the current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_sections = ['model', 'inference', 'paths', 'api', 'logging']
        
        for section in required_sections:
            if section not in self._config:
                logger.error(f"Missing required configuration section: {section}")
                return False
        
        # Validate specific values
        if self._config['model']['temperature'] < 0 or self._config['model']['temperature'] > 2:
            logger.error("Model temperature must be between 0 and 2")
            return False
        
        if self._config['api']['port'] < 1 or self._config['api']['port'] > 65535:
            logger.error("API port must be between 1 and 65535")
            return False
        
        logger.info("Configuration validation passed")
        return True
    
    def get_env_override(self, key_path: str, env_var: str) -> Any:
        """Get configuration value with environment variable override.
        
        Args:
            key_path: Dot-separated path to the configuration value
            env_var: Environment variable name
            
        Returns:
            Environment variable value if set, otherwise configuration value
        """
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Try to convert to appropriate type
            config_value = self.get_value(key_path)
            if isinstance(config_value, bool):
                return env_value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(config_value, int):
                return int(env_value)
            elif isinstance(config_value, float):
                return float(env_value)
            else:
                return env_value
        
        return self.get_value(key_path)