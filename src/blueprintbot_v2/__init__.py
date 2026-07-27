"""
BlueprintBot v2 - Advanced AI-powered construction planning platform with quantum integration.

This package provides a comprehensive suite of tools for construction industry automation,
leveraging advanced AI techniques, quantum computing, and enterprise-grade infrastructure.

Key Features:
- Multi-agent AI coordination with 200+ specialized agents
- Quantum-enhanced optimization algorithms
- Real-time plan analysis and material estimation
- Automated compliance and regulatory checking
- Enterprise-grade scalability and security
- Advanced visualization and reporting capabilities
- Comprehensive API ecosystem
- Cloud-native architecture with microservices
- Advanced machine learning and deep learning models
- Quantum machine learning integration
- Real-time collaboration and workflow management
- Advanced analytics and business intelligence
- Comprehensive testing and quality assurance
- Enterprise security and compliance frameworks
- Advanced monitoring and observability
- Comprehensive documentation and support
"""

import logging
import sys
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import os
from dataclasses import dataclass, field
from enum import Enum, auto
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import threading
from contextlib import asynccontextmanager, contextmanager
import warnings
import importlib.metadata
from packaging import version

# Version information
__version__ = "2.0.0"
__author__ = "BlueprintBot Team"
__email__ = "team@blueprintbot.ai"
__license__ = "MIT"
__copyright__ = "Copyright 2024 BlueprintBot Team"

# Package metadata
__title__ = "blueprintbot-v2"
__description__ = "Advanced AI-powered construction planning platform with quantum integration"
__url__ = "https://github.com/NaTo1000/blueprintbot_v2"
__download_url__ = "https://github.com/NaTo1000/blueprintbot_v2/archive/v2.0.0.tar.gz"
__docs_url__ = "https://blueprintbot-v2.readthedocs.io/"
__tracker_url__ = "https://github.com/NaTo1000/blueprintbot_v2/issues"

# Package constants
DEFAULT_CONFIG_PATH = Path.home() / ".blueprintbot" / "config.yaml"
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_MAX_WORKERS = min(32, (os.cpu_count() or 1) + 4)
DEFAULT_QUANTUM_BACKEND = "qiskit_aer"
DEFAULT_AI_MODEL_CACHE_SIZE = 1000
DEFAULT_API_TIMEOUT = 30.0
DEFAULT_DATABASE_POOL_SIZE = 20
DEFAULT_REDIS_POOL_SIZE = 10
DEFAULT_CELERY_CONCURRENCY = 4

# Environment variable names
ENV_CONFIG_PATH = "BLUEPRINTBOT_CONFIG_PATH"
ENV_LOG_LEVEL = "BLUEPRINTBOT_LOG_LEVEL"
ENV_DEBUG = "BLUEPRINTBOT_DEBUG"
ENV_QUANTUM_TOKEN = "BLUEPRINTBOT_QUANTUM_TOKEN"
ENV_DATABASE_URL = "BLUEPRINTBOT_DATABASE_URL"
ENV_REDIS_URL = "BLUEPRINTBOT_REDIS_URL"
ENV_SECRET_KEY = "BLUEPRINTBOT_SECRET_KEY"
ENV_API_KEY = "BLUEPRINTBOT_API_KEY"
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"
ENV_OPENAI_API_BASE = "OPENAI_API_BASE"

# Supported file formats
SUPPORTED_PLAN_FORMATS = {
    "pdf": [".pdf"],
    "image": [".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp"],
    "cad": [".dwg", ".dxf", ".dwf", ".dgn"],
    "bim": [".ifc", ".rvt", ".rfa", ".nwd", ".nwc"],
    "vector": [".svg", ".eps", ".ai"],
    "archive": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

# AI model configurations
AI_MODEL_CONFIGS = {
    "plan_analyzer": {
        "model_type": "transformer",
        "architecture": "vision_transformer",
        "input_size": (224, 224, 3),
        "num_classes": 1000,
        "hidden_size": 768,
        "num_layers": 12,
        "num_heads": 12,
        "mlp_dim": 3072,
        "dropout_rate": 0.1,
        "attention_dropout_rate": 0.1,
    },
    "material_estimator": {
        "model_type": "neural_network",
        "architecture": "feed_forward",
        "input_size": 512,
        "hidden_sizes": [1024, 512, 256, 128],
        "output_size": 100,
        "activation": "relu",
        "dropout_rate": 0.2,
        "batch_norm": True,
    },
    "compliance_checker": {
        "model_type": "ensemble",
        "base_models": ["random_forest", "gradient_boosting", "neural_network"],
        "meta_learner": "logistic_regression",
        "cv_folds": 5,
        "random_state": 42,
    },
    "quantum_optimizer": {
        "model_type": "quantum_neural_network",
        "num_qubits": 16,
        "num_layers": 4,
        "entanglement": "linear",
        "rotation_gates": ["rx", "ry", "rz"],
        "entangling_gate": "cx",
        "measurement_basis": "z",
    },
}

# Quantum computing configurations
QUANTUM_CONFIGS = {
    "qiskit": {
        "backend_name": "qasm_simulator",
        "shots": 1024,
        "optimization_level": 3,
        "seed_simulator": 42,
        "seed_transpiler": 42,
        "memory": True,
        "max_parallel_threads": 0,
        "max_parallel_experiments": 1,
        "max_memory_mb": 4096,
    },
    "cirq": {
        "simulator": "cirq.Simulator",
        "repetitions": 1000,
        "seed": 42,
        "dtype": "complex64",
    },
    "pennylane": {
        "device": "default.qubit",
        "wires": 16,
        "shots": 1000,
        "analytic": False,
        "cache": True,
    },
}

# Database configurations
DATABASE_CONFIGS = {
    "postgresql": {
        "driver": "asyncpg",
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": False,
        "echo_pool": False,
        "future": True,
    },
    "redis": {
        "encoding": "utf-8",
        "decode_responses": True,
        "socket_timeout": 5.0,
        "socket_connect_timeout": 5.0,
        "socket_keepalive": True,
        "socket_keepalive_options": {},
        "connection_pool_kwargs": {
            "max_connections": 50,
            "retry_on_timeout": True,
        },
    },
}

# API configurations
API_CONFIGS = {
    "fastapi": {
        "title": "BlueprintBot v2 API",
        "description": "Advanced AI-powered construction planning platform API",
        "version": __version__,
        "openapi_version": "3.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "swagger_ui_parameters": {
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "none",
            "operationsSorter": "method",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
        },
    },
    "cors": {
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": ["*"],
        "max_age": 600,
    },
    "rate_limiting": {
        "default_rate": "1000/minute",
        "burst_rate": "100/second",
        "authenticated_rate": "10000/minute",
        "premium_rate": "100000/minute",
        "storage_uri": "redis://localhost:6379",
        "strategy": "sliding_window",
    },
}

# Security configurations
SECURITY_CONFIGS = {
    "jwt": {
        "algorithm": "HS256",
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7,
        "issuer": "blueprintbot-v2",
        "audience": "blueprintbot-v2-users",
    },
    "password": {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digits": True,
        "require_symbols": True,
        "schemes": ["bcrypt"],
        "deprecated": ["auto"],
        "bcrypt__rounds": 12,
    },
    "encryption": {
        "algorithm": "AES-256-GCM",
        "key_derivation": "PBKDF2",
        "iterations": 100000,
        "salt_length": 32,
        "iv_length": 12,
        "tag_length": 16,
    },
}

# Monitoring and observability configurations
MONITORING_CONFIGS = {
    "prometheus": {
        "metrics_path": "/metrics",
        "registry": "default",
        "multiprocess": True,
        "buckets": [0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0],
    },
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "level": "DEBUG",
                "formatter": "detailed",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "blueprintbot_v2.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "blueprintbot_v2": {
                "handlers": ["default", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    },
    "tracing": {
        "service_name": "blueprintbot-v2",
        "jaeger_endpoint": "http://localhost:14268/api/traces",
        "sampling_rate": 0.1,
        "max_tag_value_length": 256,
        "max_spans": 1000,
    },
}

# Cloud and deployment configurations
CLOUD_CONFIGS = {
    "kubernetes": {
        "namespace": "blueprintbot-v2",
        "deployment_name": "blueprintbot-v2-api",
        "service_name": "blueprintbot-v2-service",
        "ingress_name": "blueprintbot-v2-ingress",
        "config_map_name": "blueprintbot-v2-config",
        "secret_name": "blueprintbot-v2-secrets",
        "replicas": 3,
        "max_replicas": 10,
        "cpu_request": "500m",
        "cpu_limit": "2000m",
        "memory_request": "1Gi",
        "memory_limit": "4Gi",
        "health_check_path": "/health",
        "readiness_check_path": "/ready",
    },
    "docker": {
        "base_image": "python:3.11-slim",
        "working_dir": "/app",
        "user": "blueprintbot",
        "uid": 1000,
        "gid": 1000,
        "port": 8000,
        "health_check_interval": "30s",
        "health_check_timeout": "10s",
        "health_check_retries": 3,
    },
}

# Performance and optimization configurations
PERFORMANCE_CONFIGS = {
    "caching": {
        "default_ttl": 3600,  # 1 hour
        "max_size": 1000,
        "eviction_policy": "lru",
        "compression": True,
        "serialization": "pickle",
    },
    "connection_pooling": {
        "database_pool_size": 20,
        "database_max_overflow": 30,
        "redis_pool_size": 10,
        "http_pool_size": 100,
        "http_pool_maxsize": 100,
        "http_pool_block": False,
    },
    "async_processing": {
        "max_workers": DEFAULT_MAX_WORKERS,
        "thread_pool_size": 20,
        "process_pool_size": 4,
        "queue_size": 1000,
        "batch_size": 100,
        "batch_timeout": 5.0,
    },
    "gpu_acceleration": {
        "enabled": True,
        "device": "cuda",
        "memory_fraction": 0.8,
        "allow_growth": True,
        "mixed_precision": True,
    },
}


class LogLevel(Enum):
    """Enumeration for log levels."""
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class QuantumBackend(Enum):
    """Enumeration for quantum computing backends."""
    QISKIT_AER = "qiskit_aer"
    QISKIT_IBM = "qiskit_ibm"
    CIRQ = "cirq"
    PENNYLANE = "pennylane"
    BRAKET = "braket"
    PYTKET = "pytket"


class AIModelType(Enum):
    """Enumeration for AI model types."""
    TRANSFORMER = "transformer"
    NEURAL_NETWORK = "neural_network"
    ENSEMBLE = "ensemble"
    QUANTUM_NEURAL_NETWORK = "quantum_neural_network"
    CONVOLUTIONAL = "convolutional"
    RECURRENT = "recurrent"
    REINFORCEMENT_LEARNING = "reinforcement_learning"


class DatabaseType(Enum):
    """Enumeration for database types."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"
    NEO4J = "neo4j"


class CloudProvider(Enum):
    """Enumeration for cloud providers."""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"
    LOCAL = "local"


@dataclass
class SystemInfo:
    """System information and capabilities."""
    version: str = __version__
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    platform: str = sys.platform
    cpu_count: int = os.cpu_count() or 1
    max_workers: int = DEFAULT_MAX_WORKERS
    quantum_backends: List[str] = field(default_factory=lambda: [backend.value for backend in QuantumBackend])
    ai_models: List[str] = field(default_factory=lambda: list(AI_MODEL_CONFIGS.keys()))
    supported_formats: Dict[str, List[str]] = field(default_factory=lambda: SUPPORTED_PLAN_FORMATS.copy())
    
    def __post_init__(self):
        """Post-initialization processing."""
        self.max_workers = min(32, self.cpu_count + 4)


@dataclass
class Configuration:
    """Main configuration class for BlueprintBot v2."""
    # Basic settings
    debug: bool = False
    log_level: LogLevel = LogLevel.INFO
    config_path: Optional[Path] = None
    
    # AI and ML settings
    ai_model_cache_size: int = DEFAULT_AI_MODEL_CACHE_SIZE
    quantum_backend: QuantumBackend = QuantumBackend.QISKIT_AER
    quantum_token: Optional[str] = None
    
    # Database settings
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    database_pool_size: int = DEFAULT_DATABASE_POOL_SIZE
    redis_pool_size: int = DEFAULT_REDIS_POOL_SIZE
    
    # API settings
    api_timeout: float = DEFAULT_API_TIMEOUT
    secret_key: Optional[str] = None
    api_key: Optional[str] = None
    
    # Performance settings
    max_workers: int = DEFAULT_MAX_WORKERS
    celery_concurrency: int = DEFAULT_CELERY_CONCURRENCY
    
    # External API keys
    openai_api_key: Optional[str] = None
    openai_api_base: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization processing."""
        # Load from environment variables
        self.debug = os.getenv(ENV_DEBUG, "false").lower() in ("true", "1", "yes", "on")
        self.log_level = LogLevel(getattr(logging, os.getenv(ENV_LOG_LEVEL, "INFO").upper()))
        self.config_path = Path(os.getenv(ENV_CONFIG_PATH, DEFAULT_CONFIG_PATH))
        self.quantum_token = os.getenv(ENV_QUANTUM_TOKEN)
        self.database_url = os.getenv(ENV_DATABASE_URL)
        self.redis_url = os.getenv(ENV_REDIS_URL)
        self.secret_key = os.getenv(ENV_SECRET_KEY)
        self.api_key = os.getenv(ENV_API_KEY)
        self.openai_api_key = os.getenv(ENV_OPENAI_API_KEY)
        self.openai_api_base = os.getenv(ENV_OPENAI_API_BASE)
        
        # Validate configuration
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration settings."""
        if self.max_workers <= 0:
            raise ValueError("max_workers must be positive")
        if self.api_timeout <= 0:
            raise ValueError("api_timeout must be positive")
        if self.database_pool_size <= 0:
            raise ValueError("database_pool_size must be positive")
        if self.redis_pool_size <= 0:
            raise ValueError("redis_pool_size must be positive")


# Global configuration instance
config = Configuration()

# Global system information
system_info = SystemInfo()

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(config.log_level.value)

# Create console handler if no handlers exist
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.log_level.value)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_version() -> str:
    """Get the current version of BlueprintBot v2."""
    return __version__


def get_system_info() -> SystemInfo:
    """Get system information and capabilities."""
    return system_info


def get_config() -> Configuration:
    """Get the current configuration."""
    return config


def set_log_level(level: Union[str, int, LogLevel]) -> None:
    """Set the global log level."""
    if isinstance(level, str):
        level = LogLevel[level.upper()]
    elif isinstance(level, int):
        level = LogLevel(level)
    
    config.log_level = level
    logger.setLevel(level.value)
    
    for handler in logger.handlers:
        handler.setLevel(level.value)


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available."""
    dependencies = {
        "fastapi": False,
        "pydantic": False,
        "sqlalchemy": False,
        "redis": False,
        "celery": False,
        "numpy": False,
        "pandas": False,
        "scikit-learn": False,
        "tensorflow": False,
        "torch": False,
        "qiskit": False,
        "cirq": False,
        "pennylane": False,
        "opencv-python": False,
        "pillow": False,
        "matplotlib": False,
        "plotly": False,
        "httpx": False,
        "aiohttp": False,
        "websockets": False,
        "pytest": False,
        "docker": False,
        "kubernetes": False,
    }
    
    for package in dependencies:
        try:
            importlib.metadata.version(package)
            dependencies[package] = True
        except importlib.metadata.PackageNotFoundError:
            dependencies[package] = False
    
    return dependencies


def validate_environment() -> List[str]:
    """Validate the environment and return any issues found."""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 11):
        issues.append(f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check dependencies
    deps = check_dependencies()
    missing_deps = [dep for dep, available in deps.items() if not available]
    if missing_deps:
        issues.append(f"Missing dependencies: {', '.join(missing_deps)}")
    
    # Check configuration
    try:
        config._validate()
    except ValueError as e:
        issues.append(f"Configuration error: {e}")
    
    # Check file permissions
    if config.config_path and config.config_path.exists():
        if not os.access(config.config_path, os.R_OK):
            issues.append(f"Cannot read config file: {config.config_path}")
    
    return issues


@contextmanager
def temporary_config(**kwargs):
    """Temporarily modify configuration settings."""
    original_values = {}
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            original_values[key] = getattr(config, key)
            setattr(config, key, value)
    
    try:
        yield config
    finally:
        for key, value in original_values.items():
            setattr(config, key, value)


@asynccontextmanager
async def async_temporary_config(**kwargs):
    """Asynchronously temporarily modify configuration settings."""
    original_values = {}
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            original_values[key] = getattr(config, key)
            setattr(config, key, value)
    
    try:
        yield config
    finally:
        for key, value in original_values.items():
            setattr(config, key, value)


def setup_logging(level: Optional[Union[str, int, LogLevel]] = None, 
                 config_dict: Optional[Dict[str, Any]] = None) -> None:
    """Set up logging configuration."""
    if config_dict:
        logging.config.dictConfig(config_dict)
    else:
        # Use default configuration
        logging.config.dictConfig(MONITORING_CONFIGS["logging"])
    
    if level is not None:
        set_log_level(level)


def initialize_system() -> None:
    """Initialize the BlueprintBot v2 system."""
    logger.info(f"Initializing BlueprintBot v2 {__version__}")
    
    # Validate environment
    issues = validate_environment()
    if issues:
        for issue in issues:
            logger.warning(f"Environment issue: {issue}")
    
    # Set up logging
    setup_logging()
    
    # Log system information
    logger.info(f"System info: {system_info}")
    logger.info(f"Configuration: debug={config.debug}, log_level={config.log_level.name}")
    
    # Check dependencies
    deps = check_dependencies()
    available_deps = [dep for dep, available in deps.items() if available]
    missing_deps = [dep for dep, available in deps.items() if not available]
    
    logger.info(f"Available dependencies: {', '.join(available_deps)}")
    if missing_deps:
        logger.warning(f"Missing dependencies: {', '.join(missing_deps)}")
    
    logger.info("BlueprintBot v2 initialization complete")


# Initialize system on import
try:
    initialize_system()
except Exception as e:
    logger.error(f"Failed to initialize system: {e}")
    if config.debug:
        raise


# Export public API
__all__ = [
    # Version and metadata
    "__version__", "__author__", "__email__", "__license__", "__copyright__",
    "__title__", "__description__", "__url__", "__download_url__", "__docs_url__", "__tracker_url__",
    
    # Constants
    "DEFAULT_CONFIG_PATH", "DEFAULT_LOG_LEVEL", "DEFAULT_MAX_WORKERS", "DEFAULT_QUANTUM_BACKEND",
    "DEFAULT_AI_MODEL_CACHE_SIZE", "DEFAULT_API_TIMEOUT", "DEFAULT_DATABASE_POOL_SIZE",
    "DEFAULT_REDIS_POOL_SIZE", "DEFAULT_CELERY_CONCURRENCY",
    
    # Environment variables
    "ENV_CONFIG_PATH", "ENV_LOG_LEVEL", "ENV_DEBUG", "ENV_QUANTUM_TOKEN", "ENV_DATABASE_URL",
    "ENV_REDIS_URL", "ENV_SECRET_KEY", "ENV_API_KEY", "ENV_OPENAI_API_KEY", "ENV_OPENAI_API_BASE",
    
    # Configurations
    "SUPPORTED_PLAN_FORMATS", "AI_MODEL_CONFIGS", "QUANTUM_CONFIGS", "DATABASE_CONFIGS",
    "API_CONFIGS", "SECURITY_CONFIGS", "MONITORING_CONFIGS", "CLOUD_CONFIGS", "PERFORMANCE_CONFIGS",
    
    # Enums
    "LogLevel", "QuantumBackend", "AIModelType", "DatabaseType", "CloudProvider",
    
    # Data classes
    "SystemInfo", "Configuration",
    
    # Global instances
    "config", "system_info", "logger",
    
    # Functions
    "get_version", "get_system_info", "get_config", "set_log_level", "check_dependencies",
    "validate_environment", "temporary_config", "async_temporary_config", "setup_logging",
    "initialize_system",
]


# Suppress warnings for better user experience
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Set up signal handlers for graceful shutdown
import signal
import atexit


def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown."""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    # Perform cleanup operations here
    sys.exit(0)


def cleanup():
    """Cleanup function called on exit."""
    logger.info("BlueprintBot v2 shutdown complete")


# Register signal handlers and cleanup function
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup)

logger.info(f"BlueprintBot v2 {__version__} package loaded successfully")

