# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Instalar dependências básicas
RUN apt-get update && apt-get install -y curl

#Necessario para o conector do SQL Server
RUN apt update && apt install -y unixodbc

# Copy the requirements file into the container
COPY requirements.txt .

# Instalar biblioteca uv
RUN pip3 install uv

# Instalar as dependências listadas no requirements.txt
RUN uv pip install --system -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]