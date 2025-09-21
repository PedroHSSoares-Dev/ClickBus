import os
import json
import logging
import requests
import pandas as pd
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÕES GLOBAIS ---
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'URL_NAO_CONFIGURADA')
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'dados-clickbus-pedrohs')
storage_client = storage.Client()

# ==============================================================================
# SEÇÃO 0: HELPER
# ==============================================================================
def baixar_csv_do_gcs(bucket_name, file_name):
    """Baixa um CSV do GCS e o carrega para um DataFrame."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        if not blob.exists():
            logger.warning(f"Arquivo {file_name} não encontrado no bucket {bucket_name}.")
            return None
        from io import StringIO
        return pd.read_csv(StringIO(blob.download_as_string().decode('utf-8')))
    except Exception as e:
        logger.exception(f"Erro ao baixar {file_name}: {e}")
        return None

# ==============================================================================
# SEÇÃO 1: LÓGICA PRINCIPAL
# ==============================================================================

def gerar_e_enviar_relatorio_consolidado():
    """Gera um único relatório consolidado e o envia para o Slack."""
    
    # --- Parte 1: A Manchete (Análise de Migração) ---
    df_hoje = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cliente.csv')
    df_ontem = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cliente_antigo.csv')

    texto_migracao = "Nenhuma migração de clientes entre clusters foi detectada hoje."
    if df_hoje is not None and df_ontem is not None:
        df_migracao = pd.merge(df_ontem[['fk_contact', 'grupo']], df_hoje[['fk_contact', 'grupo']], on='fk_contact', suffixes=('_ontem', '_hoje'))
        migrados = df_migracao[df_migracao['grupo_ontem'] != df_migracao['grupo_hoje']]
        if not migrados.empty:
            contagem = migrados.groupby(['grupo_ontem', 'grupo_hoje']).size().reset_index(name='qtd')
            texto_migracao = "Principais movimentações de hoje:\n"
            for _, row in contagem.head(5).iterrows():
                texto_migracao += f"➡️ {row['qtd']} clientes moveram de '{row['grupo_ontem']}' para '{row['grupo_hoje']}'\n"
        # Atualiza o arquivo antigo para o próximo dia
        storage_client.bucket(GCS_BUCKET_NAME).copy_blob(storage_client.bucket(GCS_BUCKET_NAME).blob('cliente.csv'), storage_client.bucket(GCS_BUCKET_NAME), 'cliente_antigo.csv')
    
    # --- Parte 2: O Raio-X (Detalhes dos Clusters) ---
    df_cluster = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cluster.csv')
    blocos_detalhes = []
    if df_cluster is not None:
        for _, row in df_cluster.iterrows():
            texto_cluster = (f"*{row['cluster']}* ({row['Qtd']} clientes)\n"
                             f"> Recência: `{round(row['recency_mean'])}d` | Frequência: `{round(row['frequency_mean'])}` | Gasto: `R$ {row['monetary_mean']:.2f}`")
            blocos_detalhes.append({"type": "section", "text": {"type": "mrkdwn", "text": texto_cluster}})

    # --- Montagem da Mensagem Final ---
    mensagem = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "📈 Relatório Diário de Análise de Growth"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": texto_migracao}},
            {"type": "divider"},
            {"type": "header", "text": {"type": "plain_text", "text": "🔍 Raio-X dos Clusters Atuais"}},
            *blocos_detalhes # O '*' desempacota a nossa lista de blocos aqui
        ]
    }

    # --- Envio para o Slack ---
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=mensagem, timeout=10)
        logger.info(f"Resposta do Slack: Status={resp.status_code}, Corpo={resp.text}")
    except Exception as e:
        logger.exception(f"Erro ao tentar enviar a mensagem para o Slack: {e}")

# ==============================================================================
# SEÇÃO 2: ENTRYPOINT (O "Porteiro" Simplificado)
# ==============================================================================

def clickbus_webhook(request):
    """Entrypoint: Recebe a chamada do agendador e executa o relatório consolidado."""
    if request.method == 'GET':
        logger.info("Requisição GET recebida, gerando relatório consolidado...")
        gerar_e_enviar_relatorio_consolidado()
        return ("Relatório consolidado acionado.", 200)
    
    return ("Método não permitido.", 405)