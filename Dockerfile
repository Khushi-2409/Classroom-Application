# Use the official Python image as a base
FROM python:3.9-slim

# Install bash (or another shell if necessary)
RUN apt-get update && apt-get install -y bash

# Set the working directory in the container
WORKDIR /app

# Copy the dependency file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pytest coverage py
RUN pip install waitress

# Copy the rest of the application code
COPY . .

# Make the run.sh script executable
RUN chmod +x run.sh

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["./run.sh"]