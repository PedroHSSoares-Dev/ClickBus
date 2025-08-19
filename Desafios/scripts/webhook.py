import requests
import os
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
caminho = os.getenv('URL_WEBHOOK')

CAMINHO_CSV = os.getenv('WEBHOOK_PATH')
ARQUIVO_CSV_ATUAL = f'{CAMINHO_CSV}cluster.csv'
ARQUIVO_JSON_ANTIGO = f'{CAMINHO_CSV}cluster_antigo.json'

def carregar_clusters():
    df_hoje = pd.read_csv(ARQUIVO_CSV_ATUAL)
    clusters_hoje = df_hoje.to_dict(orient="records")

    if not os.path.exists(ARQUIVO_JSON_ANTIGO):
        with open(ARQUIVO_JSON_ANTIGO, "w") as f:
            json.dump(clusters_hoje, f, indent=2)
        return clusters_hoje, None

    with open(ARQUIVO_JSON_ANTIGO, "r") as f:
        clusters_ontem = json.load(f)

    return clusters_hoje, clusters_ontem

def salvar_clusters_atuais(clusters_hoje):
    with open(ARQUIVO_JSON_ANTIGO, "w") as f:
        json.dump(clusters_hoje, f, indent=2)
        


def formatar_mensagem(clusters_hoje, clusters_ontem):
    hoje = datetime.now().strftime("%d/%m/%Y")
    mensagens = [f"*📊 Bom dia! O nosso relatório de hoje ({hoje}) já tá na mão:*"]

    clusters_ontem_dict = {c["cluster"]: c for c in clusters_ontem}

    for c_hoje in clusters_hoje:
        nome = c_hoje["cluster"]
        c_ontem = clusters_ontem_dict.get(nome)
        if not c_ontem:
            continue

        # Monetário
        monet_hoje = float(c_hoje["monetary"])
        monet_ontem = float(c_ontem["monetary"])
        monet_diff = monet_hoje - monet_ontem
        monet_pct = (monet_diff / monet_ontem) * 100 if monet_ontem else 0
        monet_emoji = "📈" if monet_diff > 0 else "📉" if monet_diff < 0 else "➖"

        # Frequência
        freq_hoje = float(c_hoje["frequency"])
        freq_ontem = float(c_ontem["frequency"])
        freq_diff = freq_hoje - freq_ontem
        freq_pct = (freq_diff / freq_ontem) * 100 if freq_ontem else 0
        freq_emoji = "📈" if freq_diff > 0 else "📉" if freq_diff < 0 else "➖"

        # Pessoas
        qtd_hoje = int(c_hoje["Qtd"])
        qtd_ontem = int(c_ontem["Qtd"])
        qtd_diff = qtd_hoje - qtd_ontem
        qtd_pct = (qtd_diff / qtd_ontem) * 100 if qtd_ontem else 0
        qtd_emoji = "📈" if qtd_diff > 0 else "📉" if qtd_diff < 0 else "➖"

        mensagens.append(
            f"\n🧠 *Cluster:* `{nome}`\n"
            f"💰 Monetário: *R${monet_hoje:,.2f}* {monet_emoji} `R${monet_diff:,.2f}` ({monet_pct:+.2f}%)\n"
            f"🔁 Frequência: *{freq_hoje:.2f}* {freq_emoji} `{freq_diff:.2f}` ({freq_pct:+.2f}%)\n"
            f"👥 Pessoas: *{qtd_hoje}* {qtd_emoji} `{qtd_diff}` ({qtd_pct:+.2f}%)"
        )

    
    alertas = gerar_alerta_quedas(clusters_hoje, clusters_ontem)
    if alertas:
        mensagens.append("\n🔍 *Atenção! Alguns clusters apresentaram queda:*\n")
        mensagens.extend(alertas)
        mensagens.append("\n🔧 *Sugestão:* Avaliar campanhas de reativação ou análise de churn nesses clusters.")
    else:
        mensagens.append("\n✅ Nenhum cluster apresentou queda hoje. Excelente!")

    return "\n".join(mensagens)


def gerar_alerta_quedas(clusters_hoje, clusters_ontem):
    clusters_ontem_dict = {c["cluster"]: c for c in clusters_ontem}
    alertas = []

    for c_hoje in clusters_hoje:
        nome = c_hoje["cluster"]
        c_ontem = clusters_ontem_dict.get(nome)
        if not c_ontem:
            continue

        monet_hoje = float(c_hoje["monetary"])
        monet_ontem = float(c_ontem["monetary"])
        monet_pct = ((monet_hoje - monet_ontem) / monet_ontem) * 100 if monet_ontem else 0

        freq_hoje = float(c_hoje["frequency"])
        freq_ontem = float(c_ontem["frequency"])
        freq_pct = ((freq_hoje - freq_ontem) / freq_ontem) * 100 if freq_ontem else 0

        qtd_hoje = int(c_hoje["Qtd"])
        qtd_ontem = int(c_ontem["Qtd"])
        qtd_pct = ((qtd_hoje - qtd_ontem) / qtd_ontem) * 100 if qtd_ontem else 0

        quedas = []
        if monet_pct < 0:
            quedas.append(f"💰 Monetário ({monet_pct:.2f}%)")
        if freq_pct < 0:
            quedas.append(f"🔁 Frequência ({freq_pct:.2f}%)")
        if qtd_pct < 0:
            quedas.append(f"👥 Pessoas ({qtd_pct:.2f}%)")

        if quedas:
            alertas.append(f"- `{nome}`: caiu em " + ", ".join(quedas))

    return alertas


def enviar_para_slack(msg, webhook_url):
    import requests
    payload = {"text": msg}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    webhook_url = os.getenv("URL_WEBHOOK")
    clusters_hoje, clusters_ontem = carregar_clusters()

    if clusters_ontem:
        mensagem = formatar_mensagem(clusters_hoje, clusters_ontem)
        enviar_para_slack(mensagem, webhook_url)
    else:
        print("Primeiro dia de execução. Dados antigos salvos, sem comparação.")

    salvar_clusters_atuais(clusters_hoje)