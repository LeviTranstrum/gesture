FROM python:3.12-slim

# Copy your application code into the container
WORKDIR /app
COPY . .

# Install dependencies if needed
RUN pip install --no-cache-dir -r requirements.txt # Add relevant packages

# Ensure your container can access the shared library
# The library itself isn't copied — it's mounted at runtime.
CMD ["python", "finger_counter.py"]
