# Traffic Wait Comparison Summary

Simulation timestamp: 2026-09-24 04:39:08
Scenario: default
Road order: A -> B -> C
Initial traffic: A=36, B=3, C=6
Arrival rates: A=0.5, B=0.125, C=0.0625

## Method
- Fixed signal order follows the configured road list
- Adaptive strategy adjusts green duration using traffic count
- Flat strategy uses a constant 30-second green duration
- Per-road wait is the average wait while that road is red before its next green phase

## Result Summary

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

## CSV Output
- File: [traffic_wait_comparison._20260924113908.csv](logs/traffic_wait_comparison._20260924113908.csv)

## Detailed Results

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
