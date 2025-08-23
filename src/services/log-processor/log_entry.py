import time
import json

class LogEntry:
    """Represents a structured log entry from a log file."""

    def __init__(self, content, source, timestamp=None, fmt = "plain"):
        self.content = content
        self.source = source
        # Use current time if no timestamp provided
        self.timestamp = timestamp or time.time()
        self.parsed = None
        self.fmt = fmt


        if fmt == "json":
            try:
                self.parsed = json.loads(content)
            except json.JSONDecodeError:
                self.parsed = None
                self.fmt = "plain"


    def to_dict(self):
        """Convert log entry to dictionary for serialization."""
        return {
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp
        }

    def __str__(self):
        """String representation of log entry."""
        return f"[{self.source}] {self.content}"