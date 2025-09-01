# Use an official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /

# Copy the application code to the container
COPY . /

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000



