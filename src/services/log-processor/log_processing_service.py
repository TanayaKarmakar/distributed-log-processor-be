from watchdog.events import FileSystemEventHandler
from log_entry import LogEntry
import os
import re
import json

class LogFileHandler(FileSystemEventHandler):
    """Handler for file system events on log files."""

    def __init__(self, collector, regex_patterns=None):
        """Initialize with a reference to the log collector."""
        self.collector = collector
        # Keep track of file positions to detect new content
        self.file_positions = {}
        self.regex_patterns = [re.compile(p) for p in regex_patterns] if regex_patterns else None

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Process changes in the file
        self._process_file_changes(event.src_path)

    def output_parsed_log(self, parsed_log, source_file):
        """Output the parsed log to a JSON file or another destination"""

        # Add source file information
        parsed_log['source_file'] = os.path.basename(source_file)

        # In a real system, you might:
        # 1. Send to Kafka or other message queue
        # 2. Write to a database
        # 3. Send to a central logging service like Elasticsearch

        # For this demo, we'll write to a JSON file
        output_dir = os.path.join(os.path.dirname(source_file), 'parsed')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir,
                                   f"parsed_{os.path.basename(source_file)}.json")

        # Append to the file
        with open(output_file, 'a') as f:
            f.write(json.dumps(parsed_log) + '\n')

        print(f"Parsed log from {source_file}: {json.dumps(parsed_log)[:100]}...")

    def _process_file_changes(self, file_path):
        """Process changes in a log file by reading new content."""
        # Get the last position we read from this file
        last_position = self.file_positions.get(file_path, 0)

        print(f"Regex patterns: {self.regex_patterns if self.regex_patterns else 'None'}")


        try:
            with open(file_path, 'r') as f:
                # Move to where we last read
                f.seek(last_position)

                # Read new lines
                new_lines = f.readlines()

                # If we have new content
                if new_lines :
                    for line in new_lines:
                        line = line.strip()
                        if self.regex_patterns and not any(p.search(line) for p in self.regex_patterns):
                            continue

                        if line:  # Skip empty lines
                            # Create and process log entry
                            fmt = "plain"
                            try:
                                json.loads(line)
                                fmt = "json"
                            except json.JSONDecodeError:
                                pass

                            entry = LogEntry(
                                content=line,
                                source=os.path.basename(file_path),
                                fmt=fmt
                            )
                            self.collector.process_entry(entry)

                # Remember position for next time
                self.file_positions[file_path] = f.tell()

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
