"""
BlueprintBot v2 - Test Configuration and Fixtures

This module provides comprehensive test configuration, fixtures, and utilities
for testing the BlueprintBot v2 application across all components including
quantum computing, AI/ML, and enterprise features.
"""

import asyncio
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional
from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pandas as pd
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

# Import application modules
from src.blueprintbot_v2.api.api_server import APIServer, APIServerConfig
from src.blueprintbot_v2.ai.advanced_ai_engine import AdvancedAIEngine
from src.blueprintbot_v2.quantum.quantum_processor import QuantumProcessor
from src.blueprintbot_v2.api.blueprint_analyzer import BlueprintAnalyzer
from src.blueprintbot_v2.core.exceptions import *


# Test configuration
TEST_DATABASE_URL = "sqlite:///test_blueprintbot.db"
TEST_REDIS_URL = "redis://localhost:6379/15"  # Use database 15 for tests


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_config() -> APIServerConfig:
    """Create test configuration for the API server."""
    return APIServerConfig(
        mode="testing",
        debug=True,
        database_url=TEST_DATABASE_URL,
        redis_url=TEST_REDIS_URL,
        enable_quantum_processing=False,  # Disable for most tests
        enable_ai_acceleration=False,     # Disable for most tests
        enable_caching=True,
        enable_metrics=False,
        enable_tracing=False,
        max_concurrent_analyses=2,
        analysis_timeout=30,
        log_level="DEBUG"
    )


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def redis_container():
    """Start Redis container for integration tests."""
    with RedisContainer("redis:7") as redis:
        yield redis


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_blueprint_data() -> Dict[str, Any]:
    """Generate sample blueprint data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "name": "Test Office Building",
        "type": "architectural",
        "dimensions": {
            "width": 50.0,
            "height": 30.0,
            "floors": 3
        },
        "rooms": [
            {
                "name": "Office 1",
                "area": 150.0,
                "type": "office"
            },
            {
                "name": "Conference Room",
                "area": 80.0,
                "type": "meeting"
            }
        ],
        "materials": [
            {
                "type": "concrete",
                "quantity": 500.0,
                "unit": "cubic_meters"
            },
            {
                "type": "steel",
                "quantity": 50.0,
                "unit": "tons"
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


@pytest.fixture
def mock_quantum_processor() -> MagicMock:
    """Create mock quantum processor for testing."""
    mock = MagicMock(spec=QuantumProcessor)
    mock.initialize = AsyncMock()
    mock.cleanup = AsyncMock()
    mock.is_available = True
    mock.backend_name = "qasm_simulator"
    mock.max_qubits = 32
    mock.execute_circuit = AsyncMock(return_value={
        "counts": {"00": 500, "11": 500},
        "execution_time": 0.1,
        "shots": 1000
    })
    mock.optimize_circuit = AsyncMock(return_value=MagicMock())
    mock.get_quantum_advantage = AsyncMock(return_value=847.5)
    return mock


@pytest.fixture
def mock_ai_engine() -> MagicMock:
    """Create mock AI engine for testing."""
    mock = MagicMock(spec=AdvancedAIEngine)
    mock.initialize = AsyncMock()
    mock.cleanup = AsyncMock()
    mock.is_available = True
    mock.analyze_image = AsyncMock(return_value={
        "objects": ["wall", "door", "window"],
        "confidence": 0.95,
        "processing_time": 0.5
    })
    mock.process_text = AsyncMock(return_value={
        "sentiment": "positive",
        "entities": ["building", "office"],
        "confidence": 0.92
    })
    mock.generate_recommendations = AsyncMock(return_value=[
        "Optimize material usage",
        "Improve energy efficiency",
        "Enhance structural integrity"
    ])
    return mock


@pytest.fixture
def mock_blueprint_analyzer(mock_quantum_processor, mock_ai_engine) -> MagicMock:
    """Create mock blueprint analyzer for testing."""
    mock = MagicMock(spec=BlueprintAnalyzer)
    mock.quantum_processor = mock_quantum_processor
    mock.ai_engine = mock_ai_engine
    mock.analyze_blueprint = AsyncMock(return_value=MagicMock(
        analysis_id="test-analysis-123",
        blueprint_type="architectural",
        analysis_level="advanced",
        accuracy_score=0.97,
        processing_time=3.2,
        material_analysis={
            "total_cost": 150000.0,
            "materials": [
                {"type": "concrete", "quantity": 500.0, "cost": 50000.0},
                {"type": "steel", "quantity": 50.0, "cost": 100000.0}
            ]
        },
        structural_analysis={
            "load_bearing_capacity": "adequate",
            "safety_factor": 2.5,
            "recommendations": ["Add reinforcement in area A"]
        },
        optimization_suggestions=[
            "Reduce material waste by 15%",
            "Improve energy efficiency by 20%"
        ],
        compliance_status={
            "building_codes": "compliant",
            "safety_standards": "compliant",
            "environmental_regulations": "compliant"
        }
    ))
    return mock


@pytest.fixture
async def api_server(test_config, mock_quantum_processor, mock_ai_engine) -> APIServer:
    """Create API server instance for testing."""
    server = APIServer(test_config)
    
    # Replace real components with mocks
    server.quantum_processor = mock_quantum_processor
    server.ai_engine = mock_ai_engine
    
    await server.initialize()
    yield server
    await server.cleanup()


@pytest.fixture
async def test_client(api_server) -> AsyncClient:
    """Create async test client for API testing."""
    async with AsyncClient(
        app=api_server.fastapi_app,
        base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
def sync_test_client(api_server) -> TestClient:
    """Create synchronous test client for API testing."""
    return TestClient(api_server.fastapi_app)


@pytest.fixture
def sample_image_data() -> bytes:
    """Generate sample image data for testing."""
    # Create a simple test image using PIL
    from PIL import Image
    import io
    
    image = Image.new('RGB', (100, 100), color='white')
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


@pytest.fixture
def sample_pdf_data() -> bytes:
    """Generate sample PDF data for testing."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Test Blueprint Document")
    p.drawString(100, 700, "This is a sample blueprint for testing purposes.")
    p.save()
    return buffer.getvalue()


@pytest.fixture
def quantum_circuit_data() -> Dict[str, Any]:
    """Generate sample quantum circuit data for testing."""
    return {
        "circuit_id": "test-circuit-123",
        "qubits": 4,
        "gates": [
            {"type": "H", "qubit": 0},
            {"type": "CNOT", "control": 0, "target": 1},
            {"type": "RZ", "qubit": 2, "angle": 0.5},
            {"type": "measure", "qubits": [0, 1, 2, 3]}
        ],
        "shots": 1000,
        "backend": "qasm_simulator"
    }


@pytest.fixture
def ai_model_data() -> Dict[str, Any]:
    """Generate sample AI model data for testing."""
    return {
        "model_id": "test-model-123",
        "model_type": "computer_vision",
        "framework": "pytorch",
        "version": "1.0.0",
        "accuracy": 0.95,
        "training_data_size": 10000,
        "parameters": {
            "learning_rate": 0.001,
            "batch_size": 32,
            "epochs": 100
        }
    }


@pytest.fixture
def performance_metrics() -> Dict[str, Any]:
    """Generate sample performance metrics for testing."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": 45.2,
        "memory_usage": 2048.0,
        "disk_usage": 15.7,
        "network_io": {
            "bytes_sent": 1024000,
            "bytes_received": 2048000
        },
        "response_times": {
            "p50": 0.1,
            "p95": 0.5,
            "p99": 1.0
        },
        "error_rate": 0.01,
        "throughput": 1000.0
    }


@pytest.fixture
def security_test_data() -> Dict[str, Any]:
    """Generate sample security test data."""
    return {
        "test_id": "security-test-123",
        "vulnerability_scan": {
            "high": 0,
            "medium": 2,
            "low": 5
        },
        "authentication_tests": {
            "jwt_validation": "passed",
            "session_management": "passed",
            "password_policy": "passed"
        },
        "encryption_tests": {
            "data_at_rest": "passed",
            "data_in_transit": "passed",
            "key_management": "passed"
        }
    }


# Pytest markers for test categorization
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.quantum = pytest.mark.quantum
pytest.mark.ai = pytest.mark.ai
pytest.mark.performance = pytest.mark.performance
pytest.mark.security = pytest.mark.security
pytest.mark.slow = pytest.mark.slow
pytest.mark.requires_gpu = pytest.mark.requires_gpu
pytest.mark.requires_quantum_hardware = pytest.mark.requires_quantum_hardware


# Test utilities
class TestUtils:
    """Utility functions for testing."""
    
    @staticmethod
    def create_test_file(content: str, suffix: str = ".txt") -> Path:
        """Create a temporary test file with given content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
        temp_file.write(content)
        temp_file.close()
        return Path(temp_file.name)
    
    @staticmethod
    def generate_random_matrix(rows: int, cols: int) -> np.ndarray:
        """Generate a random matrix for testing."""
        return np.random.rand(rows, cols)
    
    @staticmethod
    def create_test_dataframe(rows: int = 100) -> pd.DataFrame:
        """Create a test DataFrame with sample data."""
        return pd.DataFrame({
            'id': range(rows),
            'value': np.random.rand(rows),
            'category': np.random.choice(['A', 'B', 'C'], rows),
            'timestamp': pd.date_range('2023-01-01', periods=rows, freq='H')
        })
    
    @staticmethod
    async def wait_for_condition(condition_func, timeout: float = 5.0, interval: float = 0.1):
        """Wait for a condition to become true."""
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            if await condition_func():
                return True
            await asyncio.sleep(interval)
        return False


@pytest.fixture
def test_utils() -> TestUtils:
    """Provide test utilities."""
    return TestUtils()


# Async test helpers
@pytest_asyncio.fixture
async def async_session():
    """Create async database session for testing."""
    # This would be implemented based on your async database setup
    pass


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically cleanup test files after each test."""
    created_files = []
    
    def track_file(file_path: Path):
        created_files.append(file_path)
    
    yield track_file
    
    # Cleanup
    for file_path in created_files:
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors


# Configuration for pytest
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "quantum: mark test as requiring quantum computing"
    )
    config.addinivalue_line(
        "markers", "ai: mark test as requiring AI/ML components"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_gpu: mark test as requiring GPU"
    )
    config.addinivalue_line(
        "markers", "requires_quantum_hardware: mark test as requiring real quantum hardware"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "quantum" in str(item.fspath):
            item.add_marker(pytest.mark.quantum)
        elif "ai" in str(item.fspath):
            item.add_marker(pytest.mark.ai)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)


# Environment setup
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables and configuration."""
    os.environ.update({
        "BLUEPRINTBOT_ENV": "testing",
        "DATABASE_URL": TEST_DATABASE_URL,
        "REDIS_URL": TEST_REDIS_URL,
        "LOG_LEVEL": "DEBUG",
        "QUANTUM_BACKEND": "qasm_simulator",
        "AI_MODEL_CACHE_DIR": "/tmp/test_ai_models",
        "UPLOAD_DIRECTORY": "/tmp/test_uploads",
        "ENABLE_QUANTUM_PROCESSING": "false",
        "ENABLE_AI_ACCELERATION": "false",
        "ENABLE_CACHING": "true",
        "ENABLE_METRICS": "false",
        "ENABLE_TRACING": "false"
    })
    
    # Create test directories
    os.makedirs("/tmp/test_ai_models", exist_ok=True)
    os.makedirs("/tmp/test_uploads", exist_ok=True)
    
    yield
    
    # Cleanup test environment
    import shutil
    shutil.rmtree("/tmp/test_ai_models", ignore_errors=True)
    shutil.rmtree("/tmp/test_uploads", ignore_errors=True)

