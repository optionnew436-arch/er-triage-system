# ============================================================
# heap.py — Max-Heap Implementation
# Zero-based array indexing:
#   Parent(i)     = (i - 1) // 2
#   LeftChild(i)  = 2 * i + 1
#   RightChild(i) = 2 * i + 2
# ============================================================

from patient import Patient


class MaxHeap:
    def __init__(self, max_size=2000):
        # Fixed-size array to store Patient objects
        self.heap = [None] * max_size
        self.size = 0
        self.max_size = max_size

    # ── Index Helpers ──────────────────────────────────────

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # ── Core Operations ────────────────────────────────────

    def is_empty(self):
        """O(1) — Returns True if heap has no patients."""
        return self.size == 0

    def insert(self, patient):
        """
        O(log n) — Insert a new patient into the heap.
        1. Place patient at the next available index (end of array)
        2. Bubble up: swap with parent while priority > parent priority
        """
        if self.size >= self.max_size:
            print("[HEAP] Full — cannot insert more patients.")
            return

        self.heap[self.size] = patient
        i = self.size
        self.size += 1

        # Bubble up to restore max-heap property
        while i > 0 and self.heap[self._parent(i)].priority < self.heap[i].priority:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def extract_max(self):
        """
        O(log n) — Remove and return the highest priority patient.
        1. Save root (max element)
        2. Move last element to root
        3. Reduce size, then heapify down
        """
        if self.is_empty():
            return None

        max_patient = self.heap[0]

        # Replace root with last element
        self.size -= 1
        self.heap[0] = self.heap[self.size]
        self.heap[self.size] = None

        # Restore heap property from root downward
        self._max_heapify(0)

        return max_patient

    def increase_priority(self, patient_id, new_priority):
        """
        O(n + log n) — Update a patient's priority if condition worsens.
        Searches for patient then bubbles up.
        """
        index = -1
        for i in range(self.size):
            if self.heap[i].patient_id == patient_id:
                index = i
                break

        if index == -1:
            print(f"[HEAP] Patient {patient_id} not found.")
            return False

        if new_priority <= self.heap[index].priority:
            print(f"[HEAP] New priority must be greater than current ({self.heap[index].priority}).")
            return False

        self.heap[index].priority = new_priority

        # Bubble up
        while index > 0 and self.heap[self._parent(index)].priority < self.heap[index].priority:
            self._swap(index, self._parent(index))
            index = self._parent(index)

        print(f"[HEAP] {patient_id} priority updated to {new_priority}.")
        return True

    def peek(self):
        """O(1) — View highest priority patient without removing."""
        return self.heap[0] if not self.is_empty() else None

    # ── Supporting Functions ───────────────────────────────

    def _max_heapify(self, i):
        """
        O(log n) — Push element at index i downward to restore heap property.
        Compares with left and right children, swaps with largest.
        """
        largest = i
        left = self._left(i)
        right = self._right(i)

        if left < self.size and self.heap[left].priority > self.heap[largest].priority:
            largest = left

        if right < self.size and self.heap[right].priority > self.heap[largest].priority:
            largest = right

        if largest != i:
            self._swap(i, largest)
            self._max_heapify(largest)

    def build_max_heap(self, patients):
        """
        O(n) — Build a max-heap from an unsorted list of patients.
        Starts heapifying from the last non-leaf node upward.
        This is O(n) because lower-level nodes do less work than upper ones.
        """
        self.size = len(patients)
        for i in range(self.size):
            self.heap[i] = patients[i]

        # Last non-leaf node index = floor(n/2) - 1
        start = (self.size // 2) - 1
        for i in range(start, -1, -1):
            self._max_heapify(i)

    def get_all(self):
        """Return all current patients in the heap as a list."""
        return [self.heap[i] for i in range(self.size)]
