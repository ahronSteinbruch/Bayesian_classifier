# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We do this in a separate step to take advantage of Docker's layer caching.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# The command to run the application will be provided by Docker Compose
# This makes our Dockerfile flexible and reusable for all services.
# The host 0.0.0.0 is crucial to expose the app outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]