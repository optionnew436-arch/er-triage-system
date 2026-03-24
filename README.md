# Heap-Based Priority Queue: Emergency Room Triage System

## How to Run

### Requirements
- Python 3.7 or higher
- No external libraries needed

### Steps
```bash
cd er_triage_system
python main.py
```

That's it. Two output files will be created:
- `patients.csv` — 1,000 synthetic patients dataset
- `treatment_report.csv` — full treatment order log

To view the visual dashboard:
```bash
python serve.py
```
Then open `http://localhost:8080/dashboard.html` in your browser.

---

## Project Structure
```
er_triage_system/
├── heap.py               # Max-heap with all required operations
├── patient.py            # Patient data structure
├── simulation.py         # 24-hour ER simulation logic
├── dataset.py            # Dataset generator (1,000 patients → CSV)
├── main.py               # Main execution file
├── dashboard.html        # Visual browser dashboard
├── serve.py              # Local server for dashboard
├── README.md             # This file
├── patients.csv          # Generated after running main.py
└── treatment_report.csv  # Simulation results after running main.py
```

---

## Heap Operations Implemented

| Operation              | Signature                                      | Complexity   |
|------------------------|------------------------------------------------|--------------|
| `insert()`             | `insert(patientID, priority, time, condition)` | O(log n)     |
| `extractMax()`         | `extractMax()`                                 | O(log n)     |
| `increasePriority()`   | `increasePriority(patientID, newPriority)`     | O(n + log n) |
| `isEmpty()`            | `isEmpty()`                                    | O(1)         |
| `maxHeapify()`         | `maxHeapify(i)`                                | O(log n)     |
| `buildMaxHeap()`       | `buildMaxHeap(patients)`                       | O(n)         |

---

## Heap Indexing (Zero-Based)
```
Parent(i)      = (i - 1) // 2
LeftChild(i)   = 2 * i + 1
RightChild(i)  = 2 * i + 2
```

---

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

---

## Complexity Summary
| Operation       | Time       | Proof                          |
|-----------------|------------|--------------------------------|
| insert          | O(log n)   | Bubble-up ≤ tree height        |
| extractMax      | O(log n)   | maxHeapify ≤ tree height       |
| buildMaxHeap    | O(n)       | Σ(n/2^h × h) = O(n)           |
| Space           | O(n)       | Fixed-size array + O(log n) stack |

---

## Dataset Source
Self-generated using Python `random` module (seed=42 for reproducibility).
1,000 patients with unique IDs, priorities 1–10, and random arrival times across 24 hours.
