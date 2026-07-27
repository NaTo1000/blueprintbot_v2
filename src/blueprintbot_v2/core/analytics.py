import logging
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict

import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger("blueprintbot_v2.core.analytics")

class AnalyticsProtocol:
    """
    Defines protocols for collecting and processing system and application analytics.
    """
    def __init__(self):
        self.metrics_buffer: List[Dict[str, Any]] = []
        self.max_buffer_size = 1000
        self.last_flush_time = time.time()
        self.flush_interval = 60 # seconds

    async def log_event(self, event_type: str, data: Dict[str, Any], source: str = "system"):
        """
        Logs an analytical event to the buffer.
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "source": source,
            "data": data
        }
        self.metrics_buffer.append(event)
        
        if len(self.metrics_buffer) >= self.max_buffer_size or (time.time() - self.last_flush_time) > self.flush_interval:
            await self.flush_metrics()

    async def flush_metrics(self):
        """
        Flushes metrics from the buffer to persistent storage or a message queue.
        """
        if not self.metrics_buffer:
            return

        logger.info(f"Flushing {len(self.metrics_buffer)} metrics...")
        # In a real system, this would write to a database (e.g., TimescaleDB) or Kafka
        # For now, we'll just log a summary and clear the buffer
        self.metrics_buffer.clear()
        self.last_flush_time = time.time()

class ClusteringEngine:
    """
    Implements clustering algorithms for resource optimization and anomaly detection.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)

    def cluster_resources(self, resource_data: List[Dict[str, Any]]) -> List[int]:
        """
        Clusters compute resources based on their performance metrics.
        """
        if not resource_data:
            return []

        # Extract features for clustering (e.g., cpu_usage, memory_usage, latency)
        features = []
        for res in resource_data:
            features.append([
                res.get("cpu_usage", 0),
                res.get("memory_usage", 0),
                res.get("latency", 0)
            ])
        
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        
        clusters = self.kmeans.fit_predict(X_scaled)
        return clusters.tolist()

    def detect_anomalies(self, operational_data: List[Dict[str, Any]]) -> List[int]:
        """
        Detects anomalies in operational data using DBSCAN.
        Returns indices of anomalous data points.
        """
        if not operational_data:
            return []

        # Extract features (e.g., request_rate, error_rate, response_time)
        features = []
        for data in operational_data:
            features.append([
                data.get("request_rate", 0),
                data.get("error_rate", 0),
                data.get("response_time", 0)
            ])
        
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        
        # DBSCAN labels: -1 indicates an anomaly (noise)
        labels = self.dbscan.fit_predict(X_scaled)
        anomalies = [i for i, label in enumerate(labels) if label == -1]
        return anomalies

class SystemAnalyticsManager:
    """
    Orchestrates analytics collection and processing for the BlueprintBot v2 OS.
    """
    def __init__(self):
        self.protocol = AnalyticsProtocol()
        self.clustering = ClusteringEngine()
        self.resource_stats: List[Dict[str, Any]] = []
        self.operational_stats: List[Dict[str, Any]] = []

    async def record_resource_usage(self, stats: Dict[str, Any]):
        """
        Records current resource usage stats.
        """
        stats["timestamp"] = time.time()
        self.resource_stats.append(stats)
        if len(self.resource_stats) > 100:
            self.resource_stats.pop(0)
        
        await self.protocol.log_event("resource_usage", stats)

    async def record_operation(self, stats: Dict[str, Any]):
        """
        Records operational performance stats.
        """
        stats["timestamp"] = time.time()
        self.operational_stats.append(stats)
        if len(self.operational_stats) > 100:
            self.operational_stats.pop(0)
        
        await self.protocol.log_event("operation_stats", stats)

    async def analyze_system_health(self) -> Dict[str, Any]:
        """
        Performs a health check analysis using clustering and anomaly detection.
        """
        anomalies = self.clustering.detect_anomalies(self.operational_stats)
        resource_clusters = self.clustering.cluster_resources(self.resource_stats)
        
        health_status = "HEALTHY"
        if anomalies:
            health_status = "DEGRADED"
            logger.warning(f"Detected {len(anomalies)} operational anomalies!")

        return {
            "status": health_status,
            "anomaly_count": len(anomalies),
            "resource_clusters": resource_clusters,
            "timestamp": datetime.utcnow().isoformat()
        }

# Global analytics manager instance
analytics_manager = SystemAnalyticsManager()
