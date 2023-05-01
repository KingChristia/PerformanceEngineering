# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy your Python file and requirements (if any) into the container
COPY Task3/Exercise/ProductionLine.py ./
COPY Task3/Exercise/DocumentWriter.py ./
COPY Task3/Exercise/requirements.txt ./

# Install any necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run your Python script when the container starts
CMD ["python", "ProductionLine.py"]
