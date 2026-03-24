# Heap-Based Priority Queue: Emergency Room Triage System

## Problem Context
In hospital emergency rooms, patients are treated based on severity — not arrival order.
This system uses a **Max-Heap** to ensure the most critical patients are always treated first.

## Project Structure
```
er_triage_system/
├── heap.py               # Max-heap implementation (core data structure)
├── patient.py            # Patient data structure
├── simulation.py         # ER simulation logic
├── dataset.py            # Dataset generator
├── main.py               # Main execution file
├── README.md             # Documentation
├── patients.csv          # Generated dataset (after running)
└── treatment_report.csv  # Simulation results (after running)
```

## How to Run

### Requirements
- Python 3.7+
- No external libraries required

### Run the full project
```bash
cd er_triage_system
python main.py
```

### Run individual modules
```bash
python dataset.py       # Generate patients.csv only
python simulation.py    # Requires patients.csv
```

## Algorithm Summary

| Operation          | Complexity  | Description                        |
|--------------------|-------------|------------------------------------|
| insert()           | O(log n)    | Add patient, bubble up             |
| extract_max()      | O(log n)    | Remove most critical, heapify down |
| increase_priority()| O(n + log n)| Find + bubble up                   |
| build_max_heap()   | O(n)        | Build from unsorted array          |
| is_empty()         | O(1)        | Check size                         |
| Space              | O(n)        | Fixed-size array                   |

## Priority Scale
| Priority | Condition            |
|----------|----------------------|
| 10       | Cardiac Arrest       |
| 9        | Severe Trauma        |
| 8        | Stroke               |
| 7        | Respiratory Failure  |
| 6        | Severe Bleeding      |
| 5        | Broken Bone          |
| 4        | High Fever           |
| 3        | Moderate Pain        |
| 2        | Minor Laceration     |
| 1        | Common Cold          |

## Dataset
- 1,000 synthetic patients generated with `random` (seed=42)
- Arrivals spread across a 24-hour window
- Saved to `patients.csv`

## Output
- `patients.csv` — Full patient dataset
- `treatment_report.csv` — Treatment order with timestamps

## Dataset Source
Self-generated using Python's built-in `random` module (seed=42 for reproducibility).
