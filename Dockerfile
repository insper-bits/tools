# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install git and a minimal shell (sh instead of bash to reduce footprint)
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/insper-bits/tools.git 

# Install Python dependencies from requirements.txt if it exists
RUN pip install -r tools/requirements.txt

# Set entrypoint to sh for minimal shell
ENTRYPOINT ["/bin/sh"]

