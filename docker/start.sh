#!/bin/bash

# BlueprintBot v2 - Production Startup Script
# This script handles the complete startup sequence for the containerized application

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

quantum_log() {
    echo -e "${PURPLE}[$(date +'%Y-%m-%d %H:%M:%S')] QUANTUM: $1${NC}"
}

ai_log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')] AI: $1${NC}"
}

# Configuration
export PYTHONPATH="/app/src:$PYTHONPATH"
export BLUEPRINTBOT_ENV="${BLUEPRINTBOT_ENV:-production}"
export BLUEPRINTBOT_HOST="${BLUEPRINTBOT_HOST:-0.0.0.0}"
export BLUEPRINTBOT_PORT="${BLUEPRINTBOT_PORT:-8000}"
export BLUEPRINTBOT_WORKERS="${BLUEPRINTBOT_WORKERS:-4}"
export BLUEPRINTBOT_LOG_LEVEL="${BLUEPRINTBOT_LOG_LEVEL:-INFO}"

# Database configuration
export DATABASE_URL="${DATABASE_URL:-sqlite:///app/data/blueprintbot.db}"
export REDIS_URL="${REDIS_URL:-redis://localhost:6379/0}"

# Quantum computing configuration
export QISKIT_SETTINGS="${QISKIT_SETTINGS:-/app/quantum_circuits/qiskit_settings.json}"
export IBM_QUANTUM_TOKEN="${IBM_QUANTUM_TOKEN:-}"
export QUANTUM_BACKEND="${QUANTUM_BACKEND:-qasm_simulator}"

# AI configuration
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
export HUGGINGFACE_TOKEN="${HUGGINGFACE_TOKEN:-}"
export AI_MODEL_CACHE_DIR="/app/ai_models"

# Monitoring configuration
export PROMETHEUS_PORT="${PROMETHEUS_PORT:-9090}"
export GRAFANA_PORT="${GRAFANA_PORT:-3000}"

# Security configuration
export JWT_SECRET_KEY="${JWT_SECRET_KEY:-$(openssl rand -hex 32)}"
export ENCRYPTION_KEY="${ENCRYPTION_KEY:-$(openssl rand -hex 32)}"

# Performance configuration
export MAX_UPLOAD_SIZE="${MAX_UPLOAD_SIZE:-104857600}" # 100MB
export MAX_CONCURRENT_ANALYSES="${MAX_CONCURRENT_ANALYSES:-10}"
export QUANTUM_TIMEOUT="${QUANTUM_TIMEOUT:-300}" # 5 minutes
export AI_TIMEOUT="${AI_TIMEOUT:-600}" # 10 minutes

# Function to check system requirements
check_system_requirements() {
    log "Checking system requirements..."
    
    # Check memory
    TOTAL_MEM=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    if [ "$TOTAL_MEM" -lt 2048 ]; then
        warn "Low memory detected: ${TOTAL_MEM}MB. Recommended: 4GB+"
    else
        info "Memory check passed: ${TOTAL_MEM}MB"
    fi
    
    # Check disk space
    DISK_SPACE=$(df /app | awk 'NR==2 {print $4}')
    if [ "$DISK_SPACE" -lt 1048576 ]; then # 1GB in KB
        warn "Low disk space detected. Recommended: 10GB+ free space"
    else
        info "Disk space check passed"
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    info "Python version: $PYTHON_VERSION"
    
    # Check key Python packages
    python3 -c "import qiskit; print(f'Qiskit version: {qiskit.__version__}')" || warn "Qiskit not available"
    python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')" || warn "PyTorch not available"
    python3 -c "import tensorflow; print(f'TensorFlow version: {tensorflow.__version__}')" || warn "TensorFlow not available"
}

# Function to initialize directories
initialize_directories() {
    log "Initializing application directories..."
    
    # Create required directories with proper permissions
    mkdir -p /app/data/{database,cache,temp}
    mkdir -p /app/logs/{application,quantum,ai,security,performance}
    mkdir -p /app/uploads/{blueprints,images,documents}
    mkdir -p /app/quantum_circuits/{saved,templates,results}
    mkdir -p /app/ai_models/{pretrained,custom,cache}
    mkdir -p /app/blueprints/{processed,archive,exports}
    mkdir -p /app/reports/{analysis,performance,security}
    mkdir -p /app/backups/{database,configurations,models}
    
    # Set proper permissions
    chmod -R 755 /app/data
    chmod -R 755 /app/logs
    chmod -R 755 /app/uploads
    chmod -R 755 /app/quantum_circuits
    chmod -R 755 /app/ai_models
    chmod -R 755 /app/blueprints
    chmod -R 755 /app/reports
    chmod -R 755 /app/backups
    
    info "Directory initialization completed"
}

# Function to initialize database
initialize_database() {
    log "Initializing database..."
    
    # Check if database exists
    if [ ! -f "/app/data/database/blueprintbot.db" ]; then
        info "Creating new database..."
        python3 -c "
from src.blueprintbot_v2.core.database import create_tables
create_tables()
print('Database tables created successfully')
" || error "Failed to create database tables"
    else
        info "Database already exists, checking for migrations..."
        # Run migrations if needed
        python3 -c "
from src.blueprintbot_v2.core.database import run_migrations
run_migrations()
print('Database migrations completed')
" || warn "Database migration check failed"
    fi
}

# Function to initialize quantum computing
initialize_quantum() {
    quantum_log "Initializing quantum computing environment..."
    
    # Create quantum settings file
    cat > /app/quantum_circuits/qiskit_settings.json << EOF
{
    "default_backend": "${QUANTUM_BACKEND}",
    "max_qubits": 32,
    "max_shots": 8192,
    "optimization_level": 3,
    "resilience_level": 1,
    "transpiler_settings": {
        "basis_gates": ["cx", "id", "rz", "sx", "x"],
        "coupling_map": null,
        "initial_layout": null
    },
    "error_mitigation": {
        "enabled": true,
        "method": "zero_noise_extrapolation"
    }
}
EOF
    
    # Test quantum backend availability
    python3 -c "
from qiskit import IBMQ
from qiskit.providers.aer import AerSimulator
import json

# Test local simulator
simulator = AerSimulator()
print(f'Local quantum simulator available: {simulator.name()}')

# Test IBM Quantum access if token provided
if '${IBM_QUANTUM_TOKEN}':
    try:
        IBMQ.save_account('${IBM_QUANTUM_TOKEN}', overwrite=True)
        provider = IBMQ.load_account()
        backends = provider.backends()
        print(f'IBM Quantum backends available: {len(backends)}')
    except Exception as e:
        print(f'IBM Quantum connection failed: {e}')
else:
    print('IBM Quantum token not provided, using local simulator only')
" || warn "Quantum initialization check failed"
    
    quantum_log "Quantum computing environment initialized"
}

# Function to initialize AI models
initialize_ai() {
    ai_log "Initializing AI/ML environment..."
    
    # Create AI configuration
    cat > /app/ai_models/ai_config.json << EOF
{
    "models": {
        "blueprint_analyzer": {
            "type": "computer_vision",
            "framework": "pytorch",
            "model_path": "/app/ai_models/pretrained/blueprint_analyzer.pth",
            "input_size": [224, 224],
            "batch_size": 32
        },
        "text_processor": {
            "type": "nlp",
            "framework": "transformers",
            "model_name": "bert-base-uncased",
            "cache_dir": "/app/ai_models/cache"
        },
        "quantum_optimizer": {
            "type": "quantum_ml",
            "framework": "pennylane",
            "backend": "default.qubit",
            "shots": 1000
        }
    },
    "training": {
        "enabled": false,
        "data_dir": "/app/data/training",
        "checkpoint_dir": "/app/ai_models/checkpoints",
        "log_dir": "/app/logs/ai"
    },
    "inference": {
        "batch_size": 16,
        "max_sequence_length": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }
}
EOF
    
    # Test AI frameworks
    python3 -c "
import torch
import tensorflow as tf
from transformers import pipeline

print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'TensorFlow version: {tf.__version__}')

# Test basic model loading
try:
    classifier = pipeline('sentiment-analysis')
    print('Transformers pipeline test: SUCCESS')
except Exception as e:
    print(f'Transformers pipeline test: FAILED - {e}')
" || warn "AI framework test failed"
    
    ai_log "AI/ML environment initialized"
}

# Function to start monitoring services
start_monitoring() {
    log "Starting monitoring services..."
    
    # Start Prometheus metrics server
    python3 -c "
from prometheus_client import start_http_server
import time
import threading

def start_metrics_server():
    start_http_server(${PROMETHEUS_PORT})
    print('Prometheus metrics server started on port ${PROMETHEUS_PORT}')

# Start in background thread
metrics_thread = threading.Thread(target=start_metrics_server, daemon=True)
metrics_thread.start()
" &
    
    info "Monitoring services started"
}

# Function to perform health checks
health_check() {
    log "Performing health checks..."
    
    # Check Python environment
    python3 -c "
import sys
import pkg_resources
import importlib

required_packages = [
    'qiskit', 'torch', 'tensorflow', 'fastapi', 'uvicorn',
    'sqlalchemy', 'redis', 'numpy', 'pandas', 'opencv-python'
]

missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package.replace('-', '_'))
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'Missing packages: {missing_packages}')
    sys.exit(1)
else:
    print('All required packages available')
" || error "Health check failed - missing required packages"
    
    # Check file permissions
    if [ ! -w "/app/data" ] || [ ! -w "/app/logs" ]; then
        error "Health check failed - insufficient file permissions"
        exit 1
    fi
    
    # Check network connectivity
    if ! nc -z localhost 8000 2>/dev/null; then
        info "Port 8000 available for binding"
    else
        warn "Port 8000 already in use"
    fi
    
    log "Health checks completed successfully"
}

# Function to start the application
start_application() {
    log "Starting BlueprintBot v2 application..."
    
    # Export all environment variables
    export PYTHONPATH="/app/src"
    
    # Start the main application
    if [ "$BLUEPRINTBOT_ENV" = "development" ]; then
        info "Starting in development mode..."
        python3 -m uvicorn src.blueprintbot_v2.api.api_server:app \
            --host "$BLUEPRINTBOT_HOST" \
            --port "$BLUEPRINTBOT_PORT" \
            --reload \
            --log-level debug
    else
        info "Starting in production mode with $BLUEPRINTBOT_WORKERS workers..."
        python3 -m gunicorn src.blueprintbot_v2.api.api_server:app \
            --bind "$BLUEPRINTBOT_HOST:$BLUEPRINTBOT_PORT" \
            --workers "$BLUEPRINTBOT_WORKERS" \
            --worker-class uvicorn.workers.UvicornWorker \
            --log-level "$BLUEPRINTBOT_LOG_LEVEL" \
            --access-logfile /app/logs/application/access.log \
            --error-logfile /app/logs/application/error.log \
            --capture-output \
            --enable-stdio-inheritance
    fi
}

# Function to handle graceful shutdown
cleanup() {
    log "Received shutdown signal, performing cleanup..."
    
    # Kill background processes
    jobs -p | xargs -r kill
    
    # Save current state
    python3 -c "
try:
    from src.blueprintbot_v2.core.state_manager import save_application_state
    save_application_state()
    print('Application state saved')
except Exception as e:
    print(f'Failed to save application state: {e}')
" || warn "Failed to save application state"
    
    log "Cleanup completed"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Main execution
main() {
    log "Starting BlueprintBot v2 initialization..."
    
    # ASCII Art Banner
    cat << 'EOF'
    
     ██████╗ ██╗     ██╗   ██╗███████╗██████╗ ██████╗ ██╗███╗   ██╗████████╗██████╗  ██████╗ ████████╗    ██╗   ██╗██████╗ 
     ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║╚════██╗
     ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║   ██║       ██║   ██║ █████╔╝
     ██╔══██╗██║     ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝██╔═══╝ 
     ██████╔╝███████╗╚██████╔╝███████╗██║     ██║  ██║██║██║ ╚████║   ██║   ██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████╗
     ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝
                                                                                                                              
                                        ArciTEK.AI - Advanced Blueprint Analysis Platform
                                            Quantum Computing • Artificial Intelligence • Engineering
                                                            infinite♾2025
EOF
    
    info "Environment: $BLUEPRINTBOT_ENV"
    info "Host: $BLUEPRINTBOT_HOST:$BLUEPRINTBOT_PORT"
    info "Workers: $BLUEPRINTBOT_WORKERS"
    info "Log Level: $BLUEPRINTBOT_LOG_LEVEL"
    
    # Run initialization steps
    check_system_requirements
    initialize_directories
    initialize_database
    initialize_quantum
    initialize_ai
    start_monitoring
    health_check
    
    log "Initialization completed successfully!"
    log "Starting application server..."
    
    # Start the application (this will block)
    start_application
}

# Run main function
main "$@"

