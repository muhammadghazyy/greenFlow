# Traffic Wait Comparison Summary

Simulation timestamp: 2026-09-24 07:52:39

## Method
- Fixed signal order follows the configured road list
- Adaptive strategy adjusts green duration using traffic count
- Flat strategy uses a constant 30-second green duration
- Per-road wait is the average wait while that road is red before its next green phase

## Scenario: default
- Road order: A -> B -> C
- Initial traffic: A=36, B=3, C=6
- Arrival rates: A=0.5, B=0.125, C=0.0625
- Adaptive total wait: 657s
- Flat 30s total wait: 900s
- Difference: 243s

### Adaptive average red-light wait per road
- A: 26.2s
- B: 37s
- C: 34.4s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 657s
- A average wait while red: 26.2s
- B average wait while red: 37s
- C average wait while red: 34.4s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: heavy_c
- Road order: A -> B -> C
- Initial traffic: A=8, B=55, C=96
- Arrival rates: A=0.1, B=0.5, C=0.46
- Adaptive total wait: 783s
- Flat 30s total wait: 900s
- Difference: 117s

### Adaptive average red-light wait per road
- A: 45s
- B: 31.3s
- C: 42s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 783s
- A average wait while red: 45s
- B average wait while red: 31.3s
- C average wait while red: 42s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: heavy_b
- Road order: A -> B -> C
- Initial traffic: A=8, B=55, C=1
- Arrival rates: A=0.1, B=0.2, C=0.46
- Adaptive total wait: 777s
- Flat 30s total wait: 900s
- Difference: 123s

### Adaptive average red-light wait per road
- A: 44.5s
- B: 31.3s
- C: 41.6s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 777s
- A average wait while red: 44.5s
- B average wait while red: 31.3s
- C average wait while red: 41.6s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## Scenario: flat
- Road order: A -> B -> C
- Initial traffic: A=41, B=43, C=46
- Arrival rates: A=0.31, B=0.27, C=0.33
- Adaptive total wait: 900s
- Flat 30s total wait: 900s
- Difference: 0s

### Adaptive average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

### adaptive total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s

## CSV Output
- File: [traffic_wait_comparison._20260924145239.csv](logs/traffic_wait_comparison._20260924145239.csv)
