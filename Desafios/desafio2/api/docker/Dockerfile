# 1. Imagem Base
FROM python:3.11-slim

# 2. Diretório de Trabalho
WORKDIR /app

# 3. Copiar Arquivos
COPY api/requirements.txt .
# CORREÇÃO: Copia a pasta 'models' que está dentro do contexto de build
COPY models/ ./models/
# Copia o conteúdo da pasta 'api' para o diretório de trabalho do container
COPY api/ .

# 4. Instalar Dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expor a Porta
EXPOSE 5000

# 6. Comando de Execução
CMD ["python", "app.py"]