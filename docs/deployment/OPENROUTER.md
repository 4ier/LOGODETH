# 🌐 Using OpenRouter with LOGODETH

OpenRouter provides a unified API to access multiple AI models through a single endpoint, making it perfect for LOGODETH as it allows you to:

- **Access multiple vision models** with one API key
- **Compare costs** across different providers
- **Switch models** without code changes
- **Pay as you go** with transparent pricing

## 🚀 Quick Start

### 1. Get OpenRouter API Key
1. Sign up at [OpenRouter](https://openrouter.ai)
2. Go to [API Keys](https://openrouter.ai/keys)
3. Create a new API key

### 2. Configure LOGODETH
```bash
# Copy the OpenRouter config template
cp .env.openrouter.example .env

# Edit with your API key
nano .env
# Set: LOGODETH_OPENAI_API_KEY=sk-or-v1-your-key-here
```

### 3. Deploy
```bash
# With Docker
docker-compose up -d

# Or locally
uvicorn backend.app:app --reload
```

## 💰 Cost Comparison

| Model | Provider | Quality | Speed | Cost per 1M tokens | Cost per Logo |
|-------|----------|---------|-------|-------------------|---------------|
| **gpt-4-vision-preview** | OpenAI | ⭐⭐⭐⭐⭐ | Fast | $10 | ~$0.01 |
| **gpt-4o** | OpenAI | ⭐⭐⭐⭐⭐ | Fast | $5 | ~$0.005 |
| **claude-3-opus** | Anthropic | ⭐⭐⭐⭐⭐ | Fast | $15 | ~$0.015 |
| **claude-3-sonnet** | Anthropic | ⭐⭐⭐⭐ | Fast | $3 | ~$0.003 |
| **gemini-pro-vision** | Google | ⭐⭐⭐⭐ | Fast | $0.25 | ~$0.0003 |
| **llava-13b** | Open | ⭐⭐⭐ | Medium | Free | $0 |

## 🔧 Configuration Examples

### High Quality (Production)
```env
# Best accuracy for production use
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-your-key
LOGODETH_OPENAI_MODEL=openai/gpt-4-vision-preview
```

### Balanced (Recommended)
```env
# Good balance of quality and cost
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-your-key
LOGODETH_OPENAI_MODEL=openai/gpt-4o
```

### Budget-Friendly
```env
# Lower cost, still good quality
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-your-key
LOGODETH_OPENAI_MODEL=google/gemini-pro-vision
```

### Free/Ultra-Low Cost
```env
# Free tier models (may have limitations)
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-your-key
LOGODETH_OPENAI_MODEL=haotian-liu/llava-13b
```

## 🎯 Alternative Providers

### Together AI
```env
# Fast inference, competitive pricing
LOGODETH_OPENAI_BASE_URL=https://api.together.xyz/v1
LOGODETH_OPENAI_API_KEY=your-together-key
LOGODETH_OPENAI_MODEL=meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo
```

### Groq
```env
# Ultra-fast inference
LOGODETH_OPENAI_BASE_URL=https://api.groq.com/openai/v1
LOGODETH_OPENAI_API_KEY=your-groq-key
LOGODETH_OPENAI_MODEL=llama-3.2-90b-vision-preview
```

### Local Models (Ollama)
```env
# Run models locally - no API costs!
LOGODETH_OPENAI_BASE_URL=http://localhost:11434/v1
LOGODETH_OPENAI_API_KEY=not-needed
LOGODETH_OPENAI_MODEL=llava:13b
```

First install Ollama and the model:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull vision model
ollama pull llava:13b

# Start Ollama server
ollama serve
```

## 📊 Model Selection Guide

### For Best Accuracy
- **gpt-4-vision-preview**: Best for complex, illegible logos
- **claude-3-opus**: Excellent alternative, good with artistic styles
- **gpt-4o**: Newest model, great balance

### For Speed
- **claude-3-haiku**: Fastest Anthropic model
- **gemini-pro-vision**: Very fast Google model
- **groq + llama**: Ultra-fast inference

### For Cost Optimization
- **gemini-pro-vision**: Best quality/cost ratio
- **llava**: Free open-source option
- **local models**: No API costs, requires GPU

## 🔄 Switching Models

You can switch models without restarting:

### Via Environment Variable
```bash
# Switch to a different model
export LOGODETH_OPENAI_MODEL=anthropic/claude-3-sonnet
# Restart the service
docker-compose restart api
```

### Dynamic Model Selection (Future Feature)
```python
# Pass model preference in API request
curl -X POST /api/v1/recognize \
  -F "file=@logo.jpg" \
  -F "model_preference=google/gemini-pro-vision"
```

## 💡 Tips & Best Practices

### 1. Cost Control
```env
# Set spending limits in OpenRouter dashboard
# Use cheaper models for testing
LOGODETH_OPENAI_MODEL=google/gemini-pro-vision
```

### 2. Fallback Strategy
```env
# Configure multiple providers
LOGODETH_OPENAI_MODEL=openai/gpt-4o  # Primary
LOGODETH_ANTHROPIC_API_KEY=sk-ant-xxx  # Fallback
```

### 3. Caching Strategy
```env
# Increase cache TTL to reduce API calls
LOGODETH_CACHE_TTL=172800  # 48 hours
```

### 4. Rate Limiting
```env
# Adjust based on your OpenRouter plan
LOGODETH_API_RATE_LIMIT=30  # requests per minute
```

## 🔍 Monitoring Usage

### OpenRouter Dashboard
- View usage: https://openrouter.ai/activity
- Check costs: https://openrouter.ai/credits
- Set limits: https://openrouter.ai/limits

### Application Logs
```bash
# View provider info
curl http://localhost:8000/api/v1/provider-info

# Check health
curl http://localhost:8000/health
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Error
```
Error: Invalid API key
```
**Solution**: Check your API key starts with `sk-or-v1-`

#### 2. Model Not Found
```
Error: Model not available
```
**Solution**: Check model name format (provider/model-name)

#### 3. Rate Limit
```
Error: Rate limit exceeded
```
**Solution**: Upgrade OpenRouter plan or reduce request rate

#### 4. Image Size Error
```
Error: Image too large
```
**Solution**: Reduce max file size:
```env
LOGODETH_MAX_FILE_SIZE=5242880  # 5MB
```

## 📈 Performance Optimization

### For Production
```env
# Optimal production settings with OpenRouter
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-production-key
LOGODETH_OPENAI_MODEL=openai/gpt-4o
LOGODETH_CACHE_TTL=172800  # 48 hour cache
LOGODETH_WORKER_COUNT=4
LOGODETH_API_RATE_LIMIT=50
```

### For Development
```env
# Cost-effective development settings
LOGODETH_USE_OPENROUTER=true
LOGODETH_OPENAI_API_KEY=sk-or-v1-dev-key
LOGODETH_OPENAI_MODEL=google/gemini-pro-vision
LOGODETH_CACHE_TTL=3600  # 1 hour cache
LOGODETH_DEBUG=true
```

## 🔗 Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Model Pricing](https://openrouter.ai/models)
- [API Reference](https://openrouter.ai/api/v1/docs)
- [Discord Support](https://discord.gg/openrouter)

## 💰 Cost Estimation

For typical usage (1000 logos/month):

| Model | Cost/Logo | Monthly Cost |
|-------|-----------|--------------|
| GPT-4 Vision | $0.01 | $10 |
| GPT-4o | $0.005 | $5 |
| Claude 3 Sonnet | $0.003 | $3 |
| Gemini Pro Vision | $0.0003 | $0.30 |
| Llava (Free) | $0 | $0 |

With 60% cache hit rate: **Reduce costs by 60%!**

---

**Pro Tip**: Start with Gemini Pro Vision for testing, upgrade to GPT-4o for production! 🚀