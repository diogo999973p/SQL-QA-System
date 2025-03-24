# Usar uma imagem oficial do Ubuntu
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Instalar dependências básicas (python, pip e outras dependências)
RUN apt-get update && apt-get install -y python3-pip python3-dev curl

#Necessario para o conector do SQL Server
RUN apt update && apt install -y unixodbc

# Entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Copia script de instalação do driver
COPY driver.sh /usr/local/bin/driver.sh

# Permissões nos arquivos
RUN chmod +x /usr/local/bin/driver.sh /usr/local/bin/entrypoint.sh

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

# Run the script when the container starts
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]