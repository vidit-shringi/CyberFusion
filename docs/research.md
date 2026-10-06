# CyberFusion Research Methodology

## Research question
Can multi-source event correlation combined with behavioral anomaly detection and vulnerability context produce fewer, higher-value incidents than isolated rule-based detection?

## Baseline
Rule engine only.

## Proposed system
Rule engine + anomaly score + correlation score + threat intelligence.

## Metrics
- Precision
- Recall
- F1-score
- False-positive rate
- Detection latency
- Raw event count vs incident count
- Investigation effort/time

## Reproducibility
Synthetic scenarios are seeded. Store the seed, event count and scenario name with every experiment.

## Limitations
- Student-scale event volume
- Simplified entity resolution
- No enterprise SIEM connector
- No autonomous containment
- Synthetic data may not capture all real-world behavior
- PQC module is experimental
