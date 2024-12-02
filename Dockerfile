# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application code
COPY app/ app/
COPY tests/ tests/
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run tests (build-time testing)
RUN python -m unittest discover -s tests -p "*.py"

# Set the entry point for the application
COPY run.sh run.sh
RUN chmod +x run.sh

# entry point for the application
CMD ["python", "app/publisher.py"]
