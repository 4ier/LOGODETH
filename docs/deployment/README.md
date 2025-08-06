# LOGODETH Deployment Guide 🚀

This guide covers deploying LOGODETH in various environments, from local development to production cloud deployments.

## 🐳 Docker Deployment (Recommended)

### Local Development

```bash
# Clone and setup
git clone https://github.com/4ier/LOGODETH.git
cd LOGODETH

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

### Production Deployment

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with environment overrides
LOGODETH_ENVIRONMENT=production \
LOGODETH_OPENAI_API_KEY=sk-prod-key \
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployments

### AWS Deployment

#### Option 1: ECS with Fargate
```bash
# Build and push to ECR
aws ecr create-repository --repository-name logodeth
docker build -t logodeth .
docker tag logodeth:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/logodeth:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/logodeth:latest

# Deploy with ECS
# Use provided CloudFormation template or Terraform configs
```

#### Option 2: App Runner
```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements_multimodal.txt
run:
  runtime-version: 3.11
  command: uvicorn backend.app:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
  env:
    - name: LOGODETH_ENVIRONMENT
      value: production
```

#### Required AWS Services
- **ECS/App Runner**: Container hosting
- **ElastiCache Redis**: Caching layer  
- **Secrets Manager**: API key storage
- **CloudWatch**: Logging and monitoring
- **ALB**: Load balancing (optional)

### Google Cloud Platform

#### Cloud Run Deployment
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/logodeth
gcloud run deploy logodeth \
  --image gcr.io/$PROJECT_ID/logodeth \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LOGODETH_ENVIRONMENT=production
```

#### Required GCP Services
- **Cloud Run**: Serverless containers
- **Memorystore Redis**: Managed Redis
- **Secret Manager**: API key storage
- **Cloud Logging**: Centralized logging

### Azure Deployment

#### Container Instances
```bash
# Create resource group
az group create --name logodeth-rg --location eastus

# Deploy container
az container create \
  --resource-group logodeth-rg \
  --name logodeth \
  --image your-registry/logodeth:latest \
  --ports 8000 \
  --environment-variables LOGODETH_ENVIRONMENT=production \
  --secure-environment-variables LOGODETH_OPENAI_API_KEY=$OPENAI_KEY
```

#### Required Azure Services
- **Container Instances**: Container hosting
- **Redis Cache**: Managed Redis
- **Key Vault**: Secret management
- **Application Insights**: Monitoring

## 🖥️ Traditional Server Deployment

### Ubuntu/Debian Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Redis
sudo apt install redis-server -y
sudo systemctl enable redis-server

# Install Nginx (optional)
sudo apt install nginx -y

# Clone and setup application
git clone https://github.com/4ier/LOGODETH.git
cd LOGODETH

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements_multimodal.txt

# Configure environment
cp .env.example .env
# Edit .env with production settings

# Create systemd service
sudo cp scripts/logodeth.service /etc/systemd/system/
sudo systemctl enable logodeth
sudo systemctl start logodeth
```

### CentOS/RHEL Server

```bash
# Install EPEL and Python 3.11
sudo dnf install epel-release -y
sudo dnf install python3.11 python3-pip redis nginx -y

# Follow similar steps as Ubuntu
# Use scripts/logodeth.service for systemd
```

## 🔒 Production Configuration

### Environment Variables

```bash
# Core settings
LOGODETH_ENVIRONMENT=production
LOGODETH_DEBUG=false
LOGODETH_LOG_LEVEL=INFO

# API Keys (use secrets management)
LOGODETH_OPENAI_API_KEY=sk-prod-key
LOGODETH_ANTHROPIC_API_KEY=sk-ant-prod-key

# Database/Cache
LOGODETH_REDIS_URL=redis://prod-redis:6379
LOGODETH_REDIS_PASSWORD=secure-password

# Performance
LOGODETH_WORKER_COUNT=4
LOGODETH_API_RATE_LIMIT=50
LOGODETH_CACHE_TTL=86400

# Security
LOGODETH_SECRET_KEY=super-secure-secret-key
LOGODETH_CORS_ORIGINS=https://yourdomain.com

# Monitoring
LOGODETH_SENTRY_DSN=https://your-sentry-dsn
```

### SSL/HTTPS Configuration

#### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/yourdomain.pem;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    client_max_body_size 10M;
}
```

### Database Backup & Recovery

#### Redis Backup
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb /backup/redis_backup_$DATE.rdb

# Retention: keep last 7 days
find /backup -name "redis_backup_*.rdb" -mtime +7 -delete
```

## 📊 Monitoring & Observability

### Health Checks
```bash
# API health
curl -f http://localhost:8000/health || exit 1

# Redis health
redis-cli ping || exit 1

# Disk space
df -h / | awk 'NR==2 {if ($5+0 > 80) exit 1}'
```

### Logging Configuration
```yaml
# docker-compose.prod.yml logging
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **AlertManager**: Alert routing
- **Loki**: Log aggregation

## 🚨 Troubleshooting

### Common Issues

#### 1. API Not Responding
```bash
# Check service status
systemctl status logodeth

# Check logs
journalctl -u logodeth -f

# Check port binding
netstat -tlnp | grep 8000
```

#### 2. Redis Connection Issues
```bash
# Test Redis connection
redis-cli ping

# Check Redis logs
tail -f /var/log/redis/redis-server.log

# Restart Redis
systemctl restart redis-server
```

#### 3. Memory Issues
```bash
# Monitor memory usage
free -h
htop

# Check container memory (Docker)
docker stats

# Adjust worker count
export LOGODETH_WORKER_COUNT=2
```

#### 4. SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /etc/ssl/certs/yourdomain.pem -text -noout

# Test SSL
curl -I https://yourdomain.com

# Renew Let's Encrypt certificate
certbot renew
```

## 🔄 Updates & Rollbacks

### Zero-Downtime Updates
```bash
# Docker deployment
docker-compose pull
docker-compose up -d --no-deps api

# Traditional deployment
git pull origin main
source venv/bin/activate
pip install -r requirements_multimodal.txt
sudo systemctl reload logodeth
```

### Rollback Strategy
```bash
# Docker rollback
docker tag current_image:latest backup_image:latest
docker-compose up -d

# Git rollback
git revert HEAD
# or
git checkout previous-stable-commit
```

## 📋 Production Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] API keys secured in secrets management
- [ ] SSL certificates installed and valid
- [ ] Redis configured with persistence
- [ ] Monitoring and alerting setup
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Security audit passed

### Post-deployment
- [ ] Health checks passing
- [ ] SSL working correctly
- [ ] API endpoints responding
- [ ] Cache functioning
- [ ] Logs streaming to centralized system
- [ ] Monitoring dashboards showing metrics
- [ ] Alert channels tested
- [ ] Documentation updated

## 🆘 Support

For deployment issues:
- 📖 Check our [troubleshooting guide](../development/TROUBLESHOOTING.md)
- 🐛 Create an [issue](https://github.com/4ier/LOGODETH/issues)
- 💬 Join our [Discord](https://discord.gg/logodeth)