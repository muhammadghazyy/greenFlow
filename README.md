# GreenFlow 🚦

**A Simple Adaptive Traffic Light Controller**

GreenFlow is a simple Python prototype exploring how traffic lights can dynamically adjust **green-light duration based on traffic demand**.

The goal is straightforward:

> Reduce unnecessary waiting time by giving more green time to roads with more traffic, while maintaining a fixed and fair rotation between roads.

## Current MVP

GreenFlow currently simulates a **3-way intersection**:

```text
          B
          |
          |
      ----+----
       A     C
```

The traffic-light sequence is fixed:

```text
A → B → C → A → B → C → ...
```

The **order does not change**. Instead, GreenFlow dynamically determines how long each road receives a green light.

### Example

```text
A = 12 vehicles
B = 3 vehicles
C = 7 vehicles

A → GREEN
B → RED
C → RED

Green duration: based on A's traffic
```

After the green phase, traffic is updated and the controller moves to the next road.

## Current Approach

The current prototype uses a simple rule-based controller.

Conceptually:

```text
Vehicle count
      ↓
Green duration
      ↓
Traffic light
      ↓
Traffic changes
      ↓
Next road
```

There is currently **no AI or machine learning** involved.

## Project Goals

This project is an experimental prototype.

Future versions may explore:

* Better green-time calculation
* Traffic arrival and departure modeling
* Waiting-time measurement
* Comparison against fixed-time traffic lights
* Vehicle detection
* Computer vision
* Pedestrian crossing logic
* Emergency vehicle priority
* Multi-intersection coordination
* Real-world traffic signal integration

## Status

**MVP / Experiment**

The current objective is to determine whether a simple adaptive controller can reduce overall waiting time compared with conventional fixed-duration traffic signals.

## Tech Stack

* Python
* Standard Python libraries

No external dependencies are currently required.

## Disclaimer

GreenFlow is currently a **simulation/prototype project** and is not designed to control real traffic infrastructure.
