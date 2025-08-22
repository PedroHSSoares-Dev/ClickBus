# Importando as bibliotecas necessárias
import requests
import json

# URL do nosso endpoint de previsão
URL = 'http://127.0.0.1:5000/predict'

# --- DADOS DE EXEMPLO PARA UM CLIENTE ---
# Estes são os dados brutos que o nosso modelo precisa para fazer a previsão.
# Precisamos fornecer o histórico e os dados da compra atual.
dados_cliente_exemplo = {
    # Dados da compra ATUAL
    "datetime": "2025-08-21 22:30:00",
    "gmv_success": 150.75,
    "total_tickets_quantity_success": 2,
    
    # Dados do HISTÓRICO do cliente (que seriam buscados de um banco de dados)
    "data_ultima_compra": "2025-07-15 10:00:00",
    "gasto_medio_acumulado": 125.50,
    "qtd_compras_acumulada": 8,
    "gasto_max_acumulado": 250.00,
    "media_intervalo_compras": 35.5,
    "std_intervalo_compras": 10.2
}

# Converte o dicionário Python para o formato JSON
headers = {'Content-Type': 'application/json'}
data_json = json.dumps(dados_cliente_exemplo)

# Faz a requisição POST para a nossa API
print("Enviando dados para a API...")
response = requests.post(URL, data=data_json, headers=headers)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    print("\nPrevisão recebida com sucesso!")
    # Imprime o resultado retornado pela API
    print(response.json())
else:
    print(f"\nErro ao fazer a requisição. Código: {response.status_code}")
    print(response.text)
