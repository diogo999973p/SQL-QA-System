# Usar uma imagem oficial do Ubuntu
FROM ubuntu:20.04

# Definir o diretório de trabalho no container
WORKDIR /notebooks

# Instalar dependências básicas (python, pip e outras dependências)
RUN apt-get update && apt-get install -y python3-pip python3-dev curl

# Instalar dependências usadas pelo torchvision
# RUN apt-get install libjpeg-dev zlib1g-dev libpython3-dev

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

# Comando para rodar o Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8000", "--no-browser", "--allow-root"]