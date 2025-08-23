# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy our log parser files
COPY log_parser.py /app/
COPY log_parser_demo.py /app/
COPY log_entry.py /app/

# Make the demo script executable
RUN chmod +x /app/log_parser_demo.py

# Create a directory for logs
RUN mkdir -p /logs

# Entry point
ENTRYPOINT ["python3", "log_parser_demo.py"]