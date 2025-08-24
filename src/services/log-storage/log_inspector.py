import os
import gzip
import bz2
import lzma

class LogInspector:
    def __init__(self, logs_dir):
        self.logs_dir = logs_dir

    def _open_file(self, file_path):
        """Open plain or compressed log files transparently."""
        if file_path.endswith(".gz"):
            return gzip.open(file_path, "rt", encoding="utf-8", errors="ignore")
        elif file_path.endswith(".bz2"):
            return bz2.open(file_path, "rt", encoding="utf-8", errors="ignore")
        elif file_path.endswith(".xz"):
            return lzma.open(file_path, "rt", encoding="utf-8", errors="ignore")
        else:
            return open(file_path, "r", encoding="utf-8", errors="ignore")

    def display_logs(self):
        if not os.path.exists(self.logs_dir):
            print(f"Logs directory '{self.logs_dir}' does not exist.")
            return

        log_files = [
            f for f in os.listdir(self.logs_dir)
            if f.endswith((".log", ".log.gz", ".log.bz2", ".log.xz"))
        ]
        if not log_files:
            print("No log files found.")
            return

        for log_file in log_files:
            file_path = os.path.join(self.logs_dir, log_file)
            print(f"\n--- Contents of {log_file} ---")
            with self._open_file(file_path) as file:
                print(file.read())

    def search_text_within_logs(self, search_text):
        if not os.path.exists(self.logs_dir):
            print(f"Logs directory '{self.logs_dir}' does not exist.")
            return

        log_files = [
            f for f in os.listdir(self.logs_dir)
            if f.endswith((".log", ".log.gz", ".log.bz2", ".log.xz"))
        ]
        if not log_files:
            print("No log files found.")
            return

        found = False
        for log_file in log_files:
            file_path = os.path.join(self.logs_dir, log_file)
            with self._open_file(file_path) as file:
                for line_number, line in enumerate(file, start=1):
                    if search_text in line:
                        if not found:
                            print(f"\n--- Search results for '{search_text}' ---")
                            found = True
                        print(f"{log_file} (Line {line_number}): {line.strip()}")

        if not found:
            print(f"No occurrences of '{search_text}' found in log files.")


if __name__ == "__main__":
    logs_directory = "./logs"  # Adjust the path as needed
    inspector = LogInspector(logs_directory)

    # Display all logs
    inspector.display_logs()

    # Search for specific text within logs
    search_query = "ERROR"  # Adjust the search text as needed
    inspector.search_text_within_logs(search_query)