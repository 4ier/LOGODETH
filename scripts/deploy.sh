#!/bin/bash

# LOGODETH Deployment Script
# Supports: Heroku, Railway, DigitalOcean App Platform

set -e

echo "🚀 LOGODETH Deployment Script"
echo "=============================="

# Check for required files
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please configure .env with production values"
    exit 1
fi

# Select deployment target
echo ""
echo "Select deployment platform:"
echo "1) Heroku"
echo "2) Railway"
echo "3) DigitalOcean App Platform"
echo "4) Docker (self-hosted)"
echo "5) Cancel"
echo ""
read -p "Choice [1-5]: " choice

case $choice in
    1)
        echo "📦 Deploying to Heroku..."
        
        # Check if Heroku CLI is installed
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI not found. Please install it first:"
            echo "   https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        # Create Procfile
        echo "web: uvicorn backend.app:app --host 0.0.0.0 --port \$PORT" > Procfile
        
        # Create runtime.txt
        echo "python-3.11.6" > runtime.txt
        
        # Initialize git if needed
        git add Procfile runtime.txt
        git commit -m "Add Heroku deployment files" || true
        
        # Create Heroku app
        read -p "Enter Heroku app name: " app_name
        heroku create $app_name || true
        
        # Add Redis addon
        heroku addons:create heroku-redis:mini -a $app_name
        
        # Set environment variables
        heroku config:set OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2) -a $app_name
        
        # Deploy
        git push heroku feature/multimodal-api-integration:main
        
        echo "✅ Deployed to Heroku!"
        echo "🌐 URL: https://$app_name.herokuapp.com"
        ;;
        
    2)
        echo "📦 Deploying to Railway..."
        
        # Check if Railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo "❌ Railway CLI not found. Please install it first:"
            echo "   npm install -g @railway/cli"
            exit 1
        fi
        
        # Create railway.json
        cat > railway.json <<EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.app:app --host 0.0.0.0 --port \$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
        
        # Initialize Railway project
        railway login
        railway init
        
        # Add Redis
        railway add redis
        
        # Deploy
        railway up
        
        echo "✅ Deployed to Railway!"
        railway open
        ;;
        
    3)
        echo "📦 Preparing for DigitalOcean App Platform..."
        
        # Create app.yaml
        cat > app.yaml <<EOF
name: logodeth
region: nyc
services:
- build_command: pip install -r requirements_multimodal.txt
  environment_slug: python
  github:
    branch: feature/multimodal-api-integration
    deploy_on_push: true
    repo: YOUR_GITHUB_REPO
  http_port: 8000
  instance_count: 1
  instance_size_slug: basic-xxs
  name: api
  run_command: uvicorn backend.app:app --host 0.0.0.0 --port 8000
  source_dir: /
databases:
- engine: REDIS
  name: redis-cache
  num_nodes: 1
  size: db-s-dev-database
  version: "7"
EOF
        
        echo "✅ DigitalOcean app.yaml created!"
        echo ""
        echo "Next steps:"
        echo "1. Push code to GitHub"
        echo "2. Go to https://cloud.digitalocean.com/apps"
        echo "3. Create new app from GitHub"
        echo "4. Select this repository"
        echo "5. Review and deploy"
        ;;
        
    4)
        echo "📦 Building Docker image..."
        
        # Build image
        docker build -t logodeth:latest .
        
        echo ""
        echo "Docker image built! To deploy:"
        echo ""
        echo "Option 1 - Run locally:"
        echo "  docker run -d -p 8000:8000 --env-file .env logodeth:latest"
        echo ""
        echo "Option 2 - Push to registry:"
        echo "  docker tag logodeth:latest YOUR_REGISTRY/logodeth:latest"
        echo "  docker push YOUR_REGISTRY/logodeth:latest"
        echo ""
        echo "Option 3 - Deploy with docker-compose:"
        echo "  docker-compose up -d"
        ;;
        
    5)
        echo "Deployment cancelled."
        exit 0
        ;;
        
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

echo ""
echo "🤘 Deployment complete!"
echo ""
echo "Post-deployment checklist:"
echo "[ ] Test the health endpoint"
echo "[ ] Upload a test logo"
echo "[ ] Check API documentation (/docs)"
echo "[ ] Monitor usage statistics (/api/v1/stats/usage)"
echo "[ ] Set up monitoring alerts"
echo ""