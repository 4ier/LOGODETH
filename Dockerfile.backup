FROM python:3.11-slim as base

# Set labels for container metadata
LABEL org.opencontainers.image.title="LOGODETH API" \
      org.opencontainers.image.description="AI-powered metal band logo recognition engine" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="LOGODETH" \
      org.opencontainers.image.licenses="MIT"

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y \
    # Core dependencies
    libmagic1 \
    libffi-dev \
    # Security and performance
    curl \
    ca-certificates \
    # Cleanup
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_multimodal.txt requirements.txt

# Upgrade pip and install requirements with security best practices
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --require-hashes --only-binary=all -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    gunicorn==21.2.0 \
    uvloop==0.19.0 \
    httptools==0.6.1

# Copy application code
COPY backend/ ./backend/
COPY .env.example .env.example
COPY docker-entrypoint.sh /usr/local/bin/

# Create necessary directories with proper permissions
RUN mkdir -p /app/uploads /app/logs /app/data \
    && chown -R appuser:appgroup /app \
    && chmod 755 /usr/local/bin/docker-entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    LOGODETH_ENVIRONMENT=production

# Use entrypoint script for better initialization
ENTRYPOINT ["docker-entrypoint.sh"]

# Default command - can be overridden
CMD ["gunicorn", "backend.app:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "300", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--preload"]