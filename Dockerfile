# Use an official Python runtime as the base image
FROM python:3.11.4-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8010 available to the world outside this container
EXPOSE 8010

# Define the command to run the application
CMD ["python3", "server.py"]
