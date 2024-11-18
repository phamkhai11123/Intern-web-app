# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

RUN pip install pydantic-settings
# Install any needed dependencies
RUN pip install -r requirements.txt

ENV DATABASE_URL=postgres://postgres:admin@172.23.224.1:5433/fastapi
# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Define the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
