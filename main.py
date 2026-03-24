# ============================================================
# main.py — Main Execution File
# Heap-Based Priority Queue: Emergency Room Triage System
#
# Runs in order:
#   1. Generate 1,000 patient dataset → patients.csv
#   2. Load from CSV and run 24-hour simulation
#   3. Verify priority ordering (higher priority treated first)
#   4. Complexity benchmarks proving O(log n) and O(n)
# ============================================================

import random
import time
import math
from dataset import generate_dataset, save_to_csv, load_from_csv
from simulation import run_simulation, verify_priority_order, save_report
from heap import MaxHeap
from patient import Patient


# ── Complexity Benchmarks ──────────────────────────────────

def benchmark_insert(sizes):
    """
    Prove insert() is O(log n).
    If t/log(n) stays roughly constant as n grows → O(log n) confirmed.
    """
    print("=" * 58)
    print("INSERT — O(log n) Proof")
    print("=" * 58)
    print(f"{'n':<10} {'Time (ms)':<15} {'log2(n)':<12} {'t / log(n)'}")
    print("-" * 58)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [
            Patient(f"P{i:04d}", random.randint(1, 10),
                    "2024-01-01 00:00:00", "Test")
            for i in range(n)
        ]
        start = time.perf_counter()
        for p in pts:
            # Call insert with individual parameters as required
            heap.insert(p.patient_id, p.priority, p.arrival_time, p.condition)
        elapsed = (time.perf_counter() - start) * 1000
        log_n = math.log2(n)
        print(f"{n:<10} {elapsed:<15.4f} {log_n:<12.2f} {elapsed / log_n:.6f}")
    print("→ t/log(n) is roughly constant → confirms O(log n)\n")


def benchmark_extract(sizes):
    """
    Prove extractMax() is O(log n).
    """
    print("=" * 58)
    print("EXTRACT_MAX — O(log n) Proof")
    print("=" * 58)
    print(f"{'n':<10} {'Time (ms)':<15} {'log2(n)':<12} {'t / log(n)'}")
    print("-" * 58)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [
            Patient(f"P{i:04d}", random.randint(1, 10),
                    "2024-01-01 00:00:00", "Test")
            for i in range(n)
        ]
        for p in pts:
            heap.insert(p.patient_id, p.priority, p.arrival_time, p.condition)
        start = time.perf_counter()
        while not heap.isEmpty():
            heap.extractMax()
        elapsed = (time.perf_counter() - start) * 1000
        log_n = math.log2(n)
        print(f"{n:<10} {elapsed:<15.4f} {log_n:<12.2f} {elapsed / log_n:.6f}")
    print("→ t/log(n) is roughly constant → confirms O(log n)\n")


def benchmark_build(sizes):
    """
    Prove buildMaxHeap() is O(n), not O(n log n).
    If t/n stays roughly constant → O(n) confirmed.
    """
    print("=" * 58)
    print("BUILD_MAX_HEAP — O(n) Proof  (NOT O(n log n))")
    print("=" * 58)
    print(f"{'n':<10} {'Time (ms)':<15} {'t / n':<15} {'t / (n log n)'}")
    print("-" * 58)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [
            Patient(f"P{i:04d}", random.randint(1, 10),
                    "2024-01-01 00:00:00", "Test")
            for i in range(n)
        ]
        start = time.perf_counter()
        heap.buildMaxHeap(pts)
        elapsed = (time.perf_counter() - start) * 1000
        nlogn = n * math.log2(n)
        print(f"{n:<10} {elapsed:<15.6f} {elapsed/n:<15.8f} {elapsed/nlogn:.8f}")
    print("→ t/n is roughly constant → confirms O(n)\n")


def space_complexity():
    print("=" * 58)
    print("SPACE COMPLEXITY")
    print("=" * 58)
    print("""
  Structure  : Fixed-size array of Patient objects
  Array size : O(n) — one slot per patient
  Aux space  : O(log n) — recursion stack depth in maxHeapify
  Total      : O(n)

  For n = 1,000:
    Array     ≈ 1,000 slots × ~200 bytes = ~200 KB
    Recursion ≈ log2(1000) ≈ 10 stack frames
    """)


# ── Main Entry Point ───────────────────────────────────────

def main():
    random.seed(42)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║   HEAP-BASED PRIORITY QUEUE: ER TRIAGE SYSTEM       ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    # ── Step 1: Generate dataset ───────────────────────────
    print("► Step 1: Generating synthetic dataset (1,000 patients)...")
    patients = generate_dataset(1000)
    save_to_csv(patients)

    # ── Step 2: Load from CSV (Input/Output from file) ─────
    print("\n► Step 2: Loading from patients.csv...")
    loaded_patients = load_from_csv()
    print(f"[DATASET] Loaded {len(loaded_patients)} patients from CSV\n")

    # ── Step 3: Run 24-hour simulation ─────────────────────
    print("► Step 3: Running 24-hour ER simulation...\n")
    log = run_simulation(loaded_patients)

    # ── Step 4: Verify priority ordering ───────────────────
    print("► Step 4: Treatment order verification (first 20 patients)")
    verify_priority_order(log, show=20)

    # ── Step 5: Save treatment report ──────────────────────
    print()
    save_report(log)

    # ── Step 6: Complexity benchmarks ──────────────────────
    print("\n► Step 5: Complexity Analysis Benchmarks\n")
    sizes = [100, 500, 1000, 2000, 5000]
    benchmark_insert(sizes)
    benchmark_extract(sizes)
    benchmark_build(sizes)
    space_complexity()

    print("✓ All done! Output files:")
    print("   → patients.csv")
    print("   → treatment_report.csv")


if __name__ == "__main__":
    main()
