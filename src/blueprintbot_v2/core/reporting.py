"""
BlueprintBot v2: Quantum Performance Reporting Module

This module handles the collection, persistence, and generation of performance
and load distribution reports for the integrated quantum architecture.

Author: BlueprintBot Team
Version: 1.0.0
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class QuantumMetricsCollector:
    """Collects and persists performance metrics for the quantum architecture."""
    
    def __init__(self, storage_path: str = "/home/ubuntu/blueprintbot_v2/data/metrics.json"):
        self.storage_path = storage_path
        self.ensure_storage_exists()
        
    def ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
                
    def record_metric(self, provider: str, metric_type: str, value: float, metadata: Optional[Dict] = None):
        """Record a single metric point."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "provider": provider,
            "type": metric_type,
            "value": value,
            "metadata": metadata or {}
        }
        
        try:
            with open(self.storage_path, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
        except Exception as e:
            logger.error(f"Failed to record metric: {e}")

    def get_metrics_for_period(self, days: int = 7) -> List[Dict]:
        """Retrieve metrics for the specified number of days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [d for d in data if datetime.fromisoformat(d["timestamp"]) > cutoff]
        except Exception as e:
            logger.error(f"Failed to retrieve metrics: {e}")
            return []

class QuantumReportGenerator:
    """Generates performance and load distribution reports."""
    
    def __init__(self, collector: QuantumMetricsCollector):
        self.collector = collector
        
    def generate_weekly_report(self) -> str:
        """Generate a comprehensive weekly performance report in Markdown."""
        metrics = self.collector.get_metrics_for_period(7)
        if not metrics:
            return "# Quantum Architecture Weekly Report\n\nNo data available for the past 7 days."
        
        df = pd.DataFrame(metrics)
        
        # Aggregate stats
        total_tasks = len(df[df['type'] == 'task_completion'])
        avg_latency = df[df['type'] == 'latency']['value'].mean()
        total_cost = df[df['type'] == 'cost']['value'].sum()
        
        # Provider distribution
        dist = df[df['type'] == 'task_completion']['provider'].value_counts()
        
        report = [
            "# BlueprintBot v2: Quantum Architecture Weekly Performance Report",
            f"**Period:** {(datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.utcnow().strftime('%Y-%m-%d')}",
            "",
            "## Executive Summary",
            f"- **Total Quantum Tasks Executed:** {total_tasks}",
            f"- **Average System Latency:** {avg_latency:.2f} ms",
            f"- **Total Operational Cost:** ${total_cost:.2f}",
            f"- **System Availability:** {self._calculate_availability(df):.2f}%",
            "",
            "## Load Distribution by Provider",
            "| Provider | Tasks Executed | Percentage |",
            "| :--- | :--- | :--- |"
        ]
        
        for provider, count in dist.items():
            percentage = (count / total_tasks) * 100
            report.append(f"| {provider} | {count} | {percentage:.1f}% |")
            
        report.extend([
            "",
            "## Performance Metrics",
            "### Latency Analysis",
            f"- **Minimum Latency:** {df[df['type'] == 'latency']['value'].min():.2f} ms",
            f"- **Maximum Latency:** {df[df['type'] == 'latency']['value'].max():.2f} ms",
            f"- **P95 Latency:** {df[df['type'] == 'latency']['value'].quantile(0.95):.2f} ms",
            "",
            "### Error Rates",
            f"- **Total Failures:** {len(df[df['type'] == 'error'])}",
            f"- **Success Rate:** {((total_tasks - len(df[df['type'] == 'error'])) / total_tasks * 100) if total_tasks > 0 else 0:.2f}%",
            "",
            "## Recommendations",
            self._generate_recommendations(df),
            "",
            "---",
            "*Report generated automatically by BlueprintBot v2 Reporting Module*"
        ])
        
        return "\n".join(report)

    def _calculate_availability(self, df: pd.DataFrame) -> float:
        health_checks = df[df['type'] == 'health_check']
        if health_checks.empty:
            return 100.0
        return (health_checks['value'].sum() / len(health_checks)) * 100

    def _generate_recommendations(self, df: pd.DataFrame) -> str:
        # Simple logic for recommendations
        avg_latency = df[df['type'] == 'latency']['value'].mean()
        if avg_latency > 500:
            return "- **High Latency Detected:** Consider switching to a latency-optimized load balancing strategy."
        
        dist = df[df['type'] == 'task_completion']['provider'].value_counts()
        if len(dist) > 0 and dist.iloc[0] / dist.sum() > 0.8:
            return "- **Provider Concentration Risk:** Load is heavily skewed towards one provider. Review priority settings."
            
        return "- **System Healthy:** No immediate actions required. Performance is within optimal parameters."

if __name__ == "__main__":
    # Test script
    collector = QuantumMetricsCollector()
    # Mock some data if empty for demonstration
    if not collector.get_metrics_for_period(1):
        collector.record_metric("aws_braket", "task_completion", 1)
        collector.record_metric("aws_braket", "latency", 320)
        collector.record_metric("aws_braket", "cost", 0.30)
        collector.record_metric("rigetti", "task_completion", 1)
        collector.record_metric("rigetti", "latency", 510)
        collector.record_metric("rigetti", "cost", 0.50)
        collector.record_metric("aws_braket", "health_check", 1)
        collector.record_metric("rigetti", "health_check", 1)
        
    generator = QuantumReportGenerator(collector)
    print(generator.generate_weekly_report())
