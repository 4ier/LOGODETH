# LOGODETH - Metal Logo Recognition Engine

_A Metal Logo Recognition Engine for True Kvlt Warriors_

> Translate unreadable metal band logos into actual band names.  
> No more guessing. No more asking. Just LOGODETH.

---

## What is LOGODETH?

**LOGODETH** is a metalhead's dream tool:  
An AI-powered image matcher that **deciphers extreme metal band logos** —  
whether it's brutal death, black metal, goregrind, or whatever monstrosity you're into.

Upload a logo image → Get the band name → Blast it.

---

## Why?

Metal logos are supposed to be unreadable.  
But when you forget that sick band's name from last night's gig?  
You'll need LOGODETH — the Google Translate of the underground.

---

## Quick Start

### Option 1: Simple Web Interface (Current Implementation)
Just open `index.html` in your browser - no server required!

```bash
# Clone the repo
git clone <your-repo-url>
cd logodeth

# Open in browser
open index.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000
```

### Option 2: API-Powered Backend (In Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY (optional)

# Run the backend server
uvicorn backend.app:app --reload

# Access the API at http://localhost:8000
# API docs at http://localhost:8000/docs
```

---

## How It Works

1. **Image Upload**:  
   User uploads a metal band logo image through the web interface.

2. **Multimodal AI Recognition**:  
   Leverages state-of-the-art vision models (GPT-4V, Claude Vision) to analyze and identify logos.

3. **Smart Fallback**:  
   If AI models are unavailable, falls back to reverse image search APIs.

4. **Intelligent Caching**:  
   Results are cached to minimize API costs and improve response times.

5. **Result Display**:  
   Returns band name, confidence score, and additional metadata when available.

---

## Current Features

- **Dark Metal-Themed UI**: Brutal aesthetic with blood-red accents
- **Drag & Drop Upload**: Easy image uploading with preview
- **Mock Recognition**: Simulates logo analysis with realistic results (temporary)
- **Responsive Design**: Works on desktop and mobile
- **Interactive Effects**: Hover animations and visual feedback
- **Easter Eggs**: Hidden brutal mode (try the Konami code)

---

## Project Structure

```
logodeth/
├── index.html              # Main webpage
├── styles.css              # Dark metal-themed styling
├── script.js               # Frontend JavaScript functionality
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── backend/
│   ├── app.py              # FastAPI main server
│   ├── api_routes.py       # API endpoint definitions
│   ├── logo_matcher.py     # AI-powered matching logic
│   ├── llm_client.py       # Multimodal LLM integration
│   ├── cache.py            # Redis caching layer
│   └── config.py           # Configuration management
├── docker/
│   ├── Dockerfile          # Application container
│   └── docker-compose.yml  # Development environment
└── tests/
    ├── test_api.py         # API endpoint tests
    ├── test_matcher.py     # Logo matching tests
    └── test_cache.py       # Cache functionality tests
```

---

## Development Roadmap (Simplified)

### Phase 1: Backend Development (Week 1)
* [x] Build dark metal-themed web interface
* [x] Add drag & drop image upload
* [x] Create mock logo recognition system
* [ ] **FastAPI backend setup**
  - [ ] Basic server structure
  - [ ] Image upload endpoint
  - [ ] Environment configuration
* [ ] **Multimodal AI Integration**
  - [ ] OpenAI GPT-4V integration
  - [ ] Anthropic Claude Vision integration
  - [ ] Fallback mechanism implementation
  - [ ] Response parsing and formatting

### Phase 2: Core Features (Week 2)
* [ ] **Caching Layer**
  - [ ] Redis integration
  - [ ] Image hash-based caching
  - [ ] TTL configuration
* [ ] **API Optimization**
  - [ ] Rate limiting
  - [ ] Error handling
  - [ ] Request validation
  - [ ] CORS configuration
* [ ] **Frontend Integration**
  - [ ] Replace mock data with API calls
  - [ ] Loading states
  - [ ] Error handling UI

### Phase 3: Deployment (Week 3)
* [ ] **Containerization**
  - [ ] Create Dockerfile
  - [ ] Docker Compose setup
  - [ ] Environment management
* [ ] **Production Setup**
  - [ ] Choose hosting platform
  - [ ] SSL/HTTPS configuration
  - [ ] Domain setup
  - [ ] Monitoring setup
* [ ] **Documentation**
  - [ ] API documentation
  - [ ] Deployment guide
  - [ ] Usage instructions

---

## Technical Implementation Details

### AI Integration
- **Primary**: OpenAI GPT-4 Vision API
- **Secondary**: Anthropic Claude 3 Vision API
- **Fallback**: Reverse image search APIs
- **Caching**: Redis with image hash keys
- **Cost Optimization**: Tiered API usage based on confidence

### Backend Architecture
- **Framework**: FastAPI for high performance
- **Caching**: Redis for API response caching
- **Rate Limiting**: Built-in request throttling
- **Storage**: Temporary file handling for uploads
- **Monitoring**: Structured logging and metrics

---

## API Usage & Costs

- **GPT-4 Vision**: ~$0.01-0.03 per logo recognition
- **Claude Vision**: Similar pricing tier
- **Caching Strategy**: Reduces duplicate API calls
- **Rate Limiting**: Prevents abuse and controls costs
- **Monthly Budget**: Configurable spending limits

---

## Performance Targets

- **Response Time**: <2s for logo recognition
- **Cache Hit Rate**: >60% for popular logos
- **API Availability**: 99.9% uptime
- **Concurrent Users**: 50+ simultaneous requests
- **Cost Efficiency**: <$0.02 average per request

---

## Demo Bands Database (Current Mock Data)

The current mock implementation includes logos from:

**Death Metal**: Disentomb, Defeated Sanity, Visceral Disgorge, Cryptopsy, Dying Fetus, Cannibal Corpse, Bloodbath, Suffocation, Necrophagist, Gorguts

**Black Metal**: Mayhem, Darkthrone, Emperor, Burzum, Immortal, Bathory, Gorgoroth, Marduk, Watain, Behemoth

*Note: This will be replaced with real scraped data from Metal Archives.*

---

## Deployment

### Quick Deploy with Docker
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t logodeth .
docker run -p 8000:8000 --env-file .env logodeth
```

### Cloud Deployment Options
- **Heroku**: One-click deploy with Heroku button
- **Railway**: Direct GitHub integration
- **DigitalOcean App Platform**: Container-based deployment
- **AWS ECS/Fargate**: For scalable production use

### Production Checklist
- [ ] Set production API keys
- [ ] Configure Redis for persistent caching
- [ ] Set up SSL/HTTPS
- [ ] Configure rate limiting
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure backup strategy for Redis

---

## Credits

* Inspired by every unreadable band shirt ever.
* Powered by [OpenAI CLIP](https://github.com/openai/CLIP)
* Logo dataset: scraped from [Metal Archives](https://www.metal-archives.com/)
* Fonts: Google Fonts (Metal Mania, Creepster)

---

## License

MIT — spread the metal freely.

> "If you can read it, it's not LOGODETH."  
> — Unknown corpse-painted oracle

---

## Contributing

Want to make LOGODETH more brutal? 

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/more-brutality`)
3. Commit your changes (`git commit -m 'Add more brutal features'`)
4. Push to the branch (`git push origin feature/more-brutality`)
5. Open a Pull Request

### Ideas for Contributions:
- Add support for more vision AI providers
- Implement batch logo processing
- Create a Discord bot integration
- Add mobile app version
- Create Chrome extension for logo recognition on any website
- Implement band information enrichment
- Add more metal-themed UI effects
- Improve caching strategies

---

## Development Setup

### Prerequisites
- Python 3.8+
- Redis 6.0+
- Docker & Docker Compose (optional)
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/logodeth.git
cd logodeth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_api.py
pytest tests/test_matcher.py
pytest tests/test_cache.py

# Run with coverage
pytest --cov=.
```

### Environment Variables
Create a `.env` file with:
```
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
ANTHROPIC_API_KEY=your_anthropic_api_key
REDIS_URL=redis://localhost:6379
API_RATE_LIMIT=10
CACHE_TTL=86400
MAX_FILE_SIZE=10485760  # 10MB
```

