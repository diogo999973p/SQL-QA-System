# Agente de SQL

Esse repositório contém o código de um agente de SQL que se conecta a um banco de dados e responde perguntas de usuários sobre uma base dados relacional através do input em uma interface gráfica web.

TODO colocar imagem de um resultado do sistema.

## Projeto

Aqui estão enunciados alguns detalhes do projeto.

### Objetivo

Produzir um agente de IA que seja capaz de responder perguntas de funcionários de uma empresa com base em um banco de dados (Data Warehouse).​

### Fluxo do Sistema de IA

O sistema deve ser capaz de receber uma pergunta do usuário e identificar através dos detalhes de uma base de dados, quais tabelas e colunas são necessárias para respondê-la. 

O modelo saberá assim gerar uma query SQL, que deve ser executada no banco de dados, retornando a informação desejada.

No último passo o modelo irá, a partir da pergunta inicial e do retorno do resultando da consulta ao banco, gerar a resposta final para a pergunta do usuário.

Um fluxo pode ser visto na imagem:

![fluxo](fluxo_sistema.png)

### Stack

A stack escolhida foi:

1. Python: linguagem de programação
   - Flask: framework para geração do web server com interface gráfica para interação com o LLM.
   - Jupyter notebook: para testes diversos das funcionalidades do sistema.
   - Dataset: biblioteca para conexão e execução de comandos no banco de dados
   - OpenAI SDK: biblioteca da OpenAI usada para interações com diversos LLMs.
2. SQL Server: tipo de banco de dados SQL escolhido para guardar a dados da base de dados bikeStores.
3. OpenRouter API: plataforma de APIs para interagir com diversos modelos gratuitos e pagos.
4. DeepSeek R1 free: modelo LLM utilizado pelo sistema.


Dessa forma, o sistema funcionará dessa forma:

1. Back-end: Flask, OpenAI SDK e Dataset.
2. Front-end: html e javascript.
3. Persistência de dados: SQL Server.
4. Serviços externos: OpenRouter API.

### Organização dos Serviços

Todos os testes e desenvolvimentos foram efetuados utilizado o Docker, através da construção de serviços no Docker Compose.

Os serviços criados e suas utilizações foram:

1. Jupyter: serviço usado para subir em localhost jupyter notebooks com as bibliotecas necessárias instaladas. Esse serviço foi utilizado apenas para testes.
2. Sqlserver: serviço do banco de dados SQL Server em localhost.
3. Mssqltools: serviço temporário para criação da base de dado no SQL Server.
4. Flask: serviço principal que integra os sistemas anteriores. Possuindo uma interface gráfica e um servidor em localhost.

### Base de Dados

A base de dados escolhida foi uma com dados de uma loja de bicicletas denominada "bikeStores".

Na seguinte imagem é possível ver as tabelas presentes nesse banco de dados:

![banco](database.png)

Para que o modelo pudesse saber detalhes da configuração do banco de dados, foi criar um prompt que está localizado no arquivo services/flas/app/model.py.

### Testes Efetuados

Na pasta jupyter_data, estão os notebooks utilizados para construir e testar as funcionalidades do sistema.

1. Testes de conexão com o banco de dados SQL Server: database_connection.ipynb.
2. Testes com a API do Open Router: open_router.ipynb.
3. Teste do fluxo completo: integrated_test.ipynb.

Foram construídas duas classes principais: a Database, para conectar e executar comandos no banco de dados, e a Model para interagir com o modelo de linguagem.

## Resultados

A avaliação do sistema se baseou em testes do funcionamento completo do sistema, isto é, a inserção da pergunta pelo usuário, a geração das queries (podendo ser mais de uma) pelo modelo, a conexão com o banco e a execução dessas queries, e por fim, o recebimento pelo LLM da pergunta inicial e da resposta do banco, gerando a resposta final.

O arquivo questions_and_answers.txt, contém os testes efetuados e as análises dos resultados.

O único erro cometido pelo modelo foi pelo fato da base de dados possuir uma tabela de produtos com produtos de diferentes ids, mas com mesmo nome. Dessa forma, agrupar pelo ID gera um resultado diferente de agrupar pelo nome.

O agrupamento do modelo pelo ID não necessáriamente é uma falha do modelo, podendo indicar uma falha da construção da própria base de dados. Porém, caso o modelo tivesse conhecimento disso, através de uma query SELECT, ele poderia ter gerado o resultado correto.

Uma possível correção seria uma avaliação completa do modelo de todo o banco de dados, antes dele receber qualquer pergunta. Isto é, o modelo poderia gerar queries automáticas de avaliação para gerar um conhecimento das especificidades das informações do banco de dados. Porém, essa avaliação seria muito complicada para o caso de base de dados muito grandes, com milhões de linhas, e talvez pequenas amostras não evidenciassem os importantes detalhes das informações. 

Uma solução para esse problema seria a geração de um prompt para explicar os detalhes da base e qualquer informações que vá ajudar o modelo a chegar na resposta correta.

## Conclusão