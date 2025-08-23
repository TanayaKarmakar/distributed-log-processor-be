import argparse
from log_file_watcher import watch_log_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log file Collector Service")

    parser.add_argument('--log-files', nargs='+', required=True, help='Path to the log files to watch')
    parser.add_argument('--output-dir', required=True, help='Directory to store collected logs')
    #regex
    parser.add_argument('--regex', nargs='+',required=True, help='Regex pattern to filter log entries')

    # Parse arguments
    args = parser.parse_args()

    # Start watching log files
    watch_log_files(args.log_files, args.regex, args.output_dir)