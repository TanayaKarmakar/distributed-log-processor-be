import os, json, time

class LogCollector:
    """Core class for collecting and processing log entries."""

    def __init__(self, output_dir="./collected_logs"):
        """Initialize the log collector with output directory."""
        self.output_dir = output_dir
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        self.buffer = []
        self.collected_count = 0

    def process_entry(self, entry):
        """Process a new log entry."""
        print(f"New log entry detected: {entry}")

        if entry.fmt == "json" and entry.parsed:
            print(f"Parsed JSON content: {entry.parsed}")
            log_line = f"{entry.source} :: {entry.parsed}"
        else:
            log_line = f"{entry.source} :: {entry.content}"

        self.buffer.append(log_line)
        self.collected_count += 1

        # For demonstration, we'll write every 5 entries to a file
        if len(self.buffer) >= 5:
            self.flush_buffer()

    def flush_buffer(self):
        """Write buffered entries to output file."""
        if not self.buffer:
            return

        # Create output filename based on timestamp
        output_file = os.path.join(
            self.output_dir,
            f"collected_logs_{int(time.time())}.json"
        )

        # Write entries to file
        with open(output_file, 'w') as f:
            entries_dict = [entry.to_dict() for entry in self.buffer]
            json.dump(entries_dict, f, indent=2)

        print(f"Wrote {len(self.buffer)} entries to {output_file}")
        self.buffer = []  # Clear the buffer
