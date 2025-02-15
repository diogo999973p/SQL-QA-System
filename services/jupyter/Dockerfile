# Usar uma imagem oficial do Ubuntu
FROM ubuntu:20.04

# Definir o diretório de trabalho no container
WORKDIR /notebooks

# Instalar dependências básicas (python, pip e outras dependências)
RUN apt-get update && apt-get install -y python3-pip python3-dev curl

#Necessario para o conector do SQL Server
RUN apt update && apt install -y unixodbc

# Copia script de instalação do driver
COPY driver.sh /usr/local/bin/driver.sh

# Entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Permissões nos arquivos
RUN chmod +x /usr/local/bin/driver.sh /usr/local/bin/entrypoint.sh

# Update pip
RUN pip3 install --upgrade pip 

# Instalar biblioteca uv
RUN pip3 install uv

# Instalar o Jupyter Lab e outras dependências
COPY requirements.txt .

# Instalar as dependências listadas no requirements.txt
RUN uv pip install --system -r requirements.txt

# Expor a porta do Jupyter Notebook
EXPOSE 8000

# Run the script when the container starts
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]