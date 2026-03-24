# ============================================================
# dataset.py — Synthetic Patient Dataset Generator
# Generates 1,000 patients with random priorities & arrival times
# Output: patients.csv
# ============================================================

import random
import csv
from datetime import datetime, timedelta
from patient import Patient

random.seed(42)

# Priority to condition mapping (1=least critical, 10=most critical)
CONDITION_MAP = {
    10: "Cardiac Arrest",
    9:  "Severe Trauma",
    8:  "Stroke",
    7:  "Respiratory Failure",
    6:  "Severe Bleeding",
    5:  "Broken Bone",
    4:  "High Fever",
    3:  "Moderate Pain",
    2:  "Minor Laceration",
    1:  "Common Cold",
}


def generate_dataset(n=1000):
    """Generate n synthetic patients spread across a 24-hour window."""
    patients = []
    base_time = datetime(2024, 1, 1, 0, 0, 0)

    for i in range(1, n + 1):
        patient_id = f"P{i:04d}"
        priority = random.randint(1, 10)
        # Random arrival within 24 hours (86400 seconds)
        offset = random.randint(0, 86400)
        arrival_time = (base_time + timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S")
        condition = CONDITION_MAP[priority]

        patients.append(Patient(patient_id, priority, arrival_time, condition))

    # Sort by arrival time for realistic simulation
    patients.sort(key=lambda p: p.arrival_time)
    return patients


def save_to_csv(patients, filepath="patients.csv"):
    """Save patient list to CSV file."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["patient_id", "priority", "arrival_time", "condition"])
        for p in patients:
            writer.writerow([p.patient_id, p.priority, p.arrival_time, p.condition])
    print(f"[DATASET] Saved {len(patients)} patients → {filepath}")


def load_from_csv(filepath="patients.csv"):
    """Load patients from CSV file and return list of Patient objects."""
    patients = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patients.append(Patient(
                patient_id=row["patient_id"],
                priority=int(row["priority"]),
                arrival_time=row["arrival_time"],
                condition=row["condition"]
            ))
    return patients


if __name__ == "__main__":
    data = generate_dataset(1000)
    save_to_csv(data)
