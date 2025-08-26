# 1. Usar uma imagem base oficial do Python
FROM python:3.11.5-slim-bookworm

# 2. Atualizar pacotes do sistema
RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# 3. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 4. Copiar o arquivo de dependências
# CORREÇÃO: O caminho agora é relativo à pasta 'api'
COPY requirements.txt .

# 5. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar os Modelos, Dados e o Código da Aplicação
# CORREÇÃO: Os caminhos agora são relativos à pasta 'api'
COPY ./modelos/ ./modelos/
COPY ./data/ ./data/
COPY app.py .

# 7. Expor a porta que a aplicação vai usar
EXPOSE 5000

# 8. Comando para rodar a aplicação quando o container iniciar
CMD ["python", "app.py"]