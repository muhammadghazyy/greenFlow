# Traffic Wait Comparison Summary

Simulation timestamp: 2026-09-24 06:20:27

## Method
- Fixed signal order follows the configured road list
- Adaptive strategy adjusts green duration using traffic count
- Flat strategy uses a constant 30-second green duration
- Per-road wait is the average wait while that road is red before its next green phase

## Scenario: default
- Road order: A -> B -> C
- Initial traffic: A=36, B=3, C=6
- Arrival rates: A=0.5, B=0.125, C=0.0625
- Adaptive total wait: 805s
- Flat 30s total wait: 900s
- Difference: 95s

### Adaptive average red-light wait per road
- A: 29.5s
- B: 48.1s
- C: 41.6s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 805s
- A average wait while red: 29.5s
- B average wait while red: 48.1s
- C average wait while red: 41.6s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: heavy_c
- Road order: A -> B -> C
- Initial traffic: A=8, B=55, C=96
- Arrival rates: A=0.1, B=0.5, C=0.46
- Adaptive total wait: 1003s
- Flat 30s total wait: 900s
- Difference: -103s

### Adaptive average red-light wait per road
- A: 60s
- B: 38.1s
- C: 53.7s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 1003s
- A average wait while red: 60s
- B average wait while red: 38.1s
- C average wait while red: 53.7s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: heavy_b
- Road order: A -> B -> C
- Initial traffic: A=8, B=55, C=1
- Arrival rates: A=0.1, B=0.2, C=0.46
- Adaptive total wait: 981s
- Flat 30s total wait: 900s
- Difference: -81s

### Adaptive average red-light wait per road
- A: 57.8s
- B: 38.1s
- C: 52.4s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 981s
- A average wait while red: 57.8s
- B average wait while red: 38.1s
- C average wait while red: 52.4s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: flat
- Road order: A -> B -> C
- Initial traffic: A=41, B=43, C=46
- Arrival rates: A=0.31, B=0.27, C=0.33
- Adaptive total wait: 1200s
- Flat 30s total wait: 900s
- Difference: -300s

### Adaptive average red-light wait per road
- A: 60s
- B: 57.1s
- C: 62.9s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 1200s
- A average wait while red: 60s
- B average wait while red: 57.1s
- C average wait while red: 62.9s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## CSV Output
- File: [traffic_wait_comparison._20260924132027.csv](logs/traffic_wait_comparison._20260924132027.csv)
