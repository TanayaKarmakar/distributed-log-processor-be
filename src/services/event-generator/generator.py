import logging
import random
import socket
import time

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

MESSAGES = [
    'User logged in successfully.',
    'File uploaded',
    'Database query failed',
    'Cache miss',
    'Payment processed',
    'Connection timeout'
]

def main():
    host = 'logger'
    port = 8000

    while True:
        try:
            with socket.create_connection((host, port)) as sock:
                log_level = random.choice(LOG_LEVELS)
                message = random.choice(MESSAGES)
                log_entry = f"{log_level}: {message}\n"
                sock.sendall(log_entry.encode('utf-8'))
                print(f"Sent: {log_entry.strip()}")
                time.sleep(random.uniform(0.5, 2.0))
        except (ConnectionRefusedError, socket.error) as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(2)

if __name__ == "__main__":
    main()

