"""
BlueprintBot v2 API Package.

This package contains all API-related modules for the BlueprintBot v2 application,
including REST API endpoints, GraphQL schemas, WebSocket handlers, and API utilities.
"""

from .blueprint_analyzer import BlueprintAnalyzer
from .construction_optimizer import ConstructionOptimizer
from .material_calculator import MaterialCalculator
from .compliance_checker import ComplianceChecker
from .cost_estimator import CostEstimator
from .schedule_optimizer import ScheduleOptimizer
from .quality_controller import QualityController
from .safety_monitor import SafetyMonitor
from .environmental_analyzer import EnvironmentalAnalyzer
from .sustainability_assessor import SustainabilityAssessor
from .api_server import APIServer
from .websocket_handler import WebSocketHandler
from .graphql_schema import GraphQLSchema
from .middleware import AuthenticationMiddleware, RateLimitMiddleware, LoggingMiddleware
from .validators import RequestValidator, ResponseValidator
from .serializers import BlueprintSerializer, ProjectSerializer, ReportSerializer
from .exceptions import APIException, ValidationException, AuthenticationException

__version__ = "2.0.0"
__author__ = "BlueprintBot Development Team"
__email__ = "dev@blueprintbot.ai"
__license__ = "MIT"

__all__ = [
    "BlueprintAnalyzer",
    "ConstructionOptimizer", 
    "MaterialCalculator",
    "ComplianceChecker",
    "CostEstimator",
    "ScheduleOptimizer",
    "QualityController",
    "SafetyMonitor",
    "EnvironmentalAnalyzer",
    "SustainabilityAssessor",
    "APIServer",
    "WebSocketHandler",
    "GraphQLSchema",
    "AuthenticationMiddleware",
    "RateLimitMiddleware",
    "LoggingMiddleware",
    "RequestValidator",
    "ResponseValidator",
    "BlueprintSerializer",
    "ProjectSerializer",
    "ReportSerializer",
    "APIException",
    "ValidationException",
    "AuthenticationException"
]

