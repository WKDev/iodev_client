FROM python:3.12-slim

WORKDIR /app

COPY . /app

COPY requirements.txt ./

# Install the Python dependencies
RUN apt-get update && apt-get install -y \
    python3-dev libgpiod2 gcc \ 
    python3-rpi.gpio \ 
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install RPi.GPIO gpiozero

# Set the entrypoint to run your Python scripts
ENTRYPOINT ["python3", "main.py"]