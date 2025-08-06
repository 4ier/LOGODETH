#!/bin/bash
set -e

# LOGODETH Docker Entrypoint Script
echo "🔥 Starting LOGODETH API server..."

# Function to log with timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Validate required environment variables
log "Validating configuration..."

if [ -z "$LOGODETH_OPENAI_API_KEY" ]; then
    log "ERROR: LOGODETH_OPENAI_API_KEY is required"
    exit 1
fi

if [ "$LOGODETH_OPENAI_API_KEY" = "sk-your-openai-key-here" ]; then
    log "ERROR: Please set a real OpenAI API key"
    exit 1
fi

# Wait for Redis if it's configured
if [ ! -z "$LOGODETH_REDIS_URL" ]; then
    log "Waiting for Redis..."
    
    # Extract Redis host and port from URL
    REDIS_HOST=$(echo "$LOGODETH_REDIS_URL" | sed 's|redis://||' | sed 's|:.*||')
    REDIS_PORT=$(echo "$LOGODETH_REDIS_URL" | sed 's|.*:||' | sed 's|/.*||')
    
    # Default port if not specified
    if [ "$REDIS_PORT" = "$REDIS_HOST" ]; then
        REDIS_PORT=6379
    fi
    
    # Wait up to 30 seconds for Redis
    for i in {1..30}; do
        if timeout 1 bash -c "cat < /dev/null > /dev/tcp/$REDIS_HOST/$REDIS_PORT" 2>/dev/null; then
            log "Redis is ready at $REDIS_HOST:$REDIS_PORT"
            break
        fi
        log "Waiting for Redis ($i/30)..."
        sleep 1
    done
    
    # Final check
    if ! timeout 1 bash -c "cat < /dev/null > /dev/tcp/$REDIS_HOST/$REDIS_PORT" 2>/dev/null; then
        log "WARNING: Could not connect to Redis at $REDIS_HOST:$REDIS_PORT"
        log "Continuing anyway - caching will be disabled"
    fi
fi

# Create necessary directories if they don't exist
mkdir -p /app/logs /app/uploads /app/data

# Set default values for missing environment variables
export LOGODETH_ENVIRONMENT=${LOGODETH_ENVIRONMENT:-production}
export LOGODETH_LOG_LEVEL=${LOGODETH_LOG_LEVEL:-INFO}
export LOGODETH_DEBUG=${LOGODETH_DEBUG:-false}
export LOGODETH_HOST=${LOGODETH_HOST:-0.0.0.0}
export LOGODETH_PORT=${LOGODETH_PORT:-8000}

log "Configuration:"
log "  Environment: $LOGODETH_ENVIRONMENT"
log "  Log Level: $LOGODETH_LOG_LEVEL"
log "  Debug Mode: $LOGODETH_DEBUG"
log "  Host: $LOGODETH_HOST"
log "  Port: $LOGODETH_PORT"
log "  OpenAI Configured: $([ ! -z "$LOGODETH_OPENAI_API_KEY" ] && echo 'Yes' || echo 'No')"
log "  Anthropic Configured: $([ ! -z "$LOGODETH_ANTHROPIC_API_KEY" ] && echo 'Yes' || echo 'No')"
log "  Redis URL: ${LOGODETH_REDIS_URL:-'Not configured'}"

# Test API key validity (optional - comment out if causing issues)
log "Testing API configuration..."
python3 -c "
import os
import sys
from backend.config import validate_required_settings

valid, missing = validate_required_settings()
if not valid:
    print('Configuration errors:', missing, file=sys.stderr)
    sys.exit(1)
print('Configuration is valid')
" || {
    log "WARNING: Configuration validation failed, but continuing anyway..."
}

log "🚀 Starting application with command: $@"

# Execute the main command
exec "$@"