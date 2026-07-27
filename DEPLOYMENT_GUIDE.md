# BlueprintBot v2 - Deployment Guide 🚀

This guide provides comprehensive instructions for deploying BlueprintBot v2 in various environments, from local development to enterprise production deployments.

## 📋 Prerequisites

### System Requirements
- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB minimum (16GB+ recommended for production)
- **Storage**: 50GB+ available disk space
- **Network**: Stable internet connection for quantum and AI services

### Software Requirements
- **Docker**: 20.10+ and Docker Compose 2.0+
- **Python**: 3.11+ (for local development)
- **Node.js**: 22.13.0+ (for frontend development)
- **Git**: Latest version

### API Keys and Credentials
Before deployment, obtain the following API keys:

#### Required for Full Functionality
- **IBM Quantum Token**: [IBM Quantum Network](https://quantum-computing.ibm.com/)
- **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/)
- **Hugging Face Token**: [Hugging Face](https://huggingface.co/settings/tokens)

#### Optional for Enhanced Features
- **AWS Credentials**: For cloud storage and deployment
- **Azure Credentials**: For Azure deployment
- **Google Cloud Credentials**: For GCP deployment
- **Cloudflare API Token**: For CDN and DNS management

## 🐳 Docker Deployment (Recommended)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/NaTo1000/blueprintbot_v2.git
cd blueprintbot_v2

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys and configuration

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f blueprintbot-app
```

### Environment Configuration
Edit the `.env` file with your specific configuration:

```bash
# Application Settings
BLUEPRINTBOT_ENV=production
BLUEPRINTBOT_HOST=0.0.0.0
BLUEPRINTBOT_PORT=8000
BLUEPRINTBOT_WORKERS=4

# Database Configuration
POSTGRES_PASSWORD=your-secure-password
DATABASE_URL=postgresql://blueprintbot:your-secure-password@postgres:5432/blueprintbot

# Quantum Computing
IBM_QUANTUM_TOKEN=your-ibm-quantum-token
QUANTUM_BACKEND=qasm_simulator

# AI/ML Configuration
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_TOKEN=your-huggingface-token

# Security
JWT_SECRET_KEY=your-jwt-secret-key-minimum-32-characters
ENCRYPTION_KEY=your-encryption-key-32-characters
```

### Service Architecture
The Docker Compose setup includes:

- **blueprintbot-app**: Main application server
- **postgres**: PostgreSQL database
- **redis**: Cache and message broker
- **elasticsearch**: Search and analytics
- **prometheus**: Metrics collection
- **grafana**: Monitoring dashboards
- **traefik**: Reverse proxy and load balancer
- **celery-worker**: Background task processing
- **celery-beat**: Scheduled task management

### Health Checks
```bash
# Check application health
curl http://localhost:8000/health

# Check API endpoints
curl http://localhost:8000/api/v2/health

# Check quantum system
curl http://localhost:8000/api/v2/quantum/status

# Check AI system
curl http://localhost:8000/api/v2/ai/status
```

## 🔧 Local Development Setup

### Python Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements-test.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "
from src.blueprintbot_v2.core.database import create_tables
create_tables()
"

# Start development server
python -m uvicorn src.blueprintbot_v2.api.api_server:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Development Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Running Tests
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific test categories
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m quantum       # Quantum tests (requires API keys)
pytest -m ai            # AI/ML tests (requires API keys)

# Run with coverage
pytest --cov=src --cov-report=html
```

## ☁️ Cloud Deployment

### AWS Deployment

#### Using AWS ECS
```bash
# Build and push Docker image
docker build -t blueprintbot-v2:latest .
docker tag blueprintbot-v2:latest your-account.dkr.ecr.region.amazonaws.com/blueprintbot-v2:latest
docker push your-account.dkr.ecr.region.amazonaws.com/blueprintbot-v2:latest

# Deploy using ECS CLI or AWS Console
# Configure task definitions, services, and load balancers
```

#### Using AWS EKS
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### Azure Deployment

#### Using Azure Container Instances
```bash
# Create resource group
az group create --name blueprintbot-rg --location eastus

# Deploy container
az container create \
  --resource-group blueprintbot-rg \
  --name blueprintbot-v2 \
  --image blueprintbot/v2:latest \
  --dns-name-label blueprintbot-v2 \
  --ports 8000 \
  --environment-variables \
    BLUEPRINTBOT_ENV=production \
    DATABASE_URL=your-database-url
```

#### Using Azure Kubernetes Service (AKS)
```bash
# Create AKS cluster
az aks create \
  --resource-group blueprintbot-rg \
  --name blueprintbot-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group blueprintbot-rg --name blueprintbot-cluster

# Deploy application
kubectl apply -f k8s/
```

### Google Cloud Platform Deployment

#### Using Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/blueprintbot-v2

# Deploy to Cloud Run
gcloud run deploy blueprintbot-v2 \
  --image gcr.io/your-project/blueprintbot-v2 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars BLUEPRINTBOT_ENV=production
```

#### Using Google Kubernetes Engine (GKE)
```bash
# Create GKE cluster
gcloud container clusters create blueprintbot-cluster \
  --num-nodes=3 \
  --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials blueprintbot-cluster --zone=us-central1-a

# Deploy application
kubectl apply -f k8s/
```

## 🔐 Security Configuration

### SSL/TLS Setup
```bash
# Using Let's Encrypt with Traefik (automatic)
# Configuration in docker-compose.yml handles SSL automatically

# Manual SSL certificate setup
# Place certificates in:
# - /etc/ssl/certs/infinite2025.com.crt
# - /etc/ssl/private/infinite2025.com.key
```

### Firewall Configuration
```bash
# Allow necessary ports
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8000/tcp  # Application (if direct access needed)
ufw allow 22/tcp    # SSH (for management)

# Block unnecessary ports
ufw deny 5432/tcp   # PostgreSQL (should only be accessible internally)
ufw deny 6379/tcp   # Redis (should only be accessible internally)
```

### Environment Security
```bash
# Set secure file permissions
chmod 600 .env
chmod 600 secrets/*

# Use Docker secrets for sensitive data
docker secret create postgres_password /path/to/postgres_password.txt
docker secret create jwt_secret /path/to/jwt_secret.txt
```

## 📊 Monitoring and Observability

### Prometheus Metrics
Access Prometheus at `http://localhost:9091`

Key metrics to monitor:
- Application response times
- Error rates
- Quantum processing times
- AI model inference times
- Database performance
- Resource utilization

### Grafana Dashboards
Access Grafana at `http://localhost:3000`
- Default credentials: admin/admin123 (change immediately)
- Pre-configured dashboards for all services
- Alerting rules for critical metrics

### Log Management
```bash
# View application logs
docker-compose logs -f blueprintbot-app

# View all service logs
docker-compose logs -f

# Configure log rotation
# Logs are automatically rotated in production setup
```

### Health Monitoring
```bash
# Set up health check endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v2/health
curl http://localhost:8000/metrics

# Configure external monitoring
# Use services like Pingdom, UptimeRobot, or Datadog
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Automated backup (configured in docker-compose.yml)
# Manual backup
docker-compose exec postgres pg_dump -U blueprintbot blueprintbot > backup.sql

# Restore from backup
docker-compose exec -T postgres psql -U blueprintbot blueprintbot < backup.sql
```

### Application Data Backup
```bash
# Backup uploaded files and data
tar -czf blueprintbot-data-$(date +%Y%m%d).tar.gz \
  data/ uploads/ quantum_circuits/ ai_models/

# Backup to cloud storage (example with AWS S3)
aws s3 cp blueprintbot-data-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
```

### Disaster Recovery
```bash
# Full system restore procedure
# 1. Deploy fresh infrastructure
# 2. Restore database from backup
# 3. Restore application data
# 4. Update DNS to point to new deployment
# 5. Verify all services are operational
```

## 🚀 Performance Optimization

### Scaling Strategies

#### Horizontal Scaling
```bash
# Scale application containers
docker-compose up -d --scale blueprintbot-app=3

# Use load balancer (Traefik configured automatically)
# Configure database read replicas for read-heavy workloads
```

#### Vertical Scaling
```bash
# Update docker-compose.yml resource limits
services:
  blueprintbot-app:
    deploy:
      resources:
        limits:
          cpus: '8.0'
          memory: 16G
        reservations:
          cpus: '4.0'
          memory: 8G
```

### Caching Configuration
```bash
# Redis caching is pre-configured
# Tune cache settings in .env
CACHE_TTL=3600
CACHE_MAX_SIZE=1000

# Enable CDN for static assets
# Configure Cloudflare or AWS CloudFront
```

### Database Optimization
```bash
# PostgreSQL tuning in docker-compose.yml
environment:
  - POSTGRES_SHARED_PRELOAD_LIBRARIES=pg_stat_statements
  - POSTGRES_MAX_CONNECTIONS=200
  - POSTGRES_SHARED_BUFFERS=256MB
  - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
```

## 🔧 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
docker-compose logs blueprintbot-app

# Common causes:
# - Missing environment variables
# - Database connection issues
# - Port conflicts
# - Insufficient resources
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U blueprintbot -d blueprintbot -c "SELECT 1;"

# Reset database
docker-compose down -v
docker-compose up -d postgres
# Wait for database to initialize, then start other services
```

#### Quantum Processing Errors
```bash
# Check quantum service status
curl http://localhost:8000/api/v2/quantum/status

# Common causes:
# - Invalid IBM Quantum token
# - Network connectivity issues
# - Quantum backend unavailable
# - Circuit complexity exceeds limits
```

#### AI/ML Model Issues
```bash
# Check AI service status
curl http://localhost:8000/api/v2/ai/status

# Common causes:
# - Missing model files
# - Insufficient GPU memory
# - API rate limits exceeded
# - Model compatibility issues
```

### Performance Issues
```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:8000/metrics

# Profile application performance
# Use built-in profiling endpoints (development mode only)
```

### Log Analysis
```bash
# Search logs for errors
docker-compose logs blueprintbot-app | grep ERROR

# Monitor real-time logs
docker-compose logs -f --tail=100 blueprintbot-app

# Export logs for analysis
docker-compose logs blueprintbot-app > application.log
```

## 📞 Support and Maintenance

### Regular Maintenance Tasks
```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Clean up unused Docker resources
docker system prune -a

# Update SSL certificates (automatic with Let's Encrypt)
# Manual renewal if needed:
certbot renew

# Database maintenance
docker-compose exec postgres psql -U blueprintbot -d blueprintbot -c "VACUUM ANALYZE;"
```

### Monitoring Checklist
- [ ] Application health endpoints responding
- [ ] Database performance within acceptable limits
- [ ] Quantum services accessible
- [ ] AI models loading correctly
- [ ] SSL certificates valid and not expiring
- [ ] Backup processes running successfully
- [ ] Log rotation working properly
- [ ] Resource utilization within limits

### Getting Help
- **GitHub Issues**: [Report bugs and request features](https://github.com/NaTo1000/blueprintbot_v2/issues)
- **Documentation**: [Complete documentation](https://docs.infinite2025.com)
- **Community**: [Join our Discord](https://discord.gg/blueprintbot)
- **Enterprise Support**: enterprise@infinite2025.com

---

**© 2024 ArciTEK.AI - All Rights Reserved | infinite♾2025**

