"""
Tests for the AI Engine module.
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.ai_engine import AIEngine
from core.config_manager import ConfigManager


class TestAIEngine:
    """Test cases for the AI Engine."""
    
    @pytest.fixture
    def mock_config_manager(self):
        """Create a mock configuration manager."""
        mock_config = Mock(spec=ConfigManager)
        mock_config.get_config.return_value = {
            'model': {
                'name': 'microsoft/DialoGPT-small',
                'temperature': 0.7,
                'top_p': 0.9,
                'max_length': 1024,
                'device': 'cpu'
            },
            'inference': {
                'max_new_tokens': 128,
                'do_sample': True
            }
        }
        return mock_config
    
    @patch('core.ai_engine.torch')
    @patch('core.ai_engine.AutoTokenizer')
    @patch('core.ai_engine.AutoModelForCausalLM')
    def test_ai_engine_initialization(self, mock_model, mock_tokenizer, mock_torch, mock_config_manager):
        """Test AI engine initialization."""
        # Mock torch components
        mock_torch.cuda.is_available.return_value = False
        mock_torch.backends.mps.is_available.return_value = False
        
        # Mock model and tokenizer
        mock_tokenizer.from_pretrained.return_value = Mock()
        mock_model.from_pretrained.return_value = Mock()
        
        # Initialize AI engine
        ai_engine = AIEngine(mock_config_manager)
        
        assert ai_engine.config_manager == mock_config_manager
        assert ai_engine.device == 'cpu'
    
    def test_fallback_response(self, mock_config_manager):
        """Test fallback response system."""
        with patch('core.ai_engine.torch'), \
             patch('core.ai_engine.AutoTokenizer'), \
             patch('core.ai_engine.AutoModelForCausalLM'):
            
            ai_engine = AIEngine(mock_config_manager)
            # Force fallback mode
            ai_engine.model = None
            ai_engine.tokenizer = None
            
            # Test greeting response
            response = ai_engine.generate_response("hello")
            assert "Hello" in response
            assert "personal AI assistant" in response.lower()
            
            # Test capabilities question
            response = ai_engine.generate_response("what can you do?")
            assert "development" in response.lower()
    
    def test_empty_input_handling(self, mock_config_manager):
        """Test handling of empty input."""
        with patch('core.ai_engine.torch'), \
             patch('core.ai_engine.AutoTokenizer'), \
             patch('core.ai_engine.AutoModelForCausalLM'):
            
            ai_engine = AIEngine(mock_config_manager)
            
            response = ai_engine.generate_response("")
            assert "didn't catch that" in response.lower()
            
            response = ai_engine.generate_response("   ")
            assert "didn't catch that" in response.lower()
    
    def test_get_model_info_fallback(self, mock_config_manager):
        """Test model info in fallback mode."""
        with patch('core.ai_engine.torch'), \
             patch('core.ai_engine.AutoTokenizer'), \
             patch('core.ai_engine.AutoModelForCausalLM'):
            
            ai_engine = AIEngine(mock_config_manager)
            ai_engine.model = None  # Force fallback
            
            info = ai_engine.get_model_info()
            assert info['status'] == 'fallback'
            assert info['model_name'] == 'none'