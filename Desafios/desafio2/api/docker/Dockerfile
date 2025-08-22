# 1. Imagem Base Segura
FROM python:3.11.5-slim-bookworm

# 2. Atualizações de Segurança
RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# 3. Diretório de Trabalho
WORKDIR /app

# 4. Copiar Arquivos de Dependências
COPY Desafios/desafio2/api/requirements.txt .

# 5. Instalar Dependências
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar os Modelos e o Código da Aplicação
# CORREÇÃO: Aponta para o caminho exato da sua pasta de modelos
COPY Desafios/desafio2/api/modelos/ ./modelos/
# CORREÇÃO: Copia todos os arquivos .py da pasta api
COPY Desafios/desafio2/api/*.py ./

# 7. Expor a Porta
EXPOSE 5000

# 8. Comando de Execução
CMD ["python", "-u", "app.py"]