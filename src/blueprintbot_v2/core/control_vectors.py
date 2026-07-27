import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger("blueprintbot_v2.core.control_vectors")

@dataclass
class ControlVector:
    """
    Represents a control parameter that can be dynamically adjusted at runtime.
    """
    name: str
    value: Any
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    data_type: str = "float"
    description: str = ""
    mutable: bool = True
    last_updated: str = ""

    def validate(self, new_value: Any) -> bool:
        """
        Validates a new value against the control vector's constraints.
        """
        if self.data_type == "float":
            try:
                val = float(new_value)
                if self.min_value is not None and val < self.min_value:
                    return False
                if self.max_value is not None and val > self.max_value:
                    return False
                return True
            except (ValueError, TypeError):
                return False
        elif self.data_type == "int":
            try:
                val = int(new_value)
                if self.min_value is not None and val < self.min_value:
                    return False
                if self.max_value is not None and val > self.max_value:
                    return False
                return True
            except (ValueError, TypeError):
                return False
        elif self.data_type == "bool":
            return isinstance(new_value, bool)
        elif self.data_type == "string":
            return isinstance(new_value, str)
        return True

    def update(self, new_value: Any) -> bool:
        """
        Updates the control vector's value if validation passes.
        """
        if not self.mutable:
            logger.warning(f"Control vector '{self.name}' is immutable.")
            return False
        
        if self.validate(new_value):
            self.value = new_value
            self.last_updated = datetime.utcnow().isoformat()
            logger.info(f"Control vector '{self.name}' updated to {new_value}")
            return True
        else:
            logger.error(f"Invalid value for control vector '{self.name}': {new_value}")
            return False

class ControlVectorManager:
    """
    Manages all control vectors for the BlueprintBot v2 OS.
    """
    def __init__(self):
        self.control_vectors: Dict[str, ControlVector] = {}
        self._initialize_default_vectors()
        self.lock = asyncio.Lock()

    def _initialize_default_vectors(self):
        """
        Initializes default control vectors for the system.
        """
        # CPU Scheduling Control Vectors
        self.control_vectors["cpu_frequency_scaling"] = ControlVector(
            name="cpu_frequency_scaling",
            value=1.0,
            min_value=0.5,
            max_value=2.0,
            data_type="float",
            description="CPU frequency scaling factor (0.5 = 50%, 1.0 = 100%, 2.0 = 200%)",
            mutable=True
        )

        # Memory Management Control Vectors
        self.control_vectors["memory_pressure_threshold"] = ControlVector(
            name="memory_pressure_threshold",
            value=0.85,
            min_value=0.5,
            max_value=0.95,
            data_type="float",
            description="Memory usage threshold for triggering garbage collection",
            mutable=True
        )

        # Quantum Processing Control Vectors
        self.control_vectors["quantum_circuit_depth"] = ControlVector(
            name="quantum_circuit_depth",
            value=10,
            min_value=1,
            max_value=100,
            data_type="int",
            description="Maximum depth of quantum circuits",
            mutable=True
        )

        self.control_vectors["quantum_error_correction_enabled"] = ControlVector(
            name="quantum_error_correction_enabled",
            value=True,
            data_type="bool",
            description="Enable quantum error correction",
            mutable=True
        )

        # AI Model Control Vectors
        self.control_vectors["ai_batch_size"] = ControlVector(
            name="ai_batch_size",
            value=32,
            min_value=1,
            max_value=256,
            data_type="int",
            description="Batch size for AI model inference",
            mutable=True
        )

        self.control_vectors["ai_inference_timeout"] = ControlVector(
            name="ai_inference_timeout",
            value=30,
            min_value=5,
            max_value=300,
            data_type="int",
            description="Timeout for AI inference operations (seconds)",
            mutable=True
        )

        # Security Control Vectors
        self.control_vectors["encryption_enabled"] = ControlVector(
            name="encryption_enabled",
            value=True,
            data_type="bool",
            description="Enable end-to-end encryption",
            mutable=False  # Immutable for security
        )

        self.control_vectors["access_control_level"] = ControlVector(
            name="access_control_level",
            value=2,
            min_value=1,
            max_value=5,
            data_type="int",
            description="Access control level (1=open, 5=restricted)",
            mutable=True
        )

        # Analytics Control Vectors
        self.control_vectors["analytics_collection_interval"] = ControlVector(
            name="analytics_collection_interval",
            value=10,
            min_value=1,
            max_value=60,
            data_type="int",
            description="Analytics collection interval (seconds)",
            mutable=True
        )

        logger.info(f"Initialized {len(self.control_vectors)} default control vectors.")

    async def get_control_vector(self, name: str) -> Optional[ControlVector]:
        """
        Retrieves a control vector by name.
        """
        async with self.lock:
            return self.control_vectors.get(name)

    async def set_control_vector(self, name: str, value: Any) -> bool:
        """
        Sets a control vector's value.
        """
        async with self.lock:
            if name not in self.control_vectors:
                logger.error(f"Control vector '{name}' not found.")
                return False
            
            return self.control_vectors[name].update(value)

    async def get_all_control_vectors(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns all control vectors as a dictionary.
        """
        async with self.lock:
            return {
                name: asdict(cv)
                for name, cv in self.control_vectors.items()
            }

    async def apply_adaptive_tuning(self, system_metrics: Dict[str, Any]) -> Dict[str, bool]:
        """
        Applies adaptive tuning based on current system metrics.
        Automatically adjusts control vectors to optimize performance.
        """
        results = {}
        
        # Example: Adjust CPU frequency scaling based on CPU usage
        cpu_usage = system_metrics.get("cpu_usage", 0)
        if cpu_usage > 0.9:
            results["cpu_frequency_scaling"] = await self.set_control_vector("cpu_frequency_scaling", 1.5)
        elif cpu_usage < 0.3:
            results["cpu_frequency_scaling"] = await self.set_control_vector("cpu_frequency_scaling", 0.8)

        # Example: Adjust memory pressure threshold based on memory usage
        memory_usage = system_metrics.get("memory_usage", 0)
        if memory_usage > 0.9:
            results["memory_pressure_threshold"] = await self.set_control_vector("memory_pressure_threshold", 0.75)

        # Example: Adjust AI batch size based on available GPU memory
        gpu_memory_available = system_metrics.get("gpu_memory_available", 0)
        if gpu_memory_available > 4000:  # 4GB
            results["ai_batch_size"] = await self.set_control_vector("ai_batch_size", 64)
        elif gpu_memory_available < 1000:  # 1GB
            results["ai_batch_size"] = await self.set_control_vector("ai_batch_size", 16)

        logger.info(f"Adaptive tuning applied: {results}")
        return results

class SystemOrchestrator:
    """
    Orchestrates the entire BlueprintBot v2 OS, coordinating between kernel, analytics, and control vectors.
    """
    def __init__(self, kernel, analytics_manager):
        self.kernel = kernel
        self.analytics_manager = analytics_manager
        self.control_vector_manager = ControlVectorManager()
        self.orchestration_tasks: List[asyncio.Task] = []

    async def initialize(self):
        """
        Initializes the system orchestrator and starts background tasks.
        """
        logger.info("Initializing SystemOrchestrator...")
        await self.kernel.initialize()
        await self.control_vector_manager.get_all_control_vectors()
        
        # Start background orchestration tasks
        self.orchestration_tasks.append(asyncio.create_task(self._monitoring_loop()))
        self.orchestration_tasks.append(asyncio.create_task(self._adaptive_tuning_loop()))
        
        logger.info("SystemOrchestrator initialized.")

    async def shutdown(self):
        """
        Shuts down the system orchestrator and all background tasks.
        """
        logger.info("Shutting down SystemOrchestrator...")
        for task in self.orchestration_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        await self.kernel.shutdown()
        logger.info("SystemOrchestrator shut down.")

    async def _monitoring_loop(self):
        """
        Continuous monitoring loop that collects system metrics and health data.
        """
        while True:
            try:
                health_status = await self.analytics_manager.analyze_system_health()
                logger.debug(f"System health: {health_status}")
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}", exc_info=True)
                await asyncio.sleep(5)

    async def _adaptive_tuning_loop(self):
        """
        Continuous adaptive tuning loop that adjusts control vectors based on system metrics.
        """
        while True:
            try:
                # Collect current system metrics
                system_metrics = {
                    "cpu_usage": 0.5,  # Placeholder
                    "memory_usage": 0.6,  # Placeholder
                    "gpu_memory_available": 2000  # Placeholder
                }
                
                # Apply adaptive tuning
                await self.control_vector_manager.apply_adaptive_tuning(system_metrics)
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Adaptive tuning loop error: {e}", exc_info=True)
                await asyncio.sleep(10)

# Global orchestrator instance (to be initialized at startup)
system_orchestrator: Optional[SystemOrchestrator] = None
