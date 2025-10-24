# Use NVIDIA CUDA base image with Python
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create symlink for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy minimal requirements
COPY requirements-minimal.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project structure
COPY src/ ./src/
COPY util/ ./util/
COPY weights/ ./weights/
COPY handler.py .
COPY .env .

# Pre-download models (optional, speeds up first run)
RUN python -c "from transformers import AutoProcessor; \
    AutoProcessor.from_pretrained('microsoft/Florence-2-base', trust_remote_code=True); \
    print('✅ Florence-2 processor cached')" || echo "⚠️  Model download skipped"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import torch; print('OK')" || exit 1

# Run the handler
CMD ["python", "handler.py"]