# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by rembg & Pillow
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file separately for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure upload folder exists
RUN mkdir -p static/uploads

# Expose port 8080
EXPOSE 8080

# Start Gunicorn with optimized settings
CMD ["gunicorn", "--workers", "1", "--threads", "2", "--timeout", "300", "--log-level", "debug", "--bind", "0.0.0.0:8080", "application:application"]
