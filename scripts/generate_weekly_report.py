#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from blueprintbot_v2.core.reporting import QuantumMetricsCollector, QuantumReportGenerator

def main():
    report_dir = "/home/ubuntu/blueprintbot_v2/reports"
    os.makedirs(report_dir, exist_ok=True)
    
    collector = QuantumMetricsCollector()
    generator = QuantumReportGenerator(collector)
    
    report_content = generator.generate_weekly_report()
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"quantum_weekly_report_{timestamp}.md")
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"Weekly report generated at: {report_path}")
    
    # Also update a 'latest' symlink or file
    latest_path = os.path.join(report_dir, "latest_quantum_report.md")
    with open(latest_path, 'w') as f:
        f.write(report_content)

if __name__ == "__main__":
    main()
