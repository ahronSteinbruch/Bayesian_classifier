# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Declare a build-time argument
ARG SERVICE_PATH

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the specific service directory into the container
# This uses the build argument passed from docker-compose
COPY ${SERVICE_PATH} /app/${SERVICE_PATH}

# The command to run the application will be provided by Docker Compose
# This makes our Dockerfile flexible and reusable for all services.
# The host 0.0.0.0 is crucial to expose the app outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]