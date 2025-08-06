# LOGODETH API Documentation 🔥

This directory contains comprehensive API documentation for LOGODETH.

## 📋 API Overview

LOGODETH provides a RESTful API for metal band logo recognition using advanced AI models.

**Base URL:** `http://localhost:8000/api/v1`

## 🚀 Quick Start

### Authentication
Currently, no authentication is required for the API. Rate limiting is applied per IP address.

### Content Types
- **Request**: `multipart/form-data` for file uploads
- **Response**: `application/json`

## 📝 Endpoints

### POST /recognize
Analyze a metal band logo image and return identification results.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/recognize" \
  -F "file=@logo.jpg" \
  -F "provider_preference=[\"openai\", \"anthropic\"]" \
  -F "force_refresh=false"
```

**Parameters:**
- `file` (required): Image file (JPG, PNG, GIF, WebP)
- `provider_preference` (optional): JSON array of AI providers to try
- `force_refresh` (optional): Skip cache and force new analysis

**Response:**
```json
{
  "band_name": "Dying Fetus",
  "genre": "Technical Death Metal",
  "confidence": 94.2,
  "description": "Classic brutal death metal typography",
  "ai_model": "gpt-4o",
  "processing_time_ms": 1247,
  "_cache_metadata": {
    "cached_at": "2024-12-07T10:30:00Z",
    "image_hash": "a1b2c3d4...",
    "ttl_seconds": 86400
  }
}
```

### GET /health
Check API server health status.

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "redis": "ok",
    "openai": "ok"
  }
}
```

### GET /cache/stats
Get cache statistics (development only).

**Response:**
```json
{
  "total_keys": 1337,
  "redis_memory_used": "42MB",
  "cache_ttl_seconds": 86400,
  "hit_rate": "67.3%"
}
```

## 🚨 Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid file, parameters)
- `413` - Payload Too Large (file > 10MB)
- `415` - Unsupported Media Type
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable (AI providers down)

**Error Response Format:**
```json
{
  "detail": {
    "message": "File size exceeds 10MB limit",
    "code": "FILE_TOO_LARGE",
    "status": 413
  }
}
```

## 📊 Rate Limiting

- **Default**: 10 requests per minute per IP
- **Headers**: Rate limit info in response headers
  - `X-RateLimit-Limit`: Requests allowed per minute
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets

## 🔧 Configuration

API behavior can be configured via environment variables:

```bash
LOGODETH_API_RATE_LIMIT=10          # Requests per minute
LOGODETH_MAX_FILE_SIZE=10485760     # Max file size (bytes)
LOGODETH_AI_TIMEOUT=60              # AI request timeout (seconds)
```

## 🧪 Testing

See [examples directory](../examples/) for:
- Python client examples
- JavaScript fetch examples  
- cURL commands
- Postman collection

## 📈 Performance

- **Average Response Time**: < 2 seconds (< 100ms with cache)
- **Supported Formats**: JPG, PNG, GIF, WebP
- **Max File Size**: 10MB
- **Concurrent Requests**: 50+ (configurable)
- **Cache TTL**: 24 hours (configurable)

## 🔗 OpenAPI Specification

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json