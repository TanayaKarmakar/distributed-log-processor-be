from watchdog.observers import Observer
import os
import time
from log_collector import LogCollector
from log_file_handler import LogFileHandler

def watch_log_files(log_paths, regex_pattern=None, output_dir="./collected_logs"):
    """
        Watch the specified log files for changes.

        Args:
            log_paths: List of paths to log files to watch
            output_dir: Directory to save collected logs
            :param output_dir:
            :param log_paths:
            :param regex:
        """
    if regex_pattern is None:
        regex_pattern = ['WARN']
    print(f"Starting log collector. Watching {len(log_paths)} files.")
    print(f"Output directory: {output_dir}")
    print(f"Regex filter: {regex_pattern if regex_pattern else ['WARN']}")

    # Initialize the collector and event handler
    collector = LogCollector(output_dir)
    event_handler = LogFileHandler(collector,regex_patterns=regex_pattern)

    # Set up the observer
    observer = Observer()

    # Add watchers for each log file's directory
    for log_path in log_paths:
        if not os.path.exists(log_path):
            print(f"Warning: Log file {log_path} does not exist yet.")

        # Get the directory containing the log file
        directory = os.path.dirname(log_path) or '.'

        # Schedule the directory for watching
        observer.schedule(event_handler, directory, recursive=False)

        # Initial read of existing content
        if os.path.exists(log_path) and os.path.isfile(log_path):
            event_handler._process_file_changes(log_path, regex_pattern)

    # Start the observer
    observer.start()

    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
            # Every 10 seconds, flush buffer even if not full
            if time.time() % 10 < 1 and collector.buffer:
                collector.flush_buffer()

    except KeyboardInterrupt:
        # Stop the observer gracefully
        observer.stop()

    # Wait for the observer thread to finish
    observer.join()

    # Final flush of any remaining entries
    collector.flush_buffer()

    print(f"Log collector stopped. Collected {collector.collected_count} entries.")
