import pm4py

class LogLoader:
    """Factory class for loading event logs."""
    @staticmethod
    def load_log(file_path):
        try:
            if '.csv' not in file_path:
                log = pm4py.read_xes(file_path)
            else:
                log = pm4py.read_ocel_csv(file_path)
            print(f"Loaded {len(log)} traces from '{file_path}'.\n")
            return log
        except Exception as e:
            print(f"Error loading log file: {e}")
            raise
