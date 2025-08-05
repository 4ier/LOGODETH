# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LOGODETH is a metal band logo recognition engine that uses multimodal AI models (GPT-4V, Claude Vision) to identify hard-to-read extreme metal band logos. The project provides a web interface for logo upload and uses intelligent caching to minimize API costs.

## Key Commands

### Development Environment

```bash
# Start all development services (API server and Redis)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Run without Docker
uvicorn backend.app:app --reload
```

### Python Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_multimodal.txt  # All dependencies

# Run tests
pytest                              # Run all tests
pytest tests/test_scraper.py       # Run specific test file
pytest --cov=.                      # Run with coverage

# Code quality checks
black .                             # Format code
flake8                             # Lint code
mypy .                             # Type checking
```

### Frontend Development

```bash
# Current implementation is static HTML/CSS/JS
# Serve locally for development
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Architecture Overview

The project follows a simplified architecture:

1. **Frontend Layer** (root directory)
   - Dark metal-themed UI with drag-and-drop
   - JavaScript API integration
   - Real-time result display

2. **Backend API Layer** (`backend/`)
   - FastAPI server for REST endpoints
   - Multimodal AI integration (OpenAI, Anthropic)
   - Smart fallback mechanisms
   - Result caching

3. **Data Storage**
   - Redis for caching API responses
   - Temporary file storage for uploads

## Key Technical Decisions

- **AI Models**: Using GPT-4V and Claude Vision for logo recognition
- **Caching**: Redis with 24-hour TTL to minimize API costs
- **API Framework**: FastAPI for high performance and async support
- **Rate Limiting**: API request throttling to prevent abuse
- **Cost Control**: Tiered API usage and intelligent caching

## Development Workflow

1. **Feature Development**:
   - Create feature branch from `main`
   - Implement changes following existing patterns
   - Run tests and linting before committing
   - Create PR with description

2. **Testing Strategy**:
   - Unit tests for individual components
   - Integration tests for API endpoints
   - Performance benchmarks for vector search
   - Manual testing of UI features

3. **Database Migrations**:
   - Use Alembic for schema migrations (when implemented)
   - Test migrations locally before applying to production

## Current Implementation Status

- ✅ Static frontend with mock logo recognition
- ✅ Simplified architecture design
- ✅ Development environment configuration (Docker Compose)
- ✅ Project documentation
- ⏳ Backend API development
- ⏳ Multimodal AI integration
- ⏳ Frontend-backend integration
- ⏳ Production deployment

## Important Notes

- The project is in early development stages
- Current frontend shows mock data only
- API keys are required for OpenAI/Anthropic services
- Implement proper rate limiting to control costs
- Cache results to minimize repeated API calls