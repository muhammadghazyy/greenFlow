# Traffic Wait Comparison Summary

Simulation timestamp: 2026-09-24 04:17:32

## Method
- Fixed A -> B -> C signal order
- Adaptive strategy adjusts green duration using traffic count
- Flat strategy uses a constant 30-second green duration
- Per-road wait is the average wait while that road is red before its next green phase

## Result Summary

- Adaptive total wait: 838s
- Flat 30s total wait: 900s
- Difference: 62s

### Adaptive average red-light wait per road
- A: 37.2s
- B: 46.4s
- C: 41.4s

### Flat 30s average red-light wait per road
- A: 45s
- B: 42.9s
- C: 47.1s

## CSV Output
- File: [traffic_wait_comparison._20260924111732.csv](logs/traffic_wait_comparison._20260924111732.csv)

## Detailed Results

### adaptive total
- Total wait: 838s
- A average wait while red: 37.2s
- B average wait while red: 46.4s
- C average wait while red: 41.4s

### flat_30s total
- Total wait: 900s
- A average wait while red: 45s
- B average wait while red: 42.9s
- C average wait while red: 47.1s
