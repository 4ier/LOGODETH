#!/bin/bash
# LOGODETH VPS Deployment Script
# Usage: ./scripts/deploy-vps.sh

set -e

echo "🚀 Starting LOGODETH VPS deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should not be run as root${NC}" 
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install Docker if not exists
if ! command_exists docker; then
    echo -e "${YELLOW}🐳 Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}Docker installed successfully${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

# Install Docker Compose if not exists
if ! command_exists docker-compose; then
    echo -e "${YELLOW}📦 Installing Docker Compose...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}Docker Compose installed successfully${NC}"
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

# Install Git if not exists
if ! command_exists git; then
    echo -e "${YELLOW}📦 Installing Git...${NC}"
    sudo apt install git -y
else
    echo -e "${GREEN}✅ Git already installed${NC}"
fi

# Clone or update repository
if [ ! -d "LOGODETH" ]; then
    echo -e "${YELLOW}📥 Cloning LOGODETH repository...${NC}"
    git clone https://github.com/4ier/LOGODETH.git
    cd LOGODETH
else
    echo -e "${YELLOW}🔄 Updating LOGODETH repository...${NC}"
    cd LOGODETH
    git pull origin main
fi

# Setup environment file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️ Setting up environment file...${NC}"
    cp .env.example .env
    echo -e "${RED}❗ IMPORTANT: Edit .env file with your API keys:${NC}"
    echo "nano .env"
    echo "Required: LOGODETH_OPENAI_API_KEY"
    echo "Optional: LOGODETH_ANTHROPIC_API_KEY"
    read -p "Press Enter when you've configured the .env file..."
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
sudo mkdir -p /var/log/logodeth
sudo mkdir -p /var/lib/logodeth/redis
sudo chown -R $USER:$USER /var/log/logodeth /var/lib/logodeth

# Setup log rotation
echo -e "${YELLOW}📋 Setting up log rotation...${NC}"
sudo tee /etc/logrotate.d/logodeth > /dev/null <<EOF
/var/log/logodeth/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

# Deploy with Docker Compose
echo -e "${YELLOW}🚀 Deploying LOGODETH...${NC}"
docker-compose -f docker-compose.prod.yml down --remove-orphans
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Health check
echo -e "${YELLOW}🏥 Performing health check...${NC}"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ LOGODETH is healthy!${NC}"
        break
    fi
    
    attempt=$((attempt + 1))
    echo -e "${YELLOW}Attempt $attempt/$max_attempts - waiting for health check...${NC}"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}❌ Health check failed after $max_attempts attempts${NC}"
    echo "Check logs with: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

# Setup systemd service (optional)
read -p "Do you want to setup systemd service for auto-restart? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚙️ Setting up systemd service...${NC}"
    
    sudo tee /etc/systemd/system/logodeth.service > /dev/null <<EOF
[Unit]
Description=LOGODETH Metal Logo Recognition Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable logodeth.service
    echo -e "${GREEN}✅ Systemd service created and enabled${NC}"
fi

# Setup Nginx reverse proxy (optional)
read -p "Do you want to setup Nginx reverse proxy with SSL? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🔧 Installing Nginx and Certbot...${NC}"
    sudo apt install nginx certbot python3-certbot-nginx -y
    
    read -p "Enter your domain name (e.g., logodeth.yourdomain.com): " domain_name
    
    if [ ! -z "$domain_name" ]; then
        sudo tee /etc/nginx/sites-available/logodeth > /dev/null <<EOF
server {
    listen 80;
    server_name $domain_name;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # File upload settings
        client_max_body_size 10M;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
EOF
        
        sudo ln -sf /etc/nginx/sites-available/logodeth /etc/nginx/sites-enabled/
        sudo nginx -t
        
        if [ $? -eq 0 ]; then
            sudo systemctl reload nginx
            echo -e "${GREEN}✅ Nginx configured for $domain_name${NC}"
            
            # Setup SSL
            echo -e "${YELLOW}🔐 Setting up SSL certificate...${NC}"
            sudo certbot --nginx -d $domain_name --non-interactive --agree-tos --email admin@$domain_name
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ SSL certificate installed successfully${NC}"
                echo -e "${GREEN}🌐 Your site is now available at: https://$domain_name${NC}"
            fi
        else
            echo -e "${RED}❌ Nginx configuration error${NC}"
        fi
    fi
fi

# Setup monitoring script
echo -e "${YELLOW}📊 Setting up monitoring script...${NC}"
tee ~/logodeth-monitor.sh > /dev/null <<EOF
#!/bin/bash
# LOGODETH Monitoring Script

cd $(pwd)

# Check if containers are running
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "⚠️ LOGODETH containers are not running, restarting..."
    docker-compose -f docker-compose.prod.yml up -d
fi

# Check health endpoint
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️ Health check failed, restarting services..."
    docker-compose -f docker-compose.prod.yml restart api
fi

# Cleanup old logs
find /var/log/logodeth -name "*.log" -mtime +7 -delete 2>/dev/null

echo "✅ Monitoring check completed at \$(date)"
EOF

chmod +x ~/logodeth-monitor.sh

# Add to crontab
echo -e "${YELLOW}⏰ Setting up monitoring cron job...${NC}"
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/logodeth-monitor.sh >> /var/log/logodeth/monitor.log 2>&1") | crontab -

echo -e "${GREEN}🎉 LOGODETH deployment completed successfully!${NC}"
echo
echo "📋 Summary:"
echo "• Application URL: http://$(curl -s ifconfig.me):8000"
echo "• Health check: http://$(curl -s ifconfig.me):8000/health"
echo "• API docs: http://$(curl -s ifconfig.me):8000/docs"
echo
echo "📝 Next steps:"
echo "1. Configure your DNS to point to this server"
echo "2. Test the API with: curl http://$(curl -s ifconfig.me):8000/health"
echo "3. Monitor logs with: docker-compose -f docker-compose.prod.yml logs -f"
echo "4. Update with: git pull && docker-compose -f docker-compose.prod.yml up -d"
echo
echo "🔧 Useful commands:"
echo "• View logs: docker-compose -f docker-compose.prod.yml logs"
echo "• Restart: docker-compose -f docker-compose.prod.yml restart"
echo "• Update: git pull && docker-compose -f docker-compose.prod.yml up -d"
echo "• Stop: docker-compose -f docker-compose.prod.yml down"