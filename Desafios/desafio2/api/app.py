import flask
from flask import request, jsonify
import joblib
import pandas as pd
import numpy as np

app = flask.Flask(__name__)

# --- Carregamento dos Modelos ---
print("Carregando modelos...")
model_clf = joblib.load('../modelos/xgboost_classificador_final.joblib')
model_reg = joblib.load('../modelos/xgboost_regressor_final.joblib')
print("Modelos carregados com sucesso.")

# --- Listas de Features (ORDEM CORRIGIDA E SINCRONIZADA) ---
features_class = [
    'gmv_success', 'total_tickets_quantity_success', 'dia_da_semana', 
    'dia_do_mes', 'mes', 'ano', 'semana_do_ano', 'gasto_medio_acumulado', 
    'qtd_compras_acumulada', 'gasto_max_acumulado'
]

# CORREÇÃO DEFINITIVA: Esta lista agora é idêntica à que o modelo de regressão foi treinado.
# A coluna 'dias_desde_ultima_compra' é criada, mas não entra nesta lista final.
features_avancadas_regressor = [
    'gmv_success', 'total_tickets_quantity_success', 'dia_da_semana', 
    'dia_do_mes', 'mes', 'ano', 'semana_do_ano', 'gasto_medio_acumulado', 
    'qtd_compras_acumulada', 'gasto_max_acumulado', 'eh_feriado', 
    'eh_inicio_de_mes', 'eh_fim_de_semana', 'media_intervalo_compras', 
    'std_intervalo_compras', 'gasto_vs_media'
]

# --- Lógica de Pré-processamento e Predição ---
def fazer_previsao(dados_cliente):
    df = pd.DataFrame(dados_cliente, index=[0])

    # --- Reaplicar a Engenharia de Features ---
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Features de tempo
    df['dia_da_semana'] = df['datetime'].dt.dayofweek
    df['dia_do_mes'] = df['datetime'].dt.day
    df['mes'] = df['datetime'].dt.month
    df['ano'] = df['datetime'].dt.year
    df['semana_do_ano'] = df['datetime'].dt.isocalendar().week.astype(int)

    # Features de calendário
    df['eh_feriado'] = 0 
    df['eh_inicio_de_mes'] = df['datetime'].dt.day.between(1, 5).astype(int)
    df['eh_fim_de_semana'] = (df['datetime'].dt.dayofweek >= 5).astype(int)
    
    # Features de histórico
    df['gasto_vs_media'] = df['gmv_success'] - df['gasto_medio_acumulado']
    
    # --- Fazer as Predições ---
    X_class = df[features_class]
    X_reg = df[features_avancadas_regressor] # Usando a lista correta
    
    prob_recompra = model_clf.predict_proba(X_class)[0, 1]
    dias_preditos = model_reg.predict(X_reg)[0]
    
    if prob_recompra < 0.5:
        dias_preditos = -1.0
        
    return {
        'probabilidade_recompra_30d': float(prob_recompra),
        'previsao_dias_prox_compra': float(round(dias_preditos, 1))
    }

# --- Endpoint da API ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        dados_json = request.get_json(force=True)
        resultado = fazer_previsao(dados_json)
        return jsonify(resultado)
    except Exception as e:
        # Adiciona um log de erro mais detalhado no terminal da API
        print(f"Ocorreu um erro: {e}")
        return jsonify({"erro": str(e)}), 500

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)