# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project context into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the startup script executable
RUN chmod +x ./start.sh

# Expose the port the orchestrator will run on
EXPOSE 80

# Run the startup script when the container launches
CMD ["./start.sh"]