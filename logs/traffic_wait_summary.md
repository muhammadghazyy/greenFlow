# Traffic Wait Comparison Summary

Simulation timestamp: 2026-09-24 03:40:03

## Method
- Fixed A -> B -> C signal order
- Adaptive strategy adjusts green duration using traffic count
- Flat strategy uses a constant 30-second green duration
- Wait estimate is based on the time until each non-green road reaches its next green phase in the rotation

## Result Summary

- Adaptive total wait: 805s
- Flat 30s total wait: 900s
- Difference: 95s

### Adaptive road totals
- A: 177s
- B: 337s
- C: 291s

### Flat 30s road totals
- A: 270s
- B: 300s
- C: 330s

## CSV Output
- File: [traffic_wait_comparison.csv](logs/traffic_wait_comparison.csv)

## Detailed Results

### adaptive total
- Total wait: 805s
- A total wait: 177s
- B total wait: 337s
- C total wait: 291s

### flat_30s total
- Total wait: 900s
- A total wait: 270s
- B total wait: 300s
- C total wait: 330s
