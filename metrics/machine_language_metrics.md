# BlueprintBot V2: Machine Registered Language Input/Output Metrics

## 1. Overview

This document defines the machine-registered language input/output metrics for BlueprintBot V2, ensuring precise accuracy checks, robust revision deliberation, and auditable performance across all operational phases. These metrics are crucial for maintaining the integrity of the AI-driven construction processes and for continuous optimization.

## 2. Input Metrics

### 2.1 Blueprint Ingestion Metrics

| Metric Name | Description | Unit | Accuracy Target | Revision Protocol |
| :--- | :--- | :--- | :--- | :--- |
| `pdf_parse_accuracy` | Percentage of text and vector graphics correctly extracted from PDF blueprints. | % | >99.9% | Automated comparison with ground truth, human review for discrepancies >0.1% |
| `image_ocr_accuracy` | Percentage of text correctly recognized from scanned image blueprints. | % | >99.5% | OCR engine retraining, manual correction of misidentified characters |
| `dwg_feature_extraction_precision` | Precision of extracting geometric features (lines, arcs, dimensions) from DWG files. | % | >99.8% | CAD model validation, comparison with BIM data, expert review |
| `semantic_entity_recognition_f1` | F1-score for identifying construction-related entities (walls, beams, windows, materials) from input documents. | F1-score | >0.98 | Active learning with human-in-the-loop feedback, ontology refinement |

### 2.2 Real-time Data Stream Metrics

| Metric Name | Description | Unit | Accuracy Target | Revision Protocol |
| :--- | :--- | :--- | :--- | :--- |
| `iot_sensor_data_integrity` | Percentage of real-time IoT sensor data (temperature, humidity, vibration) received without corruption. | % | >99.99% | CRC checks, retransmission protocols, anomaly detection |
| `cv_object_detection_mAP` | Mean Average Precision (mAP) for computer vision object detection (e.g., material tracking, worker presence). | mAP | >0.95 | Model retraining with new datasets, adversarial testing |
| `as_built_vs_as_planned_deviation` | Average deviation between real-time 
