from watchdog.events import FileSystemEventHandler
from log_entry import LogEntry
import os
import re

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
        self._process_file_changes(event.src_path, self.regex_patterns)

    def _process_file_changes(self, file_path, regex=None):
        """Process changes in a log file by reading new content."""
        # Get the last position we read from this file
        last_position = self.file_positions.get(file_path, 0)

        if regex:
            regex = [re.compile(p) for p in regex]

        print(f"Regex patterns: {regex if regex else 'None'}")

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
                        if regex and not any(p.search(line) for p in regex):
                            continue

                        if line:  # Skip empty lines
                            # Create and process log entry
                            entry = LogEntry(
                                content=line,
                                source=os.path.basename(file_path)
                            )
                            self.collector.process_entry(entry)

                # Remember position for next time
                self.file_positions[file_path] = f.tell()

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
