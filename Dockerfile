FROM python:3.11-slim

LABEL maintainer="NeuralSynthesia"
LABEL description="AI-Powered Interactive Storybook Generator"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create results directory
RUN mkdir -p results

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]