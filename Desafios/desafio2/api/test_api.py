# Importando as bibliotecas necessárias
import requests
import json

# URL da sua API rodando localmente (se estiver usando Docker, pode ser diferente)
API_URL = "http://127.0.0.1:5000/predict"

# --- Cenário 1: Cliente com Histórico e Alta Propensão ---
# Este cliente deve existir na sua base de recomendações.
# Os dados de histórico são altos para forçar uma probabilidade alta.
# **AÇÃO**: Troque 'Cliente_VIP_123' por um ID de cliente real do seu CSV para ver uma recomendação personalizada.
cliente_vip = {
    "fk_contact": "Cliente_VIP_123",
    "datetime": "2024-04-01T10:00:00",
    "gmv_success": 150.50,
    "total_tickets_quantity_success": 2,
    "gasto_medio_acumulado": 120.0,
    "qtd_compras_acumulada": 10,
    "gasto_max_acumulado": 200.0,
    "media_intervalo_compras": 15.0,
    "std_intervalo_compras": 5.0
}

# --- Cenário 2: Cliente Novo (Cold Start) e Alta Propensão ---
# Este cliente NÃO deve existir na sua base de recomendações.
# Os dados de histórico são de um cliente novo, mas com uma compra recente de valor alto.
cliente_novo = {
    "fk_contact": "Cliente_Novo_456",
    "datetime": "2024-04-01T12:30:00",
    "gmv_success": 250.0,
    "total_tickets_quantity_success": 1,
    "gasto_medio_acumulado": 250.0,
    "qtd_compras_acumulada": 1,
    "gasto_max_acumulado": 250.0,
    "media_intervalo_compras": 0.0, # Primeira compra
    "std_intervalo_compras": 0.0    # Primeira compra
}

# --- Cenário 3: Cliente com Baixa Propensão de Compra ---
# Dados de um cliente que comprou há muito tempo e gastou pouco.
# Esperamos que a probabilidade seja baixa e os dias_preditos sejam -1.0.
cliente_inativo = {
    "fk_contact": "Cliente_Inativo_789",
    "datetime": "2022-01-15T15:00:00",
    "gmv_success": 30.0,
    "total_tickets_quantity_success": 1,
    "gasto_medio_acumulado": 30.0,
    "qtd_compras_acumulada": 1,
    "gasto_max_acumulado": 30.0,
    "media_intervalo_compras": 0.0,
    "std_intervalo_compras": 0.0
}

def testar_endpoint(cenario, dados_cliente):
    """Função para enviar a requisição e imprimir o resultado de forma organizada."""
    print(f"--- TESTANDO CENÁRIO: {cenario} ---")
    try:
        response = requests.post(API_URL, json=dados_cliente)
        response.raise_for_status()  # Lança um erro para respostas HTTP 4xx/5xx
        
        print(f"Status Code: {response.status_code}")
        print("Resposta JSON Recebida:")
        # Imprime o JSON de forma legível
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO ao conectar com a API: {e}")
    print("-" * 40 + "\n")

# --- Executa os testes ---
if __name__ == "__main__":
    testar_endpoint("Cliente VIP com Recomendação Personalizada", cliente_vip)
    testar_endpoint("Cliente Novo com Recomendação de Fallback", cliente_novo)
    testar_endpoint("Cliente Inativo com Baixa Probabilidade", cliente_inativo)