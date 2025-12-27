# Personal AI Framework

> Build your own personalized AI assistant with custom models, RAG, and conversation memory

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[**📸 Screenshot Coming Soon**]

## Overview

A modular framework for building personalized AI assistants from scratch. Supports custom model training, retrieval-augmented generation (RAG), conversation memory, and extensible plugin architecture.

**Perfect for:**
- Learning how AI assistants work under the hood
- Building custom AI solutions for personal use
- Experimenting with different AI models and techniques
- Privacy-focused AI with local processing

## Features

- 🤖 **Custom AI Engine** - Integrate any model (HuggingFace, OpenAI, Ollama)
- 💾 **Conversation Memory** - Persistent context across sessions
- 📚 **RAG Support** - Retrieval-augmented generation for knowledge bases
- 🔌 **Plugin Architecture** - Extensible with custom tools and skills
- 🎯 **CLI Interface** - Simple command-line interaction
- 🛡️ **Privacy-First** - Local processing option, no data leaks
- ⚙️ **Modular Design** - Easy to customize and extend

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Ollama for local AI models

### Installation

1. **Clone and navigate:**
   ```bash
   cd personal-ai
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the CLI:**
   ```bash
   python src/cli.py
   ```

### First Conversation

```bash
$ python src/cli.py

🤖 Personal AI - Ready to chat!
Type 'exit' to quit, 'clear' to reset conversation

You: Hello! What can you do?
AI: I'm your personal AI assistant. I can help with...

You: Tell me about Python
AI: Python is a high-level programming language...
```

## Architecture

```
personal-ai/
├── src/
│   ├── core/
│   │   ├── ai_engine.py      # Core AI model integration
│   │   ├── memory.py          # Conversation memory manager
│   │   └── embeddings.py      # Text embeddings for RAG
│   ├── models/
│   │   ├── base.py            # Base model interface
│   │   ├── ollama.py          # Ollama integration
│   │   └── openai.py          # OpenAI integration
│   ├── data/
│   │   ├── processor.py       # Data preprocessing
│   │   └── vectorstore.py     # Vector database
│   ├── utils/
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging utilities
│   ├── cli.py                 # Command-line interface
│   └── main.py                # Main application
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── config/
│   └── default.yaml           # Default configuration
├── data/                      # User data & documents
├── models/                    # Downloaded model files
└── logs/                      # Application logs
```

## Usage Examples

### Basic Chat

```python
from src.core.ai_engine import AIEngine

engine = AIEngine(model="ollama/llama2")
response = engine.chat("What is machine learning?")
print(response)
```

### Conversation with Memory

```python
from src.core.ai_engine import AIEngine
from src.core.memory import ConversationMemory

memory = ConversationMemory()
engine = AIEngine(memory=memory)

engine.chat("My name is John")
engine.chat("What's my name?")  # AI remembers context
```

### RAG with Documents

```python
from src.core.ai_engine import AIEngine
from src.data.vectorstore import VectorStore

vectorstore = VectorStore()
vectorstore.add_documents(["path/to/docs"])

engine = AIEngine(vectorstore=vectorstore)
response = engine.chat("Summarize the documentation")
```

## Configuration

### AI Model Settings

Edit `config/default.yaml`:

```yaml
ai:
  provider: ollama  # Options: ollama, openai, huggingface
  model: llama2
  temperature: 0.7
  max_tokens: 500

memory:
  enabled: true
  max_history: 10
  
rag:
  enabled: false
  chunk_size: 500
  overlap: 50
```

### Environment Variables

```bash
# For OpenAI (if using)
export OPENAI_API_KEY=your_key_here

# For HuggingFace (if using)
export HUGGINGFACE_TOKEN=your_token_here
```

## Tech Stack

- **Language:** Python 3.8+
- **AI Integration:** HuggingFace Transformers, OpenAI API, Ollama
- **Embeddings:** Sentence Transformers
- **Vector Store:** ChromaDB / FAISS
- **CLI:** Click / argparse
- **Testing:** pytest

## Project Status

- [x] Project structure and architecture
- [x] Configuration system
- [x] Logging utilities
- [ ] **Core AI engine** (IN PROGRESS)
- [ ] Conversation memory
- [ ] RAG implementation
- [ ] CLI interface
- [ ] Plugin system
- [ ] Web interface
- [ ] Documentation

## Roadmap

### Phase 1: Core Functionality (Current)
- Implement AI engine with model loading
- Add basic conversation memory
- Create functional CLI

### Phase 2: Advanced Features
- RAG with document ingestion
- Plugin architecture
- Multiple model support

### Phase 3: Polish
- Web interface
- Model fine-tuning tools
- Comprehensive documentation

## Development

### Run in development mode:
```bash
source .venv/bin/activate
python src/cli.py --debug
```

### Run tests:
```bash
pytest tests/ -v
```

### Code formatting:
```bash
black src/
flake8 src/
```

## Troubleshooting

**Import errors:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Model loading slow:**
- First load downloads models (can take time)
- Models are cached for subsequent runs
- Use smaller models for faster startup

**Memory issues:**
- Reduce max_tokens in config
- Use quantized models
- Clear conversation history regularly

## Contributing

Contributions welcome! This project is actively being developed.

**Areas needing work:**
- Core AI engine implementation
- RAG system
- Additional model integrations
- Documentation
- Tests

## License

MIT License - Free to use and modify!

## Resources

- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Ollama Documentation](https://ollama.ai/docs)
- [LangChain](https://python.langchain.com/) - Inspiration for architecture
- [ChromaDB](https://www.trychroma.com/) - Vector database
