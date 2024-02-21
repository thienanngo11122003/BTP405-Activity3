# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source code to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir pyodbc

# Expose port
EXPOSE 8000

# Command to run the server
CMD ["python", "api.py"]
