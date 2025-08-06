# LOGODETH Security Guide 🔒

This document outlines security best practices, policies, and procedures for LOGODETH.

## 🛡️ Security Overview

LOGODETH takes security seriously. As an AI-powered logo recognition service, we handle user-uploaded images and integrate with third-party AI services, making security a top priority.

## 🔐 Security Features

### Input Validation & Sanitization
- **File Type Validation**: Only accept supported image formats (JPG, PNG, GIF, WebP)
- **File Size Limits**: Maximum 10MB upload size (configurable)
- **Content Validation**: Basic image header validation
- **Path Traversal Protection**: Secure file handling without path manipulation

### Rate Limiting
- **Per-IP Rate Limiting**: Configurable requests per minute (default: 10)
- **Burst Protection**: Prevent rapid-fire requests
- **Progressive Penalties**: Increasing delays for repeated violations

### Data Protection
- **No Persistent Storage**: Images are processed in memory only
- **Temporary Files**: Auto-cleanup of temporary uploads
- **No User Data Collection**: No personal information stored
- **Cache Expiration**: Automatic cleanup of cached results

### API Security
- **CORS Protection**: Configurable allowed origins
- **Request Size Limits**: Prevent oversized requests
- **Error Information Disclosure**: Sanitized error messages
- **Health Check Security**: Limited information in health endpoints

## 🔧 Security Configuration

### Environment Variables

```bash
# Security settings
LOGODETH_SECRET_KEY=your-super-secret-key-here
LOGODETH_API_RATE_LIMIT=10                    # requests per minute
LOGODETH_MAX_FILE_SIZE=10485760               # 10MB in bytes
LOGODETH_CORS_ORIGINS=https://yourdomain.com  # allowed origins

# Production security
LOGODETH_DEBUG=false                          # disable debug mode
LOGODETH_LOG_LEVEL=INFO                       # appropriate log level
```

### File Upload Security

```python
# backend/utils/validators.py
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file for security."""
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"File type {file_ext} not allowed")
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("File size exceeds limit")
    
    # Validate file headers (magic bytes)
    file_start = file.file.read(8)
    file.file.seek(0)  # Reset file pointer
    
    if not _is_valid_image_header(file_start):
        raise ValidationError("Invalid image file")

def _is_valid_image_header(header: bytes) -> bool:
    """Check if file has valid image magic bytes."""
    image_signatures = {
        b'\xff\xd8\xff': 'jpg',      # JPEG
        b'\x89PNG\r\n\x1a\n': 'png', # PNG  
        b'GIF87a': 'gif',            # GIF87a
        b'GIF89a': 'gif',            # GIF89a
        b'RIFF': 'webp',             # WebP (partial)
    }
    
    return any(header.startswith(sig) for sig in image_signatures.keys())
```

## 🚨 Security Policies

### Responsible Disclosure

We welcome security researchers to help keep LOGODETH secure:

1. **Report Security Issues** to: security@logodeth.ai
2. **Provide Details**: Include steps to reproduce
3. **Allow Time**: Give us reasonable time to fix issues
4. **Coordinated Disclosure**: Work with us on public disclosure timing

### Bug Bounty Program

Currently, we don't have a formal bug bounty program, but we:
- Acknowledge security researchers in our Hall of Fame
- Provide special Discord roles for contributors
- Consider financial rewards for critical vulnerabilities

## 🔍 Security Testing

### Automated Security Scanning

```bash
# Dependency vulnerability scanning
pip-audit

# Code security scanning
bandit -r backend/

# Container security scanning  
docker scout cves your-image:latest

# OWASP ZAP API scanning
zap-api-scan.py -t http://localhost:8000/openapi.json
```

### Manual Security Testing

#### File Upload Testing
```bash
# Test file size limits
dd if=/dev/zero of=large_file.jpg bs=1M count=15
curl -X POST http://localhost:8000/api/v1/recognize -F "file=@large_file.jpg"

# Test invalid file types
echo "fake content" > malicious.exe
curl -X POST http://localhost:8000/api/v1/recognize -F "file=@malicious.exe"

# Test malformed images
echo "fake image data" > fake.jpg
curl -X POST http://localhost:8000/api/v1/recognize -F "file=@fake.jpg"
```

#### Rate Limiting Testing
```bash
# Test rate limiting
for i in {1..15}; do
  curl -X POST http://localhost:8000/api/v1/recognize \
    -F "file=@test.jpg" \
    --connect-timeout 5
done
```

#### CORS Testing
```bash
# Test CORS headers
curl -H "Origin: https://evil-domain.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:8000/api/v1/recognize
```

## 🔐 Production Security Hardening

### Container Security

```dockerfile
# Dockerfile security best practices
FROM python:3.11-slim as base

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

# Install security updates
RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Use non-root user
USER appuser

# Security labels
LABEL security.scan-policy="scan-on-build"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with minimal privileges
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "backend.app:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000"]
```

### Network Security

```yaml
# docker-compose.prod.yml
services:
  api:
    # Security options
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:rw,size=100M,mode=1777
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
    
    # Network isolation
    networks:
      - internal

networks:
  internal:
    driver: bridge
    internal: true  # No external access
```

### Secrets Management

#### Development
```bash
# Use environment files
cp .env.example .env.local
# Never commit .env files to git

# Use Docker secrets
echo "sk-your-key" | docker secret create openai_api_key -
```

#### Production
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name logodeth/openai-key \
  --secret-string "sk-your-production-key"

# Kubernetes secrets
kubectl create secret generic logodeth-secrets \
  --from-literal=openai-api-key=sk-your-key

# HashiCorp Vault
vault kv put secret/logodeth \
  openai_api_key=sk-your-key
```

## 📊 Security Monitoring

### Logging Security Events

```python
# backend/utils/security.py
from loguru import logger
from functools import wraps

def security_audit(event_type: str):
    """Decorator to log security events."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Security event: {event_type} - SUCCESS")
                return result
            except Exception as e:
                logger.warning(f"Security event: {event_type} - FAILED - {str(e)}")
                raise
        return wrapper
    return decorator

@security_audit("file_upload")
async def handle_file_upload(file: UploadFile):
    # File upload handling
    pass
```

### Security Metrics

Monitor these security-related metrics:

- **Failed Authentication Attempts**
- **Rate Limit Violations**
- **Invalid File Upload Attempts**
- **Suspicious Request Patterns**
- **Error Rates by Endpoint**

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: logodeth-security
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"4.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          
      - alert: RateLimitViolations
        expr: rate(rate_limit_exceeded_total[5m]) > 0.05
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High rate limit violations"
```

## 🔒 Data Privacy

### Data Handling Policies

1. **Image Processing**:
   - Images processed in memory only
   - No permanent storage of user images
   - Temporary files automatically cleaned up

2. **Caching**:
   - Only recognition results cached, not images
   - Cache keys use SHA-256 hashes
   - Configurable TTL (default 24 hours)

3. **Logging**:
   - No sensitive data in logs
   - Image hashes logged for debugging
   - IP addresses for rate limiting only

### GDPR Compliance

- **No Personal Data Collection**: We don't collect personal information
- **Right to Erasure**: Cache entries automatically expire
- **Data Portability**: API results provided in standard JSON format
- **Privacy by Design**: Security built into system architecture

## 🚨 Incident Response

### Security Incident Response Plan

1. **Detection**:
   - Automated monitoring alerts
   - User reports
   - Security scanner findings

2. **Assessment**:
   - Determine impact and scope
   - Classify severity level
   - Assemble response team

3. **Containment**:
   - Isolate affected systems
   - Implement temporary mitigations
   - Preserve evidence

4. **Eradication**:
   - Remove security threats
   - Patch vulnerabilities
   - Update security controls

5. **Recovery**:
   - Restore normal operations
   - Monitor for reoccurrence
   - Update documentation

6. **Lessons Learned**:
   - Post-incident review
   - Update procedures
   - Improve security measures

### Emergency Contacts

- **Security Team**: security@logodeth.ai
- **Development Team**: dev@logodeth.ai
- **Infrastructure**: ops@logodeth.ai

## 📋 Security Checklist

### Development Security
- [ ] All dependencies up to date
- [ ] Security tests passing
- [ ] Input validation implemented
- [ ] Error handling doesn't leak information
- [ ] No secrets in code or logs
- [ ] Type hints and validation used

### Deployment Security
- [ ] Production secrets properly managed
- [ ] SSL/TLS configured correctly
- [ ] Rate limiting configured
- [ ] Monitoring and alerting active
- [ ] Container security hardened
- [ ] Network security configured

### Operational Security
- [ ] Regular security updates applied
- [ ] Security monitoring active
- [ ] Incident response plan tested
- [ ] Backup and recovery procedures tested
- [ ] Access controls reviewed
- [ ] Security training completed

## 🔗 Security Resources

### External Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls/)
- [SANS Security Guidelines](https://www.sans.org/security-resources/)

### Tools & Services
- **Vulnerability Scanning**: Snyk, GitHub Security Advisories
- **Container Scanning**: Docker Scout, Trivy
- **Code Analysis**: Bandit, SonarQube
- **Monitoring**: Datadog, New Relic, Prometheus

Remember: Security is everyone's responsibility! 🛡️🤘