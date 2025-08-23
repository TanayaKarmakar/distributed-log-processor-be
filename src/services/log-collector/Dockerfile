FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the log collector script
COPY log_collector.py .
COPY log_file_watcher.py .
COPY log_file_handler.py .
COPY log_entry.py .
COPY log_collector_main.py .

# Create directories for logs
RUN mkdir -p /app/logs /app/collected_logs

# Set default command
ENTRYPOINT ["python", "log_collector_main.py"]
CMD ["--log-files", "/app/logs/app.log", "--output-dir", "/app/collected_logs", "--regex", "ERROR"]