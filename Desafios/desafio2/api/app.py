import flask
from flask import request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import json
from ast import literal_eval

app = flask.Flask(__name__)

# --- Carregamento dos Modelos e Dados ---
print("Carregando modelos e dados de recomendação...")

# Modelos do Desafio 2
model_clf = joblib.load('./modelos/xgboost_classificador_final.joblib')
model_reg = joblib.load('./modelos/xgboost_regressor_final.joblib')

# NOVO: Carrega a lista de rotas de fallback do Desafio 3
try:
    with open('./modelos/fallback_routes.json', 'r') as f:
        fallback_routes = json.load(f)
    print("Lista de rotas de fallback carregada.")
except FileNotFoundError:
    fallback_routes = []
    print("AVISO: Arquivo de fallback 'fallback_routes.json' não encontrado.")

# O caminho supõe que a pasta 'data' está no nível raiz do projeto, dois níveis acima da pasta 'api'
caminho_recomendacoes = './data/recomendacoes_completas_api.csv'
try:
    df_recomendacoes = pd.read_csv(caminho_recomendacoes)
    # Converte a coluna de string de lista para uma lista real
    df_recomendacoes['recomendacoes_rotas_top5'] = df_recomendacoes['recomendacoes_rotas_top5'].apply(literal_eval)
    # Usa fk_contact como índice para busca super rápida
    df_recomendacoes.set_index('fk_contact', inplace=True)
    print("Base de recomendações do Desafio 3 carregada.")
except FileNotFoundError:
    df_recomendacoes = None
    print(f"AVISO: Arquivo de recomendações '{caminho_recomendacoes}' não encontrado. A API usará apenas o fallback.")

print("Modelos e dados carregados com sucesso.")

# --- Listas de Features (mantidas como no seu original) ---
features_class = [
    'gmv_success', 'total_tickets_quantity_success', 'dia_da_semana', 
    'dia_do_mes', 'mes', 'ano', 'semana_do_ano', 'gasto_medio_acumulado', 
    'qtd_compras_acumulada', 'gasto_max_acumulado'
]
features_avancadas_regressor = [
    'gmv_success', 'total_tickets_quantity_success', 'dia_da_semana', 
    'dia_do_mes', 'mes', 'ano', 'semana_do_ano', 'gasto_medio_acumulado', 
    'qtd_compras_acumulada', 'gasto_max_acumulado', 'eh_feriado', 
    'eh_inicio_de_mes', 'eh_fim_de_semana', 'media_intervalo_compras', 
    'std_intervalo_compras', 'gasto_vs_media'
]

# --- Lógica de Pré-processamento e Predição (Função separada) ---
def fazer_previsao_desafio2(dados_cliente):
    df = pd.DataFrame(dados_cliente, index=[0])
    
    # Reaplicar a Engenharia de Features
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['dia_da_semana'] = df['datetime'].dt.dayofweek
    df['dia_do_mes'] = df['datetime'].dt.day
    df['mes'] = df['datetime'].dt.month
    df['ano'] = df['datetime'].dt.year
    df['semana_do_ano'] = df['datetime'].dt.isocalendar().week.astype(int)
    df['eh_feriado'] = 0 
    df['eh_inicio_de_mes'] = df['datetime'].dt.day.between(1, 5).astype(int)
    df['eh_fim_de_semana'] = (df['datetime'].dt.dayofweek >= 5).astype(int)
    df['gasto_vs_media'] = df['gmv_success'] - df['gasto_medio_acumulado']
    
    # Fazer as Predições
    X_class = df[features_class]
    X_reg = df[features_avancadas_regressor]
    
    prob_recompra = model_clf.predict_proba(X_class)[0, 1]
    dias_preditos_raw = model_reg.predict(X_reg)[0]
    
    # CORREÇÃO: Tratar dias negativos e aplicar a regra de negócio
    dias_preditos = max(0, dias_preditos_raw)
    if prob_recompra < 0.5:
        dias_preditos = -1.0 # Mantém a sua lógica de negócio
        
    return {
        'probabilidade_recompra_30d': float(prob_recompra),
        'previsao_dias_prox_compra': float(round(dias_preditos, 1))
    }

# --- Endpoint da API ATUALIZADO ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        dados_json = request.get_json(force=True)
        
        # Validação da entrada
        if 'fk_contact' not in dados_json:
            return jsonify({"erro": "A chave 'fk_contact' é obrigatória no JSON de entrada."}), 400

        fk_contact = dados_json['fk_contact']

        # 1. Executa a lógica do Desafio 2
        resultado_desafio2 = fazer_previsao_desafio2(dados_json)

        # 2. Executa a lógica do Desafio 3 (Consulta)
        recomendacoes_rotas = fallback_routes  # Começa com o fallback
        if df_recomendacoes is not None and fk_contact in df_recomendacoes.index:
            recomendacoes_rotas = df_recomendacoes.loc[fk_contact, 'recomendacoes_rotas_top5']

        # 3. Combina todos os resultados em uma única resposta
        resposta_final = {
            'fk_contact': fk_contact,
            'probabilidade_recompra_30d': round(resultado_desafio2['probabilidade_recompra_30d'] * 100, 2),
            'previsao_dias_prox_compra': resultado_desafio2['previsao_dias_prox_compra'],
            'recomendacoes_rotas_top5': recomendacoes_rotas
        }
        
        return jsonify(resposta_final)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return jsonify({"erro": str(e)}), 500

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)