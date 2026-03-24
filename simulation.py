# ============================================================
# simulation.py — 24-Hour ER Simulation Logic
# - Patients arrive randomly throughout the day
# - Every 5 minutes the most critical patient is treated
# - Verifies higher priority patients are treated first
# ============================================================

import csv
from datetime import datetime, timedelta
from heap import MaxHeap

TREATMENT_INTERVAL = 5   # minutes between each treatment
SIMULATION_HOURS = 24


def run_simulation(patients):
    """
    Simulate a 24-hour ER operation.
    Returns a list of treatment records (dicts).
    """
    heap = MaxHeap(max_size=2000)
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    end_time = base_time + timedelta(hours=SIMULATION_HOURS)

    treatment_log = []
    arrival_index = 0
    total = len(patients)
    treatment_count = 0
    current_time = base_time

    print("=" * 70)
    print("        EMERGENCY ROOM TRIAGE — 24-HOUR SIMULATION")
    print("=" * 70)
    print(f"{'Time':<8} {'Event':<14} {'Patient ID':<12} {'Priority':<10} {'Condition'}")
    print("-" * 70)

    while current_time <= end_time:
        # Admit all patients who have arrived by current_time
        while arrival_index < total:
            arr = datetime.strptime(patients[arrival_index].arrival_time, "%Y-%m-%d %H:%M:%S")
            if arr <= current_time:
                heap.insert(patients[arrival_index])
                p = patients[arrival_index]
                print(f"{current_time.strftime('%H:%M'):<8} {'ARRIVED':<14} "
                      f"{p.patient_id:<12} {p.priority:<10} {p.condition}")
                arrival_index += 1
            else:
                break

        # Treat the most critical patient in the queue
        if not heap.is_empty():
            treated = heap.extract_max()
            treatment_count += 1
            treatment_log.append({
                "treatment_order": treatment_count,
                "treated_at": current_time.strftime("%H:%M"),
                "patient_id": treated.patient_id,
                "priority": treated.priority,
                "condition": treated.condition,
                "arrival_time": treated.arrival_time,
            })
            print(f"{current_time.strftime('%H:%M'):<8} {'>>> TREATED':<14} "
                  f"{treated.patient_id:<12} {treated.priority:<10} {treated.condition}")

        current_time += timedelta(minutes=TREATMENT_INTERVAL)

    print("=" * 70)
    print(f"\n[SIM] Simulation complete — {treatment_count} patients treated.\n")
    return treatment_log


def verify_priority_order(treatment_log, show=20):
    """Print first N treated patients to verify priority ordering."""
    print(f"{'#':<6} {'Time':<8} {'Patient':<12} {'Priority':<10} {'Visual'}")
    print("-" * 50)
    for entry in treatment_log[:show]:
        bar = "█" * entry["priority"]
        print(f"{entry['treatment_order']:<6} {entry['treated_at']:<8} "
              f"{entry['patient_id']:<12} {entry['priority']:<10} {bar}")


def save_report(treatment_log, filepath="treatment_report.csv"):
    """Save treatment log to CSV."""
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "treatment_order", "treated_at", "patient_id",
            "priority", "condition", "arrival_time"
        ])
        writer.writeheader()
        writer.writerows(treatment_log)
    print(f"[SIM] Treatment report saved → {filepath}")
