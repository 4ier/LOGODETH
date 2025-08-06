# 🚀 LOGODETH Quick Start Guide

Get LOGODETH running in under 5 minutes!

## Prerequisites

- Python 3.8+
- Redis (or Docker)
- OpenAI API key

## ⚡ Fastest Setup (Using Docker)

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd LOGODETH

# 2. Copy and configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start everything with Docker
docker-compose up -d

# 4. Open frontend
open index.html  # Mac
# OR
xdg-open index.html  # Linux
# OR just drag index.html to your browser
```

## 🛠️ Manual Setup (Without Docker)

### Step 1: Install Redis

**Mac:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**Windows:**
Use WSL2 or Docker Desktop

### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_multimodal.txt
```

### Step 3: Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Required configuration:**
```env
OPENAI_API_KEY=sk-...your_actual_key_here...
```

### Step 4: Start the Backend

```bash
# Run the API server
python run.py

# Or use the startup script
./start_dev.sh
```

### Step 5: Open the Frontend

Open `index.html` in your browser:
- The backend should be running on http://localhost:8000
- API docs available at http://localhost:8000/docs

## 🧪 Test Your Setup

1. **Check API Health:**
```bash
curl http://localhost:8000/
# Should return: {"status":"healthy",...}
```

2. **Upload a Test Image:**
- Open index.html in browser
- Drag & drop any metal band logo image
- Click "ANALYZE LOGO"
- Wait for AI results

## 📊 Monitor Usage

Check your OpenAI usage to track costs:
- https://platform.openai.com/usage

Each logo recognition costs approximately $0.01-0.03

## 🐛 Troubleshooting

### "Cannot connect to API server"
- Check if backend is running: `curl http://localhost:8000/`
- Check if Redis is running: `redis-cli ping`
- Check console for CORS errors

### "API key not working"
- Verify your OpenAI API key is valid
- Check you have GPT-4 Vision access
- Ensure you have available credits

### "File upload fails"
- Max file size: 10MB
- Supported formats: JPG, PNG, GIF, WebP
- Check browser console for errors

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not, start Redis:
redis-server  # Or: sudo systemctl start redis
```

## 🔥 Pro Tips

1. **Use Cached Results**: The same image won't call API twice (24hr cache)

2. **Batch Processing**: Upload multiple logos to save on API calls

3. **Cost Control**: Set monthly limits in OpenAI dashboard

4. **Local Testing**: Use the mock mode by not setting API keys

## 📝 Configuration Options

Edit `.env` for advanced settings:

```env
# API Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...  # Optional fallback

# Cache Settings
REDIS_URL=redis://localhost:6379
CACHE_TTL=86400  # 24 hours

# Limits
API_RATE_LIMIT=10  # per minute
MAX_FILE_SIZE=10485760  # 10MB
```

## 🚢 Ready for Production?

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guides:
- Deploy to Heroku
- Deploy to Railway
- Deploy to DigitalOcean
- Self-host with Docker

## 📚 Next Steps

- Read the [full documentation](README.md)
- Check the [API documentation](http://localhost:8000/docs)
- Join our [Discord](#) for support
- Report issues on [GitHub](#)

---

**Need help?** Open an issue or reach out on Discord!

🤘 Happy logo hunting! 🤘