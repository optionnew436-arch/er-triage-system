# ============================================================
# heap.py — Max-Heap Implementation
# Uses a fixed-size array with zero-based indexing:
#   Parent(i)     = (i - 1) // 2
#   LeftChild(i)  = 2 * i + 1
#   RightChild(i) = 2 * i + 2
# All algorithms implemented manually — no built-in heap/sort used
# ============================================================

from patient import Patient


class MaxHeap:
    def __init__(self, max_size=2000):
        # Fixed-size array — explicit array storage as required
        self.heap = [None] * max_size
        self.size = 0
        self.max_size = max_size

    # ── Index Helpers ──────────────────────────────────────

    def _parent(self, i):
        """Return parent index of node i (zero-based)"""
        return (i - 1) // 2

    def _left(self, i):
        """Return left child index of node i"""
        return 2 * i + 1

    def _right(self, i):
        """Return right child index of node i"""
        return 2 * i + 2

    def _swap(self, i, j):
        """Swap two elements in the heap array"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # ── Core Heap Operations ───────────────────────────────

    def isEmpty(self):
        """
        O(1) — Check if the priority queue is empty.
        Returns True if no patients are waiting.
        """
        return self.size == 0

    def insert(self, patientID, priority, arrival_time, condition):
        """
        O(log n) — Add a new patient with given priority.

        Steps:
        1. Create Patient object and place at end of array (index = size)
        2. Increment size
        3. Bubble up: while node > parent, swap upward
           This restores the max-heap property

        Proof of O(log n): bubble-up traverses at most height of tree = log2(n)
        """
        if self.size >= self.max_size:
            print("[HEAP] Full — cannot insert more patients.")
            return

        # Place new patient at next available position
        patient = Patient(patientID, priority, arrival_time, condition)
        self.heap[self.size] = patient
        i = self.size
        self.size += 1

        # Bubble up to restore max-heap property
        while i > 0 and self.heap[self._parent(i)].priority < self.heap[i].priority:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def extractMax(self):
        """
        O(log n) — Remove and return the highest priority patient (root).

        Steps:
        1. Save root (maximum element)
        2. Move last element to root position
        3. Decrease size
        4. Call maxHeapify(0) to restore heap property downward

        Proof of O(log n): maxHeapify traverses at most height = log2(n)
        """
        if self.isEmpty():
            return None

        # Root is always the max (highest priority)
        max_patient = self.heap[0]

        # Move last element to root and shrink heap
        self.size -= 1
        self.heap[0] = self.heap[self.size]
        self.heap[self.size] = None

        # Restore heap property from root downward
        self.maxHeapify(0)

        return max_patient

    def increasePriority(self, patientID, newPriority):
        """
        O(n + log n) — Update patient priority if condition worsens.

        Steps:
        1. Search for patient by ID — O(n)
        2. Update priority value
        3. Bubble up to restore heap property — O(log n)

        Use case: patient's condition deteriorates while waiting
        """
        index = -1
        for i in range(self.size):
            if self.heap[i].patient_id == patientID:
                index = i
                break

        if index == -1:
            print(f"[HEAP] Patient {patientID} not found in queue.")
            return False

        if newPriority <= self.heap[index].priority:
            print(f"[HEAP] New priority ({newPriority}) must be higher than "
                  f"current ({self.heap[index].priority}).")
            return False

        old_priority = self.heap[index].priority
        self.heap[index].priority = newPriority

        # Bubble up to restore max-heap property
        while index > 0 and self.heap[self._parent(index)].priority < self.heap[index].priority:
            self._swap(index, self._parent(index))
            index = self._parent(index)

        print(f"[HEAP] {patientID} priority updated: {old_priority} → {newPriority} "
              f"(condition worsened)")
        return True

    def peek(self):
        """O(1) — View highest priority patient without removing."""
        return self.heap[0] if not self.isEmpty() else None

    # ── Supporting Functions ───────────────────────────────

    def maxHeapify(self, i):
        """
        O(log n) — Maintain heap property after deletion.
        Pushes element at index i downward by swapping with largest child.

        Called after extractMax to restore the heap from root down.
        Recursively fixes violations until heap property is satisfied.
        """
        largest = i
        left  = self._left(i)
        right = self._right(i)

        # Find largest among node and its children
        if left < self.size and self.heap[left].priority > self.heap[largest].priority:
            largest = left

        if right < self.size and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        # If largest is not current node, swap and continue heapifying
        if largest != i:
            self._swap(i, largest)
            self.maxHeapify(largest)

    def buildMaxHeap(self, patients):
        """
        O(n) — Build heap from an unsorted array (for initial patient load).

        Steps:
        1. Copy all patients into the array
        2. Start from last non-leaf node: floor(n/2) - 1
        3. Call maxHeapify on each node going upward to root

        Why O(n) not O(n log n)?
        - Nodes at height h do at most O(h) work
        - Sum over all heights: Σ (n/2^h) * h = O(n)
        - Lower nodes (leaves) do zero work; upper nodes do more
        - This is more efficient than inserting one-by-one (O(n log n))
        """
        self.size = len(patients)
        for i in range(self.size):
            self.heap[i] = patients[i]

        # Start heapifying from last non-leaf node upward to root
        start = (self.size // 2) - 1
        for i in range(start, -1, -1):
            self.maxHeapify(i)

    def get_all(self):
        """Return all current patients in the heap as a list."""
        return [self.heap[i] for i in range(self.size)]
