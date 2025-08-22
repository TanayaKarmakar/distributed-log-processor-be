FROM python:3.9-slim

WORKDIR /app

# Copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables (default values can be overridden at runtime)
ENV LOG_LEVEL=ERROR
ENV LOG_FREQUENCY=10
ENV LOG_FORMAT="[%(asctime)s] [%(levelname)s] %(message)s"
ENV LOG_FILE="logs/my_app.log"

# Run the application
ENTRYPOINT ["python", "-u"]
CMD ["app.py"]