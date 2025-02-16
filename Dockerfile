# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create the directory for the Unix socket
RUN mkdir -p /run/fastapi
RUN chmod 777 /run/fastapi  # Allow FastAPI & Nginx to access the socket

# Set Gunicorn to use the Unix socket
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "unix:/run/fastapi/fastapi.sock", "main:app"]
