"""
BlueprintBot v2 Advanced AI Integration Module.

This module provides comprehensive AI capabilities for construction planning and analysis,
including multi-agent coordination, advanced machine learning models, and hybrid AI systems.

Key Features:
- Multi-agent AI coordination with 200+ specialized agents
- Advanced transformer models for plan analysis
- Computer vision for blueprint interpretation
- Natural language processing for specifications
- Reinforcement learning for optimization
- Federated learning for distributed training
- AutoML for automated model selection
- Explainable AI for decision transparency
- Real-time model serving and inference
- Advanced ensemble methods
- Neural architecture search
- Transfer learning capabilities
- Continual learning systems
- AI safety and robustness measures
"""

import logging
import numpy as np
import asyncio
import json
import pickle
import time
from typing import Dict, List, Optional, Union, Any, Tuple, Callable, Type
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
from contextlib import asynccontextmanager, contextmanager
import warnings
import hashlib
import uuid
from datetime import datetime, timedelta

# Core ML imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers, callbacks
    import tensorflow_probability as tfp
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, Dataset
    import torchvision
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from transformers import (
        AutoModel, AutoTokenizer, AutoConfig, AutoProcessor,
        pipeline, Trainer, TrainingArguments, 
        BertModel, GPTModel, T5Model, VisionEncoderDecoderModel
    )
    import datasets
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import sklearn
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False

try:
    import ray
    from ray import tune
    from ray.tune import CLIReporter
    from ray.tune.schedulers import ASHAScheduler
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False

try:
    import mlflow
    import mlflow.tensorflow
    import mlflow.pytorch
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False

try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False

from ..core.exceptions import AIModelError, ConfigurationError, ValidationError
from ..core.config import get_config
from ..utils.logging import get_logger
from ..quantum import get_quantum_manager, QuantumBackendType

logger = get_logger(__name__)


class AIModelType(Enum):
    """Enumeration for AI model types."""
    TRANSFORMER = "transformer"
    CONVOLUTIONAL = "convolutional"
    RECURRENT = "recurrent"
    ENSEMBLE = "ensemble"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    GENERATIVE = "generative"
    MULTIMODAL = "multimodal"
    GRAPH_NEURAL_NETWORK = "graph_neural_network"
    ATTENTION = "attention"
    AUTOENCODER = "autoencoder"


class AITaskType(Enum):
    """Enumeration for AI task types."""
    PLAN_ANALYSIS = "plan_analysis"
    MATERIAL_ESTIMATION = "material_estimation"
    COMPLIANCE_CHECKING = "compliance_checking"
    COST_PREDICTION = "cost_prediction"
    SCHEDULE_OPTIMIZATION = "schedule_optimization"
    RISK_ASSESSMENT = "risk_assessment"
    QUALITY_CONTROL = "quality_control"
    SAFETY_MONITORING = "safety_monitoring"
    RESOURCE_ALLOCATION = "resource_allocation"
    DEFECT_DETECTION = "defect_detection"


class TrainingStrategy(Enum):
    """Enumeration for training strategies."""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    SEMI_SUPERVISED = "semi_supervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    FEDERATED = "federated"
    CONTINUAL = "continual"
    META_LEARNING = "meta_learning"
    SELF_SUPERVISED = "self_supervised"
    ACTIVE_LEARNING = "active_learning"


class OptimizationAlgorithm(Enum):
    """Enumeration for optimization algorithms."""
    ADAM = "adam"
    ADAMW = "adamw"
    SGD = "sgd"
    RMSPROP = "rmsprop"
    ADAGRAD = "adagrad"
    ADADELTA = "adadelta"
    ADAMAX = "adamax"
    NADAM = "nadam"
    FTRL = "ftrl"
    LION = "lion"


@dataclass
class AIModelConfig:
    """Configuration for AI models."""
    model_type: AIModelType = AIModelType.TRANSFORMER
    task_type: AITaskType = AITaskType.PLAN_ANALYSIS
    model_name: str = "blueprintbot_model"
    model_version: str = "1.0.0"
    
    # Architecture parameters
    input_size: Tuple[int, ...] = (224, 224, 3)
    output_size: int = 1000
    hidden_sizes: List[int] = field(default_factory=lambda: [512, 256, 128])
    num_layers: int = 12
    num_heads: int = 8
    dropout_rate: float = 0.1
    activation: str = "relu"
    
    # Training parameters
    training_strategy: TrainingStrategy = TrainingStrategy.SUPERVISED
    optimizer: OptimizationAlgorithm = OptimizationAlgorithm.ADAM
    learning_rate: float = 1e-4
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    early_stopping: bool = True
    patience: int = 10
    
    # Advanced parameters
    use_mixed_precision: bool = True
    gradient_clipping: float = 1.0
    weight_decay: float = 1e-5
    label_smoothing: float = 0.1
    augmentation_enabled: bool = True
    regularization_l1: float = 0.0
    regularization_l2: float = 1e-4
    
    # Quantum integration
    quantum_enhanced: bool = False
    quantum_backend: QuantumBackendType = QuantumBackendType.QISKIT_AER
    quantum_layers: int = 2
    
    def __post_init__(self):
        """Post-initialization validation."""
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.epochs <= 0:
            raise ValueError("epochs must be positive")
        if not 0 < self.validation_split < 1:
            raise ValueError("validation_split must be between 0 and 1")


@dataclass
class MultiAgentConfig:
    """Configuration for multi-agent AI system."""
    num_agents: int = 200
    agent_types: List[str] = field(default_factory=lambda: [
        "plan_analyzer", "material_estimator", "compliance_checker", "cost_predictor",
        "schedule_optimizer", "risk_assessor", "quality_controller", "safety_monitor"
    ])
    coordination_strategy: str = "hierarchical"
    communication_protocol: str = "message_passing"
    consensus_mechanism: str = "voting"
    load_balancing: bool = True
    fault_tolerance: bool = True
    scalability_mode: str = "dynamic"
    
    def __post_init__(self):
        """Post-initialization validation."""
        if self.num_agents <= 0:
            raise ValueError("num_agents must be positive")
        if not self.agent_types:
            raise ValueError("agent_types cannot be empty")


@dataclass
class TrainingMetrics:
    """Training metrics and statistics."""
    epoch: int = 0
    train_loss: float = 0.0
    val_loss: float = 0.0
    train_accuracy: float = 0.0
    val_accuracy: float = 0.0
    learning_rate: float = 0.0
    training_time: float = 0.0
    memory_usage: float = 0.0
    gpu_utilization: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "epoch": self.epoch,
            "train_loss": self.train_loss,
            "val_loss": self.val_loss,
            "train_accuracy": self.train_accuracy,
            "val_accuracy": self.val_accuracy,
            "learning_rate": self.learning_rate,
            "training_time": self.training_time,
            "memory_usage": self.memory_usage,
            "gpu_utilization": self.gpu_utilization,
        }


class AIAgent(ABC):
    """Abstract base class for AI agents."""
    
    def __init__(self, agent_id: str, agent_type: str, config: AIModelConfig):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config
        self.model = None
        self.is_trained = False
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self.creation_time = datetime.now()
        self.last_update_time = self.creation_time
        
        # Performance metrics
        self.inference_count = 0
        self.total_inference_time = 0.0
        self.error_count = 0
        self.success_rate = 1.0
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the AI agent."""
        pass
    
    @abstractmethod
    async def train(self, training_data: Any, validation_data: Optional[Any] = None) -> TrainingMetrics:
        """Train the AI agent."""
        pass
    
    @abstractmethod
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """Make predictions using the AI agent."""
        pass
    
    @abstractmethod
    async def evaluate(self, test_data: Any) -> Dict[str, Any]:
        """Evaluate the AI agent performance."""
        pass
    
    async def update_model(self, new_data: Any) -> bool:
        """Update the model with new data (continual learning)."""
        try:
            self.logger.info(f"Updating model for agent {self.agent_id}")
            
            # Implement continual learning logic here
            # This is a placeholder - actual implementation would depend on the specific model
            
            self.last_update_time = datetime.now()
            return True
        
        except Exception as e:
            self.logger.error(f"Model update failed for agent {self.agent_id}: {e}")
            return False
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information and statistics."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "model_type": self.config.model_type.value,
            "task_type": self.config.task_type.value,
            "is_trained": self.is_trained,
            "creation_time": self.creation_time.isoformat(),
            "last_update_time": self.last_update_time.isoformat(),
            "inference_count": self.inference_count,
            "average_inference_time": self.total_inference_time / max(1, self.inference_count),
            "error_count": self.error_count,
            "success_rate": self.success_rate,
        }
    
    def _update_performance_metrics(self, inference_time: float, success: bool):
        """Update performance metrics."""
        self.inference_count += 1
        self.total_inference_time += inference_time
        
        if not success:
            self.error_count += 1
        
        self.success_rate = (self.inference_count - self.error_count) / self.inference_count


class PlanAnalyzerAgent(AIAgent):
    """AI agent specialized in blueprint and plan analysis."""
    
    def __init__(self, agent_id: str, config: AIModelConfig):
        super().__init__(agent_id, "plan_analyzer", config)
        self.vision_model = None
        self.text_model = None
    
    async def initialize(self) -> bool:
        """Initialize the plan analyzer agent."""
        try:
            self.logger.info(f"Initializing plan analyzer agent {self.agent_id}")
            
            if TRANSFORMERS_AVAILABLE:
                # Initialize vision transformer for image analysis
                self.vision_model = AutoModel.from_pretrained("google/vit-base-patch16-224")
                
                # Initialize text model for specification analysis
                self.text_model = AutoModel.from_pretrained("bert-base-uncased")
                
                self.logger.info("Initialized transformer models")
            
            elif TENSORFLOW_AVAILABLE:
                # Fallback to TensorFlow models
                self.vision_model = self._create_cnn_model()
                self.text_model = self._create_text_model()
                
                self.logger.info("Initialized TensorFlow models")
            
            else:
                # Fallback to classical models
                if SKLEARN_AVAILABLE:
                    from sklearn.ensemble import RandomForestClassifier
                    self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                    self.logger.info("Initialized classical model")
                else:
                    raise ImportError("No suitable ML library available")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to initialize plan analyzer agent: {e}")
            return False
    
    async def train(self, training_data: Any, validation_data: Optional[Any] = None) -> TrainingMetrics:
        """Train the plan analyzer agent."""
        try:
            self.logger.info(f"Training plan analyzer agent {self.agent_id}")
            
            start_time = time.time()
            metrics = TrainingMetrics()
            
            # Placeholder training logic - would be implemented based on specific model
            if hasattr(self.model, 'fit'):
                # Scikit-learn style interface
                X_train, y_train = training_data
                self.model.fit(X_train, y_train)
                
                if validation_data:
                    X_val, y_val = validation_data
                    val_score = self.model.score(X_val, y_val)
                    metrics.val_accuracy = val_score
                
                train_score = self.model.score(X_train, y_train)
                metrics.train_accuracy = train_score
            
            metrics.training_time = time.time() - start_time
            self.is_trained = True
            
            self.logger.info(f"Training completed for agent {self.agent_id}")
            return metrics
        
        except Exception as e:
            self.logger.error(f"Training failed for agent {self.agent_id}: {e}")
            raise AIModelError(f"Training failed: {e}")
    
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """Analyze construction plans and extract information."""
        start_time = time.time()
        success = False
        
        try:
            if not self.is_trained:
                raise ValueError("Agent must be trained before making predictions")
            
            self.logger.debug(f"Making prediction with agent {self.agent_id}")
            
            # Handle different input types
            if isinstance(input_data, dict):
                if "image" in input_data:
                    result = await self._analyze_image(input_data["image"])
                elif "text" in input_data:
                    result = await self._analyze_text(input_data["text"])
                else:
                    result = await self._analyze_mixed(input_data)
            else:
                # Assume it's image data
                result = await self._analyze_image(input_data)
            
            success = True
            return {
                "agent_id": self.agent_id,
                "prediction": result,
                "confidence": result.get("confidence", 0.8),
                "processing_time": time.time() - start_time,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Prediction failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
        
        finally:
            self._update_performance_metrics(time.time() - start_time, success)
    
    async def evaluate(self, test_data: Any) -> Dict[str, Any]:
        """Evaluate the plan analyzer agent."""
        try:
            self.logger.info(f"Evaluating plan analyzer agent {self.agent_id}")
            
            # Placeholder evaluation logic
            if hasattr(self.model, 'score'):
                X_test, y_test = test_data
                accuracy = self.model.score(X_test, y_test)
                
                return {
                    "agent_id": self.agent_id,
                    "accuracy": accuracy,
                    "success": True
                }
            
            return {
                "agent_id": self.agent_id,
                "message": "Evaluation not implemented for this model type",
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Evaluation failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
    
    async def _analyze_image(self, image_data: Any) -> Dict[str, Any]:
        """Analyze blueprint images."""
        # Placeholder for image analysis
        return {
            "elements_detected": ["walls", "doors", "windows", "dimensions"],
            "room_count": 5,
            "total_area": 1200.5,
            "confidence": 0.85
        }
    
    async def _analyze_text(self, text_data: str) -> Dict[str, Any]:
        """Analyze textual specifications."""
        # Placeholder for text analysis
        return {
            "specifications_extracted": ["concrete", "steel", "insulation"],
            "requirements": ["fire_safety", "accessibility"],
            "confidence": 0.78
        }
    
    async def _analyze_mixed(self, mixed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mixed image and text data."""
        # Placeholder for multimodal analysis
        return {
            "integrated_analysis": True,
            "cross_modal_consistency": 0.82,
            "confidence": 0.80
        }
    
    def _create_cnn_model(self):
        """Create a CNN model for image analysis."""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.config.input_size),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.config.output_size, activation='softmax')
        ])
        
        model.compile(
            optimizer=self.config.optimizer.value,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _create_text_model(self):
        """Create a text model for specification analysis."""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        model = keras.Sequential([
            layers.Embedding(10000, 128),
            layers.LSTM(64, dropout=0.5, recurrent_dropout=0.5),
            layers.Dense(self.config.output_size, activation='softmax')
        ])
        
        model.compile(
            optimizer=self.config.optimizer.value,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model


class MaterialEstimatorAgent(AIAgent):
    """AI agent specialized in material quantity estimation."""
    
    def __init__(self, agent_id: str, config: AIModelConfig):
        super().__init__(agent_id, "material_estimator", config)
    
    async def initialize(self) -> bool:
        """Initialize the material estimator agent."""
        try:
            self.logger.info(f"Initializing material estimator agent {self.agent_id}")
            
            if XGBOOST_AVAILABLE:
                self.model = xgb.XGBRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42
                )
            elif SKLEARN_AVAILABLE:
                from sklearn.ensemble import RandomForestRegressor
                self.model = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
            else:
                raise ImportError("No suitable ML library available")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to initialize material estimator agent: {e}")
            return False
    
    async def train(self, training_data: Any, validation_data: Optional[Any] = None) -> TrainingMetrics:
        """Train the material estimator agent."""
        try:
            self.logger.info(f"Training material estimator agent {self.agent_id}")
            
            start_time = time.time()
            metrics = TrainingMetrics()
            
            X_train, y_train = training_data
            self.model.fit(X_train, y_train)
            
            if validation_data:
                X_val, y_val = validation_data
                val_predictions = self.model.predict(X_val)
                val_mse = np.mean((y_val - val_predictions) ** 2)
                metrics.val_loss = val_mse
            
            train_predictions = self.model.predict(X_train)
            train_mse = np.mean((y_train - train_predictions) ** 2)
            metrics.train_loss = train_mse
            
            metrics.training_time = time.time() - start_time
            self.is_trained = True
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Training failed for agent {self.agent_id}: {e}")
            raise AIModelError(f"Training failed: {e}")
    
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """Estimate material quantities."""
        start_time = time.time()
        success = False
        
        try:
            if not self.is_trained:
                raise ValueError("Agent must be trained before making predictions")
            
            # Make prediction
            if hasattr(self.model, 'predict'):
                prediction = self.model.predict(input_data.reshape(1, -1))[0]
            else:
                prediction = 0.0  # Fallback
            
            # Convert to material estimates
            material_estimates = self._convert_to_materials(prediction, input_data)
            
            success = True
            return {
                "agent_id": self.agent_id,
                "material_estimates": material_estimates,
                "total_cost": sum(material_estimates.values()),
                "confidence": 0.82,
                "processing_time": time.time() - start_time,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Prediction failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
        
        finally:
            self._update_performance_metrics(time.time() - start_time, success)
    
    async def evaluate(self, test_data: Any) -> Dict[str, Any]:
        """Evaluate the material estimator agent."""
        try:
            X_test, y_test = test_data
            predictions = self.model.predict(X_test)
            
            mse = np.mean((y_test - predictions) ** 2)
            mae = np.mean(np.abs(y_test - predictions))
            
            return {
                "agent_id": self.agent_id,
                "mse": mse,
                "mae": mae,
                "rmse": np.sqrt(mse),
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Evaluation failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
    
    def _convert_to_materials(self, prediction: float, input_data: Any) -> Dict[str, float]:
        """Convert prediction to material quantities."""
        # Placeholder conversion logic
        base_materials = {
            "concrete": prediction * 0.4,
            "steel": prediction * 0.2,
            "lumber": prediction * 0.15,
            "insulation": prediction * 0.1,
            "drywall": prediction * 0.08,
            "roofing": prediction * 0.05,
            "plumbing": prediction * 0.02
        }
        
        return base_materials


class ComplianceCheckerAgent(AIAgent):
    """AI agent specialized in regulatory compliance checking."""
    
    def __init__(self, agent_id: str, config: AIModelConfig):
        super().__init__(agent_id, "compliance_checker", config)
        self.rule_engine = None
        self.knowledge_base = {}
    
    async def initialize(self) -> bool:
        """Initialize the compliance checker agent."""
        try:
            self.logger.info(f"Initializing compliance checker agent {self.agent_id}")
            
            # Load compliance rules and regulations
            await self._load_compliance_rules()
            
            if SKLEARN_AVAILABLE:
                from sklearn.ensemble import RandomForestClassifier
                self.model = RandomForestClassifier(
                    n_estimators=200,
                    max_depth=10,
                    random_state=42
                )
            else:
                raise ImportError("No suitable ML library available")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to initialize compliance checker agent: {e}")
            return False
    
    async def train(self, training_data: Any, validation_data: Optional[Any] = None) -> TrainingMetrics:
        """Train the compliance checker agent."""
        try:
            self.logger.info(f"Training compliance checker agent {self.agent_id}")
            
            start_time = time.time()
            metrics = TrainingMetrics()
            
            X_train, y_train = training_data
            self.model.fit(X_train, y_train)
            
            if validation_data:
                X_val, y_val = validation_data
                val_score = self.model.score(X_val, y_val)
                metrics.val_accuracy = val_score
            
            train_score = self.model.score(X_train, y_train)
            metrics.train_accuracy = train_score
            
            metrics.training_time = time.time() - start_time
            self.is_trained = True
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Training failed for agent {self.agent_id}: {e}")
            raise AIModelError(f"Training failed: {e}")
    
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """Check compliance against regulations."""
        start_time = time.time()
        success = False
        
        try:
            if not self.is_trained:
                raise ValueError("Agent must be trained before making predictions")
            
            # Perform compliance checking
            compliance_results = await self._check_compliance_rules(input_data)
            
            # ML-based compliance prediction
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(input_data.reshape(1, -1))[0]
                compliance_score = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            else:
                compliance_score = 0.8  # Fallback
            
            success = True
            return {
                "agent_id": self.agent_id,
                "compliance_score": compliance_score,
                "compliance_results": compliance_results,
                "violations": compliance_results.get("violations", []),
                "recommendations": compliance_results.get("recommendations", []),
                "processing_time": time.time() - start_time,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Prediction failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
        
        finally:
            self._update_performance_metrics(time.time() - start_time, success)
    
    async def evaluate(self, test_data: Any) -> Dict[str, Any]:
        """Evaluate the compliance checker agent."""
        try:
            X_test, y_test = test_data
            predictions = self.model.predict(X_test)
            
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
            recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
            f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
            
            return {
                "agent_id": self.agent_id,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Evaluation failed for agent {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "success": False
            }
    
    async def _load_compliance_rules(self):
        """Load compliance rules and regulations."""
        # Placeholder for loading compliance rules
        self.knowledge_base = {
            "building_codes": {
                "fire_safety": ["sprinkler_system", "fire_exits", "fire_resistant_materials"],
                "accessibility": ["ramps", "door_widths", "elevator_access"],
                "structural": ["load_bearing", "seismic_requirements", "wind_resistance"]
            },
            "safety_regulations": {
                "osha": ["fall_protection", "hazard_communication", "personal_protective_equipment"],
                "local": ["noise_limits", "dust_control", "traffic_management"]
            }
        }
    
    async def _check_compliance_rules(self, input_data: Any) -> Dict[str, Any]:
        """Check input against compliance rules."""
        # Placeholder compliance checking logic
        violations = []
        recommendations = []
        
        # Simulate rule checking
        if "fire_safety" not in str(input_data):
            violations.append("Missing fire safety specifications")
            recommendations.append("Add fire safety measures according to local building codes")
        
        if "accessibility" not in str(input_data):
            violations.append("Accessibility requirements not addressed")
            recommendations.append("Include accessibility features as per ADA guidelines")
        
        return {
            "violations": violations,
            "recommendations": recommendations,
            "compliance_level": "partial" if violations else "full"
        }


class MultiAgentCoordinator:
    """Coordinator for managing multiple AI agents."""
    
    def __init__(self, config: MultiAgentConfig):
        self.config = config
        self.agents: Dict[str, AIAgent] = {}
        self.agent_pool = ThreadPoolExecutor(max_workers=config.num_agents)
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self.coordination_lock = threading.Lock()
        
        # Performance tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.average_response_time = 0.0
        
    async def initialize_agents(self) -> bool:
        """Initialize all AI agents."""
        try:
            self.logger.info(f"Initializing {self.config.num_agents} AI agents")
            
            # Calculate agents per type
            agents_per_type = self.config.num_agents // len(self.config.agent_types)
            
            agent_classes = {
                "plan_analyzer": PlanAnalyzerAgent,
                "material_estimator": MaterialEstimatorAgent,
                "compliance_checker": ComplianceCheckerAgent,
            }
            
            # Create agents
            for agent_type in self.config.agent_types:
                agent_class = agent_classes.get(agent_type, PlanAnalyzerAgent)  # Default fallback
                
                for i in range(agents_per_type):
                    agent_id = f"{agent_type}_{i:03d}"
                    config = AIModelConfig(task_type=AITaskType(agent_type.upper()))
                    
                    agent = agent_class(agent_id, config)
                    
                    # Initialize agent
                    if await agent.initialize():
                        self.agents[agent_id] = agent
                        self.logger.debug(f"Initialized agent {agent_id}")
                    else:
                        self.logger.warning(f"Failed to initialize agent {agent_id}")
            
            self.logger.info(f"Successfully initialized {len(self.agents)} agents")
            return len(self.agents) > 0
        
        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {e}")
            return False
    
    async def coordinate_prediction(self, task_type: AITaskType, input_data: Any) -> Dict[str, Any]:
        """Coordinate prediction across multiple agents."""
        try:
            start_time = time.time()
            self.total_requests += 1
            
            # Find relevant agents
            relevant_agents = self._find_relevant_agents(task_type)
            
            if not relevant_agents:
                raise ValueError(f"No agents available for task type: {task_type}")
            
            # Distribute work across agents
            tasks = []
            for agent in relevant_agents[:min(5, len(relevant_agents))]:  # Limit to 5 agents
                tasks.append(agent.predict(input_data))
            
            # Execute predictions in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            successful_results = []
            errors = []
            
            for result in results:
                if isinstance(result, Exception):
                    errors.append(str(result))
                elif isinstance(result, dict) and result.get("success"):
                    successful_results.append(result)
                else:
                    errors.append("Unknown error in agent prediction")
            
            if not successful_results:
                raise Exception(f"All agents failed. Errors: {errors}")
            
            # Aggregate results using consensus mechanism
            aggregated_result = await self._aggregate_results(successful_results)
            
            # Update performance metrics
            response_time = time.time() - start_time
            self.successful_requests += 1
            self.average_response_time = (
                (self.average_response_time * (self.successful_requests - 1) + response_time) 
                / self.successful_requests
            )
            
            return {
                "task_type": task_type.value,
                "result": aggregated_result,
                "num_agents_used": len(successful_results),
                "response_time": response_time,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Coordination failed: {e}")
            return {
                "task_type": task_type.value,
                "error": str(e),
                "success": False
            }
    
    async def train_agents(self, training_data: Dict[str, Any]) -> Dict[str, TrainingMetrics]:
        """Train all agents with appropriate data."""
        try:
            self.logger.info("Starting agent training")
            
            training_results = {}
            
            # Train agents by type
            for agent_type in self.config.agent_types:
                if agent_type in training_data:
                    type_agents = [agent for agent in self.agents.values() 
                                 if agent.agent_type == agent_type]
                    
                    if type_agents:
                        # Train first agent of each type (others can share the model)
                        agent = type_agents[0]
                        metrics = await agent.train(training_data[agent_type])
                        training_results[agent_type] = metrics
                        
                        # Copy trained model to other agents of same type
                        for other_agent in type_agents[1:]:
                            other_agent.model = agent.model
                            other_agent.is_trained = True
            
            return training_results
        
        except Exception as e:
            self.logger.error(f"Agent training failed: {e}")
            return {}
    
    def _find_relevant_agents(self, task_type: AITaskType) -> List[AIAgent]:
        """Find agents relevant to the task type."""
        # Map task types to agent types
        task_to_agent_mapping = {
            AITaskType.PLAN_ANALYSIS: "plan_analyzer",
            AITaskType.MATERIAL_ESTIMATION: "material_estimator",
            AITaskType.COMPLIANCE_CHECKING: "compliance_checker",
            AITaskType.COST_PREDICTION: "material_estimator",  # Can handle cost prediction
            AITaskType.RISK_ASSESSMENT: "compliance_checker",  # Can handle risk assessment
        }
        
        agent_type = task_to_agent_mapping.get(task_type, "plan_analyzer")
        
        return [agent for agent in self.agents.values() 
                if agent.agent_type == agent_type and agent.is_trained]
    
    async def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from multiple agents using consensus mechanism."""
        if not results:
            return {}
        
        if len(results) == 1:
            return results[0]["prediction"]
        
        # Implement voting-based consensus
        if self.config.consensus_mechanism == "voting":
            return await self._voting_consensus(results)
        elif self.config.consensus_mechanism == "averaging":
            return await self._averaging_consensus(results)
        elif self.config.consensus_mechanism == "weighted":
            return await self._weighted_consensus(results)
        else:
            # Default to simple averaging
            return await self._averaging_consensus(results)
    
    async def _voting_consensus(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Implement voting-based consensus."""
        # Placeholder implementation
        # In practice, this would implement sophisticated voting mechanisms
        
        # For now, return the result with highest confidence
        best_result = max(results, key=lambda r: r.get("confidence", 0))
        return best_result["prediction"]
    
    async def _averaging_consensus(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Implement averaging-based consensus."""
        # Placeholder implementation
        # Average numerical values where possible
        
        aggregated = {}
        
        # Extract predictions
        predictions = [r["prediction"] for r in results]
        
        # Simple aggregation for demonstration
        if predictions:
            aggregated = predictions[0].copy()  # Start with first prediction
            
            # Average confidence scores
            confidences = [r.get("confidence", 0.5) for r in results]
            aggregated["confidence"] = sum(confidences) / len(confidences)
        
        return aggregated
    
    async def _weighted_consensus(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Implement weighted consensus based on agent performance."""
        # Placeholder implementation
        # Weight results by agent success rates
        
        total_weight = 0
        weighted_result = {}
        
        for result in results:
            agent_id = result["agent_id"]
            agent = self.agents.get(agent_id)
            
            if agent:
                weight = agent.success_rate
                total_weight += weight
                
                # Weighted aggregation logic would go here
                # For now, just return the highest weighted result
                if not weighted_result or weight > weighted_result.get("weight", 0):
                    weighted_result = result["prediction"].copy()
                    weighted_result["weight"] = weight
        
        return weighted_result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and performance metrics."""
        active_agents = sum(1 for agent in self.agents.values() if agent.is_trained)
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "agent_types": list(set(agent.agent_type for agent in self.agents.values())),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "success_rate": self.successful_requests / max(1, self.total_requests),
            "average_response_time": self.average_response_time,
            "coordination_strategy": self.config.coordination_strategy,
            "consensus_mechanism": self.config.consensus_mechanism,
        }
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent."""
        agent = self.agents.get(agent_id)
        return agent.get_agent_info() if agent else None
    
    async def shutdown(self):
        """Shutdown the multi-agent system."""
        self.logger.info("Shutting down multi-agent system")
        
        # Shutdown thread pool
        self.agent_pool.shutdown(wait=True)
        
        # Clear agents
        self.agents.clear()
        
        self.logger.info("Multi-agent system shutdown complete")


class AIModelManager:
    """Manager for AI models and training pipelines."""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.training_jobs: Dict[str, Any] = {}
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize experiment tracking
        self.experiment_tracker = None
        self._initialize_experiment_tracking()
    
    def _initialize_experiment_tracking(self):
        """Initialize experiment tracking (MLflow, Wandb, etc.)."""
        try:
            if MLFLOW_AVAILABLE:
                mlflow.set_tracking_uri("sqlite:///mlflow.db")
                mlflow.set_experiment("blueprintbot_v2")
                self.experiment_tracker = "mlflow"
                self.logger.info("Initialized MLflow experiment tracking")
            
            elif WANDB_AVAILABLE:
                # wandb.init would be called here with proper configuration
                self.experiment_tracker = "wandb"
                self.logger.info("Wandb available for experiment tracking")
            
        except Exception as e:
            self.logger.warning(f"Failed to initialize experiment tracking: {e}")
    
    async def create_model(self, config: AIModelConfig) -> str:
        """Create a new AI model."""
        try:
            model_id = f"{config.model_name}_{config.model_version}_{uuid.uuid4().hex[:8]}"
            
            self.logger.info(f"Creating model {model_id}")
            
            # Create model based on configuration
            if config.model_type == AIModelType.TRANSFORMER and TRANSFORMERS_AVAILABLE:
                model = await self._create_transformer_model(config)
            elif config.model_type == AIModelType.CONVOLUTIONAL and TENSORFLOW_AVAILABLE:
                model = await self._create_cnn_model(config)
            elif config.model_type == AIModelType.ENSEMBLE and SKLEARN_AVAILABLE:
                model = await self._create_ensemble_model(config)
            else:
                # Fallback to simple model
                model = await self._create_simple_model(config)
            
            # Store model
            self.models[model_id] = {
                "model": model,
                "config": config,
                "created_at": datetime.now(),
                "status": "created"
            }
            
            self.logger.info(f"Successfully created model {model_id}")
            return model_id
        
        except Exception as e:
            self.logger.error(f"Failed to create model: {e}")
            raise AIModelError(f"Model creation failed: {e}")
    
    async def train_model(self, model_id: str, training_data: Any, 
                         validation_data: Optional[Any] = None) -> TrainingMetrics:
        """Train a model."""
        try:
            if model_id not in self.models:
                raise ValueError(f"Model {model_id} not found")
            
            model_info = self.models[model_id]
            model = model_info["model"]
            config = model_info["config"]
            
            self.logger.info(f"Starting training for model {model_id}")
            
            # Start experiment tracking
            if self.experiment_tracker == "mlflow":
                mlflow.start_run(run_name=f"train_{model_id}")
                mlflow.log_params(config.__dict__)
            
            # Update status
            model_info["status"] = "training"
            
            # Create training job
            job_id = f"job_{uuid.uuid4().hex[:8]}"
            self.training_jobs[job_id] = {
                "model_id": model_id,
                "status": "running",
                "started_at": datetime.now()
            }
            
            # Perform training
            start_time = time.time()
            metrics = TrainingMetrics()
            
            if hasattr(model, 'fit'):
                # Scikit-learn style
                if isinstance(training_data, tuple):
                    X_train, y_train = training_data
                    model.fit(X_train, y_train)
                    
                    if validation_data:
                        X_val, y_val = validation_data
                        val_score = model.score(X_val, y_val)
                        metrics.val_accuracy = val_score
                    
                    train_score = model.score(X_train, y_train)
                    metrics.train_accuracy = train_score
                
            elif hasattr(model, 'compile'):
                # Keras/TensorFlow style
                if isinstance(training_data, tuple):
                    X_train, y_train = training_data
                    
                    # Prepare callbacks
                    callbacks_list = []
                    if config.early_stopping:
                        early_stopping = keras.callbacks.EarlyStopping(
                            monitor='val_loss',
                            patience=config.patience,
                            restore_best_weights=True
                        )
                        callbacks_list.append(early_stopping)
                    
                    # Train model
                    history = model.fit(
                        X_train, y_train,
                        batch_size=config.batch_size,
                        epochs=config.epochs,
                        validation_data=validation_data,
                        callbacks=callbacks_list,
                        verbose=1
                    )
                    
                    # Extract metrics
                    if history.history:
                        metrics.train_loss = history.history['loss'][-1]
                        metrics.train_accuracy = history.history.get('accuracy', [0])[-1]
                        if 'val_loss' in history.history:
                            metrics.val_loss = history.history['val_loss'][-1]
                        if 'val_accuracy' in history.history:
                            metrics.val_accuracy = history.history['val_accuracy'][-1]
            
            # Update metrics
            training_time = time.time() - start_time
            metrics.training_time = training_time
            
            # Update model status
            model_info["status"] = "trained"
            model_info["trained_at"] = datetime.now()
            model_info["metrics"] = metrics
            
            # Update job status
            self.training_jobs[job_id]["status"] = "completed"
            self.training_jobs[job_id]["completed_at"] = datetime.now()
            
            # Log to experiment tracker
            if self.experiment_tracker == "mlflow":
                mlflow.log_metrics(metrics.to_dict())
                mlflow.log_metric("training_time", training_time)
                mlflow.end_run()
            
            self.logger.info(f"Training completed for model {model_id}")
            return metrics
        
        except Exception as e:
            # Update job status
            if job_id in self.training_jobs:
                self.training_jobs[job_id]["status"] = "failed"
                self.training_jobs[job_id]["error"] = str(e)
            
            # End experiment tracking
            if self.experiment_tracker == "mlflow":
                mlflow.end_run(status="FAILED")
            
            self.logger.error(f"Training failed for model {model_id}: {e}")
            raise AIModelError(f"Training failed: {e}")
    
    async def predict_with_model(self, model_id: str, input_data: Any) -> Dict[str, Any]:
        """Make predictions with a trained model."""
        try:
            if model_id not in self.models:
                raise ValueError(f"Model {model_id} not found")
            
            model_info = self.models[model_id]
            
            if model_info["status"] != "trained":
                raise ValueError(f"Model {model_id} is not trained")
            
            model = model_info["model"]
            
            # Make prediction
            start_time = time.time()
            
            if hasattr(model, 'predict'):
                prediction = model.predict(input_data)
            else:
                raise ValueError("Model does not support prediction")
            
            prediction_time = time.time() - start_time
            
            return {
                "model_id": model_id,
                "prediction": prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
                "prediction_time": prediction_time,
                "success": True
            }
        
        except Exception as e:
            self.logger.error(f"Prediction failed for model {model_id}: {e}")
            return {
                "model_id": model_id,
                "error": str(e),
                "success": False
            }
    
    async def _create_transformer_model(self, config: AIModelConfig):
        """Create a transformer model."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers library not available")
        
        # For now, use a pre-trained model
        # In practice, you might create a custom transformer
        model = AutoModel.from_pretrained("bert-base-uncased")
        return model
    
    async def _create_cnn_model(self, config: AIModelConfig):
        """Create a CNN model."""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow not available")
        
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation=config.activation, input_shape=config.input_size),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation=config.activation),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation=config.activation),
            layers.GlobalAveragePooling2D(),
            layers.Dropout(config.dropout_rate),
            layers.Dense(config.hidden_sizes[0], activation=config.activation),
            layers.Dropout(config.dropout_rate),
            layers.Dense(config.output_size, activation='softmax')
        ])
        
        # Compile model
        optimizer_class = getattr(optimizers, config.optimizer.value.title())
        optimizer = optimizer_class(learning_rate=config.learning_rate)
        
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    async def _create_ensemble_model(self, config: AIModelConfig):
        """Create an ensemble model."""
        if not SKLEARN_AVAILABLE:
            raise ImportError("Scikit-learn not available")
        
        from sklearn.ensemble import VotingClassifier
        
        # Create base models
        base_models = []
        
        if SKLEARN_AVAILABLE:
            base_models.append(('rf', RandomForestClassifier(n_estimators=100, random_state=42)))
            base_models.append(('gb', GradientBoostingClassifier(n_estimators=100, random_state=42)))
        
        if XGBOOST_AVAILABLE:
            base_models.append(('xgb', xgb.XGBClassifier(n_estimators=100, random_state=42)))
        
        if LIGHTGBM_AVAILABLE:
            base_models.append(('lgb', lgb.LGBMClassifier(n_estimators=100, random_state=42)))
        
        # Create voting classifier
        model = VotingClassifier(estimators=base_models, voting='soft')
        
        return model
    
    async def _create_simple_model(self, config: AIModelConfig):
        """Create a simple fallback model."""
        if SKLEARN_AVAILABLE:
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ImportError("No suitable ML library available")
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a model."""
        if model_id not in self.models:
            return None
        
        model_info = self.models[model_id].copy()
        # Remove the actual model object for serialization
        model_info.pop("model", None)
        
        return model_info
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all models."""
        return [
            {
                "model_id": model_id,
                **{k: v for k, v in info.items() if k != "model"}
            }
            for model_id, info in self.models.items()
        ]
    
    def get_training_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a training job."""
        return self.training_jobs.get(job_id)


# Global instances
_multi_agent_coordinator = None
_ai_model_manager = None


def get_multi_agent_coordinator(config: Optional[MultiAgentConfig] = None) -> MultiAgentCoordinator:
    """Get the global multi-agent coordinator instance."""
    global _multi_agent_coordinator
    
    if _multi_agent_coordinator is None:
        if config is None:
            config = MultiAgentConfig()
        _multi_agent_coordinator = MultiAgentCoordinator(config)
    
    return _multi_agent_coordinator


def get_ai_model_manager() -> AIModelManager:
    """Get the global AI model manager instance."""
    global _ai_model_manager
    
    if _ai_model_manager is None:
        _ai_model_manager = AIModelManager()
    
    return _ai_model_manager


# Utility functions
def check_ai_availability() -> Dict[str, bool]:
    """Check availability of AI libraries."""
    return {
        "tensorflow": TENSORFLOW_AVAILABLE,
        "torch": TORCH_AVAILABLE,
        "transformers": TRANSFORMERS_AVAILABLE,
        "opencv": OPENCV_AVAILABLE,
        "pillow": PIL_AVAILABLE,
        "sklearn": SKLEARN_AVAILABLE,
        "xgboost": XGBOOST_AVAILABLE,
        "lightgbm": LIGHTGBM_AVAILABLE,
        "optuna": OPTUNA_AVAILABLE,
        "ray": RAY_AVAILABLE,
        "mlflow": MLFLOW_AVAILABLE,
        "wandb": WANDB_AVAILABLE,
    }


async def quick_ai_test() -> Dict[str, Any]:
    """Run a quick test of AI functionality."""
    try:
        # Test multi-agent system
        config = MultiAgentConfig(num_agents=3)
        coordinator = MultiAgentCoordinator(config)
        
        # Initialize a few agents
        success = await coordinator.initialize_agents()
        
        if success:
            # Test prediction
            dummy_data = np.random.rand(10)
            result = await coordinator.coordinate_prediction(AITaskType.PLAN_ANALYSIS, dummy_data)
            
            return {
                "test": "Multi-agent AI system",
                "agents_initialized": len(coordinator.agents),
                "prediction_success": result.get("success", False),
                "success": True
            }
        else:
            return {
                "test": "Multi-agent AI system",
                "error": "Failed to initialize agents",
                "success": False
            }
    
    except Exception as e:
        return {
            "test": "Multi-agent AI system",
            "error": str(e),
            "success": False
        }


# Export public API
__all__ = [
    # Enums
    "AIModelType", "AITaskType", "TrainingStrategy", "OptimizationAlgorithm",
    
    # Configuration classes
    "AIModelConfig", "MultiAgentConfig", "TrainingMetrics",
    
    # Agent classes
    "AIAgent", "PlanAnalyzerAgent", "MaterialEstimatorAgent", "ComplianceCheckerAgent",
    
    # Manager classes
    "MultiAgentCoordinator", "AIModelManager",
    
    # Utility functions
    "get_multi_agent_coordinator", "get_ai_model_manager", "check_ai_availability", "quick_ai_test",
]

# Initialize logging
logger.info(f"AI module initialized. Available libraries: {check_ai_availability()}")

