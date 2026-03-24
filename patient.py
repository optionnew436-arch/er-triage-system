# ============================================================
# patient.py — Patient Data Structure
# ============================================================

class Patient:
    def __init__(self, patient_id, priority, arrival_time, condition):
        self.patient_id = patient_id    # Unique ID e.g. P0001
        self.priority = priority        # 1-10, 10 = most critical
        self.arrival_time = arrival_time  # datetime string
        self.condition = condition      # Medical condition description

    def __repr__(self):
        return (f"Patient(id={self.patient_id}, priority={self.priority}, "
                f"arrived={self.arrival_time}, condition={self.condition})")
