# BlueprintBot v2 - Multi-stage Docker Build
# This Dockerfile creates a production-ready container with all necessary components
# including Python backend, React frontend, quantum computing libraries, and AI frameworks

# Stage 1: Base system with quantum and AI dependencies
FROM ubuntu:22.04 as base-system

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=22.13.0
ENV PYTHON_VERSION=3.11
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Basic system tools
    curl \
    wget \
    git \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    # Python dependencies
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    # Node.js dependencies
    nodejs \
    npm \
    # Quantum computing dependencies
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    libblas-dev \
    libatlas-base-dev \
    # AI/ML dependencies
    libhdf5-dev \
    libnetcdf-dev \
    pkg-config \
    # Image processing
    libopencv-dev \
    python3-opencv \
    # Database dependencies
    libpq-dev \
    libsqlite3-dev \
    # Networking
    netcat \
    # Security
    openssl \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js specific version
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs

# Install pnpm globally
RUN npm install -g pnpm@latest

# Create application user
RUN useradd -m -u 1000 blueprintbot && \
    mkdir -p /app && \
    chown -R blueprintbot:blueprintbot /app

# Stage 2: Python dependencies and quantum libraries
FROM base-system as python-deps

USER blueprintbot
WORKDIR /app

# Copy Python requirements
COPY --chown=blueprintbot:blueprintbot pyproject.toml ./

# Create virtual environment
RUN python3.11 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Install quantum computing libraries
RUN pip install \
    # Quantum computing frameworks
    qiskit[all]==0.46.0 \
    qiskit-aer==0.13.3 \
    qiskit-ibm-runtime==0.18.0 \
    qiskit-optimization==0.6.0 \
    qiskit-machine-learning==0.7.2 \
    cirq==1.3.0 \
    pennylane==0.33.1 \
    pennylane-qiskit==0.33.1 \
    # Quantum simulators
    qulacs==0.6.4 \
    pyquil==4.5.1 \
    # Quantum optimization
    dimod==0.12.14 \
    dwave-ocean-sdk==6.9.0 \
    # Advanced quantum libraries
    mitiq==0.31.0 \
    qibo==0.2.8

# Install AI/ML frameworks
RUN pip install \
    # Core ML frameworks
    torch==2.1.2 \
    torchvision==0.16.2 \
    torchaudio==2.1.2 \
    tensorflow==2.15.0 \
    # Quantum ML
    tensorflow-quantum==0.7.3 \
    # Scientific computing
    numpy==1.24.4 \
    scipy==1.11.4 \
    pandas==2.1.4 \
    scikit-learn==1.3.2 \
    # Computer vision
    opencv-python==4.8.1.78 \
    pillow==10.1.0 \
    # Natural language processing
    transformers==4.36.2 \
    tokenizers==0.15.0 \
    # Optimization
    optuna==3.5.0 \
    hyperopt==0.2.7

# Install web framework dependencies
RUN pip install \
    # Web frameworks
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    flask==3.0.0 \
    flask-cors==4.0.0 \
    flask-socketio==5.3.6 \
    # Database
    sqlalchemy==2.0.23 \
    alembic==1.13.1 \
    asyncpg==0.29.0 \
    # Caching
    redis==5.0.1 \
    # Message queues
    celery==5.3.4 \
    # API documentation
    pydantic==2.5.2 \
    # Monitoring
    prometheus-client==0.19.0 \
    # Security
    cryptography==41.0.8 \
    pyjwt==2.8.0

# Install additional scientific and engineering libraries
RUN pip install \
    # Mathematical libraries
    sympy==1.12 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    plotly==5.17.0 \
    # Engineering libraries
    pint==0.23 \
    # File processing
    pypdf==3.17.4 \
    python-docx==1.1.0 \
    openpyxl==3.1.2 \
    # Image processing
    imageio==2.33.1 \
    scikit-image==0.22.0 \
    # Networking
    httpx==0.25.2 \
    aiohttp==3.9.1 \
    websockets==12.0 \
    # Development tools
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    black==23.11.0 \
    flake8==6.1.0

# Stage 3: Frontend build
FROM base-system as frontend-build

USER blueprintbot
WORKDIR /app/frontend

# Copy frontend package files
COPY --chown=blueprintbot:blueprintbot frontend/package*.json ./
COPY --chown=blueprintbot:blueprintbot frontend/pnpm-lock.yaml ./

# Install frontend dependencies
RUN pnpm install --frozen-lockfile

# Copy frontend source code
COPY --chown=blueprintbot:blueprintbot frontend/ ./

# Build frontend for production
RUN pnpm run build

# Stage 4: Main application
FROM python-deps as main-app

# Copy source code
COPY --chown=blueprintbot:blueprintbot src/ ./src/
COPY --chown=blueprintbot:blueprintbot pyproject.toml ./

# Install the application
RUN pip install -e .

# Copy built frontend
COPY --from=frontend-build --chown=blueprintbot:blueprintbot /app/frontend/dist ./static/

# Create necessary directories
RUN mkdir -p \
    /app/data \
    /app/logs \
    /app/uploads \
    /app/cache \
    /app/quantum_circuits \
    /app/ai_models \
    /app/blueprints \
    /app/reports \
    /app/backups

# Stage 5: Production image
FROM base-system as production

USER blueprintbot
WORKDIR /app

# Copy virtual environment
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/venv ./venv

# Copy application
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/src ./src
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/static ./static
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/pyproject.toml ./
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/data ./data
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/logs ./logs
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/uploads ./uploads
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/cache ./cache
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/quantum_circuits ./quantum_circuits
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/ai_models ./ai_models
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/blueprints ./blueprints
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/reports ./reports
COPY --from=main-app --chown=blueprintbot:blueprintbot /app/backups ./backups

# Set PATH
ENV PATH="/app/venv/bin:$PATH"

# Copy startup scripts
COPY --chown=blueprintbot:blueprintbot docker/ ./docker/

# Make scripts executable
USER root
RUN chmod +x /app/docker/*.sh
USER blueprintbot

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000 8001 8002 9090

# Set default environment variables
ENV PYTHONPATH="/app/src"
ENV BLUEPRINTBOT_ENV="production"
ENV BLUEPRINTBOT_HOST="0.0.0.0"
ENV BLUEPRINTBOT_PORT="8000"
ENV BLUEPRINTBOT_WORKERS="4"
ENV BLUEPRINTBOT_LOG_LEVEL="INFO"

# Labels
LABEL maintainer="ArciTEK.AI Team"
LABEL version="2.0.0"
LABEL description="BlueprintBot v2 - AI-powered blueprint analysis with quantum computing"
LABEL org.opencontainers.image.title="BlueprintBot v2"
LABEL org.opencontainers.image.description="Advanced AI-powered blueprint analysis platform"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.vendor="ArciTEK.AI"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/NaTo1000/blueprintbot_v2"

# Default command
CMD ["/app/docker/start.sh"]

