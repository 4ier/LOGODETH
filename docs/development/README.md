# LOGODETH Development Guide 👩‍💻

Welcome to the LOGODETH development guide! This document will help you contribute to the project effectively.

## 🏗️ Architecture Overview

LOGODETH follows a modern web application architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    LOGODETH Architecture                 │
├─────────────────────────────────────────────────────────┤
│  Frontend (HTML/JS)                                     │
│  ├── Drag & Drop UI                                     │
│  ├── Progress Indicators                                │
│  └── Result Display                                     │
├─────────────────────────────────────────────────────────┤
│  Backend API (FastAPI)                                  │
│  ├── /api/v1/recognize - Logo recognition endpoint      │
│  ├── /health - Health check endpoint                    │
│  └── /cache/stats - Cache statistics                    │
├─────────────────────────────────────────────────────────┤
│  Services Layer                                         │
│  ├── LLM Client - AI provider integration               │
│  ├── Cache Service - Redis caching                      │
│  └── Recognition Service - Business logic               │
├─────────────────────────────────────────────────────────┤
│  External Services                                       │
│  ├── OpenAI GPT-4V - Primary AI provider               │
│  ├── Anthropic Claude - Fallback AI provider           │
│  └── Redis - Caching layer                             │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- Redis 6.0+
- Docker & Docker Compose (optional)
- Git
- OpenAI API Key

### Quick Setup
```bash
# Clone repository
git clone https://github.com/4ier/LOGODETH.git
cd LOGODETH

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_multimodal.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Run application
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
LOGODETH/
├── backend/                    # FastAPI backend
│   ├── app.py                 # Main application entry
│   ├── config.py              # Configuration management
│   ├── models/                # Pydantic models
│   ├── routers/               # API route handlers
│   ├── services/              # Business logic services
│   └── utils/                 # Utility functions
├── frontend/                   # Static frontend
│   ├── index.html             # Main HTML page
│   ├── script.js              # JavaScript functionality
│   └── styles.css             # CSS styling
├── tests/                      # Test suites
├── docs/                       # Documentation
├── scripts/                    # Deployment scripts
├── docker-compose*.yml         # Docker configurations
├── Dockerfile                  # Container definition
└── requirements*.txt           # Python dependencies
```

## 🧪 Testing Strategy

### Test Categories

1. **Unit Tests** - Individual function testing
2. **Integration Tests** - API endpoint testing
3. **Service Tests** - External service integration
4. **End-to-End Tests** - Complete workflow testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test categories
pytest tests/test_api.py          # API tests
pytest tests/test_recognition.py  # Recognition logic
pytest tests/test_cache.py        # Cache functionality

# Run tests with verbose output
pytest -v -s
```

### Writing Tests

**Example Unit Test:**
```python
# tests/test_cache.py
import pytest
from backend.services.cache import ImageHasher

class TestImageHasher:
    def test_hash_consistency(self):
        hasher = ImageHasher()
        image_data = b"fake image data"
        
        hash1 = hasher.hash_image(image_data)
        hash2 = hasher.hash_image(image_data)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 length

    def test_different_images_different_hashes(self):
        hasher = ImageHasher()
        
        hash1 = hasher.hash_image(b"image1")
        hash2 = hasher.hash_image(b"image2")
        
        assert hash1 != hash2
```

**Example API Test:**
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_recognize_endpoint_missing_file():
    response = client.post("/api/v1/recognize")
    assert response.status_code == 422  # Validation error
```

### Mocking External Services

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_openai_client():
    with patch('backend.services.llm_client.AsyncOpenAI') as mock:
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = '{"band_name": "Test Band", "confidence": 95}'
        mock.return_value.chat.completions.create.return_value = mock_response
        yield mock
```

## 🎨 Code Style & Standards

### Python Code Style

We follow PEP 8 with these tools:

```bash
# Format code
black backend/ tests/

# Sort imports  
isort backend/ tests/

# Lint code
flake8 backend/ tests/

# Type checking
mypy backend/
```

### Code Quality Guidelines

1. **Type Hints**: Use type hints for all function signatures
2. **Docstrings**: Document all public functions and classes
3. **Error Handling**: Use specific exception types
4. **Logging**: Use structured logging with appropriate levels
5. **Security**: Validate all inputs and sanitize data

**Example Function:**
```python
from typing import Optional
from loguru import logger

async def recognize_logo(
    image_bytes: bytes,
    provider: str = "openai",
    force_refresh: bool = False
) -> RecognitionResult:
    """
    Recognize a metal band logo using AI vision models.
    
    Args:
        image_bytes: Raw image data to analyze
        provider: AI provider to use ('openai' or 'anthropic')
        force_refresh: Skip cache and force new recognition
        
    Returns:
        RecognitionResult containing band name, confidence, etc.
        
    Raises:
        InvalidImageError: If image format is not supported
        AIServiceError: If AI service is unavailable
    """
    logger.info(f"Starting logo recognition with {provider}")
    
    try:
        # Validate image
        if not _is_valid_image(image_bytes):
            raise InvalidImageError("Unsupported image format")
            
        # Check cache unless forced refresh
        if not force_refresh:
            cached_result = await cache.get_by_image(image_bytes)
            if cached_result:
                logger.info("Found cached result")
                return RecognitionResult.from_dict(cached_result)
        
        # Perform AI recognition
        result = await _call_ai_provider(provider, image_bytes)
        
        # Cache the result
        await cache.set_by_image(image_bytes, result.to_dict())
        
        logger.info(f"Recognition completed: {result.band_name}")
        return result
        
    except Exception as e:
        logger.error(f"Recognition failed: {e}")
        raise
```

## 🔧 Development Workflows

### Feature Development

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/awesome-new-feature
   ```

2. **Write Tests First** (TDD approach)
   ```bash
   # Write failing tests
   pytest tests/test_new_feature.py
   ```

3. **Implement Feature**
   - Follow code style guidelines
   - Add type hints and docstrings
   - Handle errors appropriately

4. **Test Implementation**
   ```bash
   pytest tests/test_new_feature.py
   pytest  # Run all tests
   ```

5. **Code Quality Checks**
   ```bash
   black backend/ tests/
   isort backend/ tests/ 
   flake8 backend/ tests/
   mypy backend/
   ```

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add awesome new feature"
   git push origin feature/awesome-new-feature
   ```

### Bug Fixes

1. **Create Bug Report** (if not exists)
2. **Write Reproduction Test**
3. **Fix the Bug**
4. **Verify Fix with Tests**
5. **Create Pull Request**

### Performance Optimization

1. **Profile Current Performance**
   ```bash
   # Use cProfile for Python profiling
   python -m cProfile -o profile.stats backend/app.py
   
   # Analyze with snakeviz
   snakeviz profile.stats
   ```

2. **Identify Bottlenecks**
3. **Implement Optimizations**
4. **Measure Improvement**
5. **Add Performance Tests**

## 🔍 Debugging Guide

### Local Development Debugging

```bash
# Enable debug mode
export LOGODETH_DEBUG=true
export LOGODETH_LOG_LEVEL=DEBUG

# Run with debugger
python -m pdb backend/app.py

# Use breakpoint() in code
def some_function():
    breakpoint()  # Python 3.7+
    # Code execution will pause here
```

### API Debugging

```bash
# Test API endpoints
curl -X POST http://localhost:8000/api/v1/recognize \
  -F "file=@test_logo.jpg" \
  -H "Accept: application/json"

# Check API health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

### Redis Debugging

```bash
# Connect to Redis
redis-cli

# View cached keys
redis-cli KEYS "logodeth:logo:*"

# Check memory usage
redis-cli INFO memory

# Monitor commands
redis-cli MONITOR
```

## 📊 Performance Monitoring

### Local Monitoring

```python
# Add timing decorators
from functools import wraps
import time

def timed_function(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@timed_function
async def recognize_logo(...):
    # Function implementation
```

### Production Monitoring

- **Metrics**: Prometheus/Grafana
- **Logging**: Structured logging with correlation IDs
- **Tracing**: OpenTelemetry for distributed tracing
- **Health Checks**: Comprehensive health endpoints

## 🐛 Common Development Issues

### 1. Import Errors
```bash
# Fix Python path issues
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use relative imports
from backend.services import cache
```

### 2. Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping

# Use different Redis DB for development
export LOGODETH_REDIS_URL="redis://localhost:6379/1"
```

### 3. API Key Issues
```bash
# Verify API key format
echo $LOGODETH_OPENAI_API_KEY | grep -E "^sk-"

# Test API key validity
curl -H "Authorization: Bearer $LOGODETH_OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

### 4. Docker Issues
```bash
# Rebuild containers
docker-compose build --no-cache

# Check container logs
docker-compose logs api

# Reset everything
docker-compose down -v
docker system prune -a
```

## 📚 Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)

### Development Tools
- **VS Code Extensions**:
  - Python
  - Pylance
  - Black Formatter
  - GitLens
  - Docker

### Learning Resources
- [Python Type Checking](https://mypy.readthedocs.io/)
- [Async Python Programming](https://realpython.com/async-io-python/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Redis Best Practices](https://redis.io/docs/manual/performance/)

## 🤝 Getting Help

- **Documentation Issues**: Update this guide
- **Code Questions**: Create GitHub discussion
- **Bugs**: Create GitHub issue
- **Chat**: Join our Discord server
- **Email**: dev@logodeth.ai

Happy coding! 🤘🔥