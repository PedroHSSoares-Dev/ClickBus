import os
import json
import logging
import requests
import pandas as pd
from google.cloud import storage
from flask import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÕES GLOBAIS ---
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'URL_NAO_CONFIGURADA')
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'dados-clickbus-pedrohs')
storage_client = storage.Client()

# ==============================================================================
# SEÇÃO 0: HELPERS
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
# SEÇÃO 1: LÓGICA DAS FUNCIONALIDADES
# ==============================================================================

def gerar_relatorio_movimentacao():
    """Gera o relatório diário de migração de clientes."""
    df_hoje = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cliente.csv')
    df_ontem = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cliente_antigo.csv')

    if df_hoje is None or df_ontem is None:
        texto_migracao = "ERRO: Não foi possível carregar os arquivos de clientes para comparação."
    else:
        df_migracao = pd.merge(df_ontem[['fk_contact', 'grupo']], df_hoje[['fk_contact', 'grupo']], on='fk_contact', suffixes=('_ontem', '_hoje'))
        migrados = df_migracao[df_migracao['grupo_ontem'] != df_migracao['grupo_hoje']]
        if not migrados.empty:
            contagem = migrados.groupby(['grupo_ontem', 'grupo_hoje']).size().reset_index(name='qtd')
            texto_migracao = "Principais movimentações de hoje:\n"
            for _, row in contagem.head(5).iterrows():
                texto_migracao += f"➡️ {row['qtd']} clientes moveram de '{row['grupo_ontem']}' para '{row['grupo_hoje']}'\n"
        else:
            texto_migracao = "Nenhuma migração de clientes entre clusters foi detectada hoje."
        # Atualiza o arquivo antigo para o próximo dia
        storage_client.bucket(GCS_BUCKET_NAME).copy_blob(storage_client.bucket(GCS_BUCKET_NAME).blob('cliente.csv'), storage_client.bucket(GCS_BUCKET_NAME), 'cliente_antigo.csv')

    mensagem = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "📈 Relatório Diário de Movimentação"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": texto_migracao}},
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": "Para mais informações, consulte os detalhes do cluster:"}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "📊 Ver Detalhes dos Clusters"}, "action_id": "btn_detalhes_cluster", "style": "primary"}
            ]}
        ]
    }
    requests.post(SLACK_WEBHOOK_URL, json=mensagem)

def mostrar_detalhes_cluster():
    """Busca os detalhes dos clusters e formata a resposta."""
    df_cluster = baixar_csv_do_gcs(GCS_BUCKET_NAME, 'cluster.csv')
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "🔍 Detalhes dos Clusters de Clientes"}}]

    if df_cluster is not None:
        for _, row in df_cluster.iterrows():
            texto_cluster = (f"*{row['cluster']}* ({row['Qtd']} clientes)\n"
                             f"> Recência Média: `{round(row['recency_mean'])} dias` | "
                             f"Frequência Média: `{round(row['frequency_mean'])}` | "
                             f"Gasto Médio: `R$ {row['monetary_mean']:.2f}`")
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": texto_cluster}})
    else:
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": "Desculpe, não consegui encontrar o arquivo de resumo dos clusters (`cluster.csv`)."}})
    
    # Adiciona um botão para voltar ao relatório inicial
    blocks.append({"type": "actions", "elements": [
        {"type": "button", "text": {"type": "plain_text", "text": "🏠 Voltar ao Relatório Principal"}, "action_id": "btn_home"}
    ]})
    return {"replace_original": True, "blocks": blocks}

# ==============================================================================
# SEÇÃO 2: ENTRYPOINT (O "Porteiro")
# ==============================================================================

def clickbus_webhook(request):
    """Entrypoint: GET para o relatório, POST para interações."""
    try:
        # Chamada do Agendador ou teste manual
        if request.method == 'GET':
            logger.info("Requisição GET recebida, gerando relatório diário...")
            gerar_relatorio_movimentacao()
            return Response("Relatório diário acionado.", status=200)

        # Interação vinda do Slack (clique em botão)
        elif request.method == 'POST':
            payload = json.loads(request.form.get('payload'))
            action_id = payload['actions'][0]['action_id']
            response_url = payload.get('response_url')
            
            logger.info(f"Interação recebida: {action_id}")
            
            resposta_final = None
            if action_id == 'btn_detalhes_cluster':
                resposta_final = mostrar_detalhes_cluster()
            elif action_id == 'btn_home':
                # Ao clicar em "Voltar", simplesmente reenviamos o relatório principal
                gerar_relatorio_movimentacao()
                # E apagamos a mensagem anterior para não poluir o canal
                requests.post(response_url, json={"delete_original": True})
                return Response(status=200) # Apenas confirmamos o recebimento

            if resposta_final:
                requests.post(response_url, json=resposta_final)

            return Response(status=200) # Sempre confirma o recebimento para o Slack

    except Exception as e:
        logger.exception(f"Erro inesperado no handler: {e}")
        return Response("Erro interno no servidor.", status=500)

    return Response("Método não permitido.", status=405)