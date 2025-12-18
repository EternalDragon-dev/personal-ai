# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Setup & Installation
```bash
make install          # Install basic dependencies
make dev-install      # Install dev dependencies + setup pre-commit hooks
make setup-dev        # Complete development environment setup
```

### Running the Application
```bash
make run              # Start interactive AI assistant mode
make run-api          # Start FastAPI server mode
make run-verbose      # Run with verbose debug logging
python3 src/main.py --mode interactive --config config/config.yaml
python3 src/main.py --mode api --verbose
```

### Testing & Quality
```bash
make test             # Run pytest test suite
make test-cov         # Run tests with HTML coverage report
make lint             # Run black, flake8, and mypy checks
make format           # Auto-format code with black and isort
make check            # Run both lint and test
pytest tests/test_ai_engine.py -v  # Run single test file
```

### Maintenance
```bash
make clean            # Remove __pycache__, .pytest_cache, build artifacts
```

## Architecture Overview

### Core Components
- **AIEngine** (`src/core/ai_engine.py`) - Main AI processing engine with transformer model loading, fallback responses, and device detection (CUDA/MPS/CPU)
- **ConfigManager** (`src/core/config_manager.py`) - Centralized configuration management with YAML loading, dot-notation access, and environment variable overrides
- **FastAPI Server** (`src/api/server.py`) - REST API with chat endpoints, health checks, and CORS middleware

### Application Flow
The system initializes through `PersonalAI` class in `main.py`, which:
1. Loads configuration via ConfigManager
2. Sets up logging with loguru and file rotation
3. Initializes AIEngine with model loading and fallback handling
4. Starts either interactive CLI mode or API server mode

### Key Design Patterns
- **Graceful Degradation**: AIEngine falls back to keyword-based responses if model loading fails
- **Device Auto-Detection**: Automatically selects CUDA, MPS, or CPU based on availability
- **Modular Configuration**: YAML-based config with programmatic overrides and validation
- **Structured Logging**: loguru with file rotation, error-only logs, and compression

### Model Management
- Default model: `microsoft/DialoGPT-small` (configurable)
- Supports GPU acceleration with automatic device selection
- Implements conversation history context (last 5 exchanges)
- Includes cache clearing for GPU memory management

### API Design
- RESTful endpoints: `/chat`, `/health`, `/model/info`, `/config`
- Pydantic models for request/response validation
- Built-in CORS and error handling
- Conversation history support in chat requests

## Configuration

The system uses `config/config.yaml` for all settings. Key sections:
- **model**: Model name, temperature, device settings
- **inference**: Generation parameters, token limits
- **api**: Server host, port, CORS origins  
- **logging**: Levels, formats, file rotation
- **paths**: Data, model, logs, cache directories

Environment variables can override config values using dot notation (e.g., `MODEL_TEMPERATURE` overrides `model.temperature`).

## Testing Strategy

- **Unit tests**: Focus on AIEngine with mocked dependencies
- **Fallback testing**: Verify graceful degradation without model loading
- **Configuration testing**: Validate config loading and defaults
- **Coverage target**: 70% minimum (configured in pytest.ini)
- **Markers**: `slow`, `integration`, `unit` for test categorization

## Key Dependencies

- **AI/ML**: PyTorch, Transformers, sentence-transformers
- **Vector DBs**: Faiss, ChromaDB, Pinecone
- **API**: FastAPI, Uvicorn, Pydantic
- **Development**: Black, flake8, mypy, pre-commit
- **Logging**: loguru with structured output