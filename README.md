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

### Option 2: Full Backend Setup (Future Implementation)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web scraper to collect logos
python scraper/metal_archives_scraper.py

# Process and embed logo images
python processing/logo_processor.py

# Run the web app
python app.py

# Or run the Gradio interface
python gradio_ui.py
```

---

## How It Works

1. **Data Collection**:  
   Crawls thousands of band logos from Metal Archives using intelligent web scraping.

2. **Image Processing**:  
   Preprocesses logo images, handles various formats and sizes.

3. **Feature Extraction**:  
   Uses [CLIP](https://github.com/openai/CLIP) to embed logo images into high-dimensional vector space.

4. **Vector Database**:  
   Stores embeddings in optimized vector database for fast similarity search.

5. **Similarity Search**:  
   Computes cosine similarity against precomputed logo vector database.

6. **Result Ranking**:  
   Returns top matching band names with confidence scores and metadata.

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
├── scraper/
│   ├── metal_archives_scraper.py    # Main scraper for Metal Archives
│   ├── logo_downloader.py           # Image download utilities
│   ├── rate_limiter.py              # Respectful scraping rate limiting
│   └── data_validator.py            # Data quality validation
├── processing/
│   ├── logo_processor.py            # Image preprocessing pipeline
│   ├── clip_embedder.py             # CLIP-based feature extraction
│   └── vector_db.py                 # Vector database operations
├── backend/
│   ├── app.py                       # Flask/FastAPI main server
│   ├── api_routes.py                # API endpoint definitions
│   └── logo_matcher.py              # Core matching algorithm
├── data/
│   ├── raw_logos/                   # Downloaded logo images
│   ├── processed_logos/             # Preprocessed images
│   ├── embeddings/                  # CLIP embeddings
│   └── metadata.json               # Band metadata
└── tests/
    ├── test_scraper.py
    ├── test_processor.py
    └── test_matcher.py
```

---

## Development Roadmap

### Phase 1: Data Collection & Infrastructure (Week 1-2)
* [x] Build dark metal-themed web interface
* [x] Add drag & drop image upload
* [x] Create mock logo recognition system
* [ ] **Implement Metal Archives scraper**
  - [ ] Band listing crawler
  - [ ] Logo image downloader
  - [ ] Metadata extraction (genre, country, year)
  - [ ] Rate limiting and respectful scraping
  - [ ] Error handling and retry logic
* [ ] **Data validation and cleaning**
  - [ ] Image format standardization
  - [ ] Duplicate detection and removal
  - [ ] Quality filtering (resolution, corruption)

### Phase 2: Image Processing & AI Pipeline (Week 3-4)
* [ ] **Image preprocessing pipeline**
  - [ ] Resize and normalize images
  - [ ] Background removal/standardization
  - [ ] Augmentation for training data
* [ ] **CLIP integration**
  - [ ] Batch embedding generation
  - [ ] Embedding optimization and compression
  - [ ] Performance benchmarking
* [ ] **Vector database setup**
  - [ ] Choose optimal vector DB (Pinecone/Weaviate/Chroma)
  - [ ] Index optimization for similarity search
  - [ ] Backup and versioning system

### Phase 3: Backend Development (Week 5-6)
* [ ] **API development**
  - [ ] Flask/FastAPI server setup
  - [ ] Image upload and processing endpoints
  - [ ] Logo matching and ranking API
  - [ ] Batch processing capabilities
* [ ] **Core matching algorithm**
  - [ ] Similarity computation optimization
  - [ ] Multi-stage filtering (genre, year, etc.)
  - [ ] Confidence score calibration
  - [ ] Top-N recommendation system

### Phase 4: Frontend Integration & Testing (Week 7-8)
* [ ] **Frontend-backend integration**
  - [ ] Replace mock data with real API calls
  - [ ] Real-time processing indicators
  - [ ] Error handling and user feedback
* [ ] **Advanced features**
  - [ ] Batch logo recognition
  - [ ] Search history and favorites
  - [ ] Band information integration
  - [ ] Spotify/Apple Music links
* [ ] **Testing and optimization**
  - [ ] Unit tests for all components
  - [ ] Integration testing
  - [ ] Performance optimization
  - [ ] User acceptance testing

### Phase 5: Deployment & Scaling (Week 9-10)
* [ ] **Production deployment**
  - [ ] Containerization (Docker)
  - [ ] Cloud deployment (AWS/GCP/Azure)
  - [ ] CDN setup for image serving
  - [ ] Monitoring and logging
* [ ] **Additional features**
  - [ ] Mobile app version
  - [ ] Chrome extension
  - [ ] Offline CLI version
  - [ ] API documentation and public access

---

## Technical Implementation Details

### Web Scraping Strategy
- **Target**: Metal Archives (https://www.metal-archives.com/)
- **Approach**: Respectful scraping with rate limiting
- **Data Points**: Band name, logo image, genre, country, formation year
- **Estimated Dataset**: 50,000+ band logos
- **Storage**: Local filesystem + metadata JSON

### AI Pipeline
- **Model**: OpenAI CLIP (ViT-B/32 or ViT-L/14)
- **Preprocessing**: 224x224 RGB normalization
- **Embeddings**: 512/768-dimensional vectors
- **Similarity**: Cosine similarity with optimized search
- **Database**: Vector database with metadata filtering

### Backend Architecture
- **Framework**: FastAPI for high performance
- **Database**: PostgreSQL + pgvector for embeddings
- **Caching**: Redis for frequent queries
- **Queue**: Celery for background processing
- **Storage**: S3-compatible object storage

---

## Data Collection Ethics

- **Respectful Scraping**: Implements proper rate limiting (1-2 requests/second)
- **Terms Compliance**: Follows Metal Archives' terms of service
- **Attribution**: Credits data sources appropriately
- **Fair Use**: Educational/research purposes, non-commercial
- **Opt-out**: Respects robots.txt and removal requests

---

## Performance Targets

- **Dataset Size**: 50,000+ band logos
- **Query Speed**: <500ms for similarity search
- **Accuracy**: >85% top-3 matching accuracy
- **Throughput**: 100+ concurrent users
- **Uptime**: 99.9% availability

---

## Demo Bands Database (Current Mock Data)

The current mock implementation includes logos from:

**Death Metal**: Disentomb, Defeated Sanity, Visceral Disgorge, Cryptopsy, Dying Fetus, Cannibal Corpse, Bloodbath, Suffocation, Necrophagist, Gorguts

**Black Metal**: Mayhem, Darkthrone, Emperor, Burzum, Immortal, Bathory, Gorgoroth, Marduk, Watain, Behemoth

*Note: This will be replaced with real scraped data from Metal Archives.*

---

## Deployment

### Static Hosting (Current)
Deploy to any static hosting service:
- **Netlify**: Drag and drop the folder
- **Vercel**: Connect your GitHub repo
- **GitHub Pages**: Enable in repository settings

### Full Stack (Future)
- **Backend**: Railway, Heroku, or DigitalOcean
- **Frontend**: Vercel or Netlify
- **Database**: PostgreSQL with pgvector for embeddings
- **Storage**: AWS S3 or Google Cloud Storage

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
- Improve the Metal Archives scraper
- Implement additional data sources
- Optimize CLIP embedding pipeline
- Enhance the matching algorithm
- Add mobile app version
- Create Chrome extension for logo recognition on any website
- Implement band information integration
- Add sound effects and brutal animations

---

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend build tools)
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
pytest tests/test_scraper.py
pytest tests/test_processor.py
pytest tests/test_matcher.py

# Run with coverage
pytest --cov=.
```

### Environment Variables
Create a `.env` file with:
```
METAL_ARCHIVES_DELAY=1.5
CLIP_MODEL=ViT-B/32
VECTOR_DB_URL=your_vector_db_url
API_SECRET_KEY=your_secret_key
```

