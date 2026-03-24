# ============================================================
# simulation.py — 24-Hour ER Simulation Logic
# - Reads patients from CSV (Input from file as required)
# - Patients arrive randomly throughout the day
# - Every 5 minutes the most critical patient is treated (extractMax)
# - Demonstrates increasePriority when condition worsens
# - Verifies higher priority patients are always treated first
# ============================================================

import csv
from datetime import datetime, timedelta
from heap import MaxHeap

TREATMENT_INTERVAL = 5   # treat one patient every 5 sim-minutes
SIMULATION_HOURS   = 24


def run_simulation(patients):
    """
    Simulate a 24-hour ER operation using the MaxHeap priority queue.
    Returns a list of treatment records.
    """
    heap = MaxHeap(max_size=2000)
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    end_time  = base_time + timedelta(hours=SIMULATION_HOURS)

    treatment_log  = []
    arrival_index  = 0
    total          = len(patients)
    treatment_count = 0
    current_time   = base_time

    # Track which patients had priority increased (demo)
    priority_increased = set()

    print("=" * 70)
    print("        EMERGENCY ROOM TRIAGE — 24-HOUR SIMULATION")
    print("=" * 70)
    print(f"{'Time':<8} {'Event':<18} {'Patient ID':<12} {'Priority':<10} {'Condition'}")
    print("-" * 70)

    while current_time <= end_time:

        # ── Admit all patients who have arrived by current_time ──
        while arrival_index < total:
            arr = datetime.strptime(
                patients[arrival_index].arrival_time, "%Y-%m-%d %H:%M:%S"
            )
            if arr <= current_time:
                p = patients[arrival_index]
                # Use insert(patientID, priority, arrival_time, condition)
                heap.insert(p.patient_id, p.priority, p.arrival_time, p.condition)
                print(f"{current_time.strftime('%H:%M'):<8} {'ARRIVED':<18} "
                      f"{p.patient_id:<12} {p.priority:<10} {p.condition}")
                arrival_index += 1
            else:
                break

        # ── Demo: increasePriority for one patient at 06:00 ──────
        if current_time == datetime(2024, 1, 1, 6, 0, 0):
            # Find a low-priority patient in the heap and worsen condition
            for i in range(heap.size):
                candidate = heap.heap[i]
                if candidate and candidate.priority <= 3 and candidate.patient_id not in priority_increased:
                    print(f"\n[ALERT] {candidate.patient_id} condition worsened!")
                    heap.increasePriority(candidate.patient_id, candidate.priority + 5)
                    priority_increased.add(candidate.patient_id)
                    break
            print()

        # ── Treat the most critical patient (extractMax) ─────────
        if not heap.isEmpty():
            treated = heap.extractMax()
            treatment_count += 1
            treatment_log.append({
                "treatment_order": treatment_count,
                "treated_at":      current_time.strftime("%H:%M"),
                "patient_id":      treated.patient_id,
                "priority":        treated.priority,
                "condition":       treated.condition,
                "arrival_time":    treated.arrival_time,
            })
            print(f"{current_time.strftime('%H:%M'):<8} {'>>> TREATED':<18} "
                  f"{treated.patient_id:<12} {treated.priority:<10} {treated.condition}")

        current_time += timedelta(minutes=TREATMENT_INTERVAL)

    print("=" * 70)
    print(f"\n[SIM] Simulation complete — {treatment_count} patients treated.\n")
    return treatment_log


def verify_priority_order(treatment_log, show=20):
    """
    Print first N treated patients to verify priority ordering.
    Higher priority patients should appear first in the list.
    """
    print(f"\n{'#':<6} {'Time':<8} {'Patient':<12} {'Priority':<10} {'Visual Bar'}")
    print("-" * 55)
    for entry in treatment_log[:show]:
        bar = "█" * entry["priority"]
        print(f"{entry['treatment_order']:<6} {entry['treated_at']:<8} "
              f"{entry['patient_id']:<12} {entry['priority']:<10} {bar}")


def save_report(treatment_log, filepath="treatment_report.csv"):
    """Save treatment log to CSV — readable output format as required."""
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "treatment_order", "treated_at", "patient_id",
            "priority", "condition", "arrival_time"
        ])
        writer.writeheader()
        writer.writerows(treatment_log)
    print(f"[SIM] Treatment report saved → {filepath}")
