# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container


# Copy the current directory contents into the container at /app
COPY ./apps/6 .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements/install.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI server using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]