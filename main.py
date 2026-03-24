# ============================================================
# main.py — Main Execution File
# Runs the full ER Triage System:
#   1. Generate dataset
#   2. Run 24-hour simulation
#   3. Verify priority ordering
#   4. Complexity benchmarks
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
    print("=" * 55)
    print("INSERT — O(log n) Proof")
    print("=" * 55)
    print(f"{'n':<10} {'Time (ms)':<15} {'log2(n)':<12} {'t / log(n)'}")
    print("-" * 55)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [Patient(f"P{i}", random.randint(1, 10), "2024-01-01 00:00:00", "Test") for i in range(n)]
        start = time.perf_counter()
        for p in pts:
            heap.insert(p)
        elapsed = (time.perf_counter() - start) * 1000
        log_n = math.log2(n)
        print(f"{n:<10} {elapsed:<15.4f} {log_n:<12.2f} {elapsed / log_n:.6f}")


def benchmark_extract(sizes):
    print("\n" + "=" * 55)
    print("EXTRACT_MAX — O(log n) Proof")
    print("=" * 55)
    print(f"{'n':<10} {'Time (ms)':<15} {'log2(n)':<12} {'t / log(n)'}")
    print("-" * 55)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [Patient(f"P{i}", random.randint(1, 10), "2024-01-01 00:00:00", "Test") for i in range(n)]
        for p in pts:
            heap.insert(p)
        start = time.perf_counter()
        while not heap.is_empty():
            heap.extract_max()
        elapsed = (time.perf_counter() - start) * 1000
        log_n = math.log2(n)
        print(f"{n:<10} {elapsed:<15.4f} {log_n:<12.2f} {elapsed / log_n:.6f}")


def benchmark_build(sizes):
    print("\n" + "=" * 55)
    print("BUILD_MAX_HEAP — O(n) Proof")
    print("=" * 55)
    print(f"{'n':<10} {'Time (ms)':<15} {'t / n'}")
    print("-" * 55)
    for n in sizes:
        heap = MaxHeap(max_size=n + 10)
        pts = [Patient(f"P{i}", random.randint(1, 10), "2024-01-01 00:00:00", "Test") for i in range(n)]
        start = time.perf_counter()
        heap.build_max_heap(pts)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{n:<10} {elapsed:<15.6f} {elapsed / n:.8f}")


# ── Main ───────────────────────────────────────────────────

def main():
    random.seed(42)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║   HEAP-BASED PRIORITY QUEUE: ER TRIAGE SYSTEM       ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    # Step 1: Generate and save dataset
    print("► Step 1: Generating dataset (1,000 patients)...")
    patients = generate_dataset(1000)
    save_to_csv(patients)

    # Step 2: Load from CSV and run simulation
    print("\n► Step 2: Running 24-hour ER simulation...\n")
    loaded_patients = load_from_csv()
    log = run_simulation(loaded_patients)

    # Step 3: Verify priority ordering
    print("\n► Step 3: Treatment order verification (first 20 patients)\n")
    verify_priority_order(log, show=20)

    # Step 4: Save treatment report
    print()
    save_report(log)

    # Step 5: Complexity benchmarks
    print("\n► Step 4: Complexity Analysis Benchmarks\n")
    sizes = [100, 500, 1000, 2000, 5000]
    benchmark_insert(sizes)
    benchmark_extract(sizes)
    benchmark_build(sizes)

    print("\n✓ All done! Output files:")
    print("   → er_triage_system/patients.csv")
    print("   → er_triage_system/treatment_report.csv")


if __name__ == "__main__":
    main()
