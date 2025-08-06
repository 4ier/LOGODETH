# Contributing to LOGODETH 🤘

First off, thank you for considering contributing to LOGODETH! It's people like you that make the metal community stronger. 

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## 🔥 Ways to Contribute

LOGODETH is an open-source project and we love to receive contributions from our community — you! There are many ways to contribute:

- **Reporting bugs** 🐛
- **Suggesting enhancements** ✨  
- **Writing code** 💻
- **Improving documentation** 📚
- **Adding logo samples** 🖼️
- **Testing and feedback** 🧪
- **Community engagement** 💬

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** - Required for backend development
- **Docker & Docker Compose** - For containerized development
- **Git** - Version control
- **Redis** - For caching (can use Docker)
- **OpenAI API Key** - For AI recognition (required for testing)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LOGODETH.git
   cd LOGODETH
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements_multimodal.txt
   pip install -r requirements-dev.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

6. **Start Redis** (using Docker):
   ```bash
   docker run -d -p 6379:6379 redis:7-alpine
   ```

7. **Run the application**:
   ```bash
   # Start API server
   uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   
   # Start frontend (separate terminal)
   cd frontend && python3 -m http.server 8080
   ```

## 🧪 Testing

We use pytest for testing. Please make sure all tests pass before submitting a PR.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test categories
pytest tests/test_api.py
pytest tests/test_recognition.py
pytest tests/test_cache.py

# Run tests with verbose output
pytest -v
```

### Writing Tests

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test API endpoints and service interactions
- **Mock external dependencies**: Use mocks for AI APIs in tests
- **Test edge cases**: Invalid inputs, network failures, etc.

Example test:
```python
import pytest
from backend.services.cache import CacheService

def test_image_hashing():
    cache = CacheService()
    image_bytes = b"fake image data"
    
    hash1 = cache.hasher.hash_image(image_bytes)
    hash2 = cache.hasher.hash_image(image_bytes)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex length
```

## 📋 Code Standards

### Python Code Style

We follow PEP 8 with some modifications. Use these tools:

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

- **Type hints**: Use type hints for all function signatures
- **Docstrings**: Document all public functions and classes
- **Error handling**: Proper exception handling with specific error types
- **Logging**: Use structured logging with appropriate levels
- **Security**: Validate all inputs, sanitize user data

Example function:
```python
async def recognize_logo(
    image_bytes: bytes, 
    provider: str = "openai"
) -> RecognitionResult:
    """
    Recognize a metal band logo using AI vision models.
    
    Args:
        image_bytes: Raw image data
        provider: AI provider to use ('openai' or 'anthropic')
        
    Returns:
        RecognitionResult with band name, confidence, etc.
        
    Raises:
        InvalidImageError: If image format is not supported
        AIServiceError: If AI service is unavailable
    """
    # Implementation here...
```

### Frontend Code Style

- **Modern JavaScript**: Use ES6+ features
- **Consistent formatting**: 2-space indentation
- **Error handling**: Proper try/catch blocks
- **Accessibility**: Follow WCAG guidelines
- **Performance**: Optimize for speed and memory

### Git Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```bash
feat: add batch logo processing API
fix: resolve cache key collision issue  
docs: update deployment guide
test: add integration tests for recognition
refactor: simplify AI client architecture
chore: update dependencies to latest versions
```

**Commit Message Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Examples:**
- `feat(api): add batch processing endpoint`
- `fix(cache): prevent memory leak in Redis client`
- `docs: add contributing guidelines`
- `test(recognition): add unit tests for AI fallback`

## 🔄 Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/awesome-new-feature
   ```

2. **Make your changes** following our code standards

3. **Add or update tests** for your changes

4. **Run the test suite** and ensure all tests pass:
   ```bash
   pytest
   black backend/ tests/
   flake8 backend/ tests/
   ```

5. **Update documentation** if needed

6. **Commit your changes** with descriptive commit messages

7. **Push to your fork**:
   ```bash
   git push origin feature/awesome-new-feature
   ```

8. **Submit a Pull Request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots (if UI changes)
   - Testing instructions

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧪 Test improvements
- [ ] 🔧 Chore/maintenance

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged and published
```

## 🎯 Areas for Contribution

### 🤖 AI & Machine Learning
- **Model improvements**: Experiment with different AI providers
- **Accuracy enhancement**: Improve prompt engineering
- **Batch processing**: Implement efficient batch recognition
- **Custom models**: Train specialized metal logo models

### 🔧 Backend Development  
- **API endpoints**: Add new functionality
- **Performance**: Optimize database queries and caching
- **Security**: Improve authentication and authorization
- **Monitoring**: Add metrics and observability

### 🌐 Frontend Development
- **UI/UX**: Improve user interface and experience
- **Mobile responsiveness**: Better mobile support
- **Accessibility**: WCAG compliance improvements
- **Performance**: Frontend optimization

### 📱 Integrations & Extensions
- **Discord bot**: Metal server integration
- **Browser extensions**: Logo recognition on web pages
- **Mobile apps**: React Native or Flutter apps
- **CLI tools**: Command-line interface

### 📊 Data & Content
- **Logo database**: Expand the training dataset
- **Genre classification**: Improve metal subgenre detection
- **Band information**: Integrate with music databases
- **Internationalization**: Support for non-English bands

## 🐛 Reporting Bugs

Bugs are tracked as [GitHub issues](https://github.com/4ier/LOGODETH/issues). When you create a bug report, please include:

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. macOS, Linux, Windows]
- Browser: [e.g. Chrome, Firefox, Safari]
- Python version: [e.g. 3.11.0]
- Docker version: [if applicable]

**Additional context**
Add any other context about the problem here.
```

## ✨ Suggesting Enhancements

Enhancement suggestions are also tracked as [GitHub issues](https://github.com/4ier/LOGODETH/issues). When creating an enhancement suggestion:

### Enhancement Request Template

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.

**Would you be willing to implement this feature?**
- [ ] Yes, I'd like to work on this
- [ ] I can help with testing/feedback
- [ ] I'd prefer someone else implement it
```

## 🏷️ Issue Labels

We use labels to categorize issues:

- **`bug`** - Something isn't working
- **`enhancement`** - New feature or request  
- **`documentation`** - Improvements or additions to documentation
- **`good first issue`** - Good for newcomers
- **`help wanted`** - Extra attention is needed
- **`question`** - Further information is requested
- **`wontfix`** - This will not be worked on
- **`duplicate`** - This issue or pull request already exists

## 🤝 Community Guidelines

### Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inspiring community for all.

### Communication

- **Be respectful** - Treat everyone with respect and kindness
- **Be constructive** - Provide helpful feedback and suggestions  
- **Be patient** - Remember that everyone has different skill levels
- **Stay on topic** - Keep discussions relevant to the project
- **Use inclusive language** - Avoid discriminatory or offensive language

### Getting Help

If you need help:

1. **Check the documentation** - README, docs/, and code comments
2. **Search existing issues** - Your question might already be answered
3. **Join our Discord** - Real-time community support
4. **Create an issue** - For bugs or feature requests
5. **Start a discussion** - For general questions or ideas

## 🎉 Recognition

Contributors will be recognized in:

- **README contributors section**
- **Release notes** for significant contributions  
- **Hall of Fame** for major contributors
- **Special roles** in our Discord community

## 📚 Resources

### Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Docker Documentation](https://docs.docker.com/)

### Learning Resources
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Async Python](https://docs.python.org/3/library/asyncio.html)
- [REST API Design](https://restfulapi.net/)
- [Git Best Practices](https://www.conventionalcommits.org/)

Thank you for contributing to LOGODETH! Together, we'll make the metal community's logo recognition dreams come true. 🤘🔥

---

*Questions about contributing? Join our [Discord](https://discord.gg/logodeth) or create an [issue](https://github.com/4ier/LOGODETH/issues).*