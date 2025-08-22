import os
import time
from datetime import datetime

def main():
    """
    Simple logger service to verify that our environment is set up correctly.
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    print("Logger service started with log level:", log_level)

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Logger service is running. This will be part of our distributed system!")
        time.sleep(5)

if __name__ == "__main__":
    main()
