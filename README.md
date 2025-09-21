# 🚌 Challenge ClickBus – Análise e Soluções de Dados

Este repositório apresenta uma série de soluções desenvolvidas para o **Challenge ClickBus**, focado em desafios de análise de dados, modelagem preditiva e sistemas de recomendação. O projeto está estruturado em três desafios principais, cada um abordando aspectos cruciais para a otimização da experiência do cliente e das operações da empresa.

## 🌟 Visão Geral do Projeto

O objetivo central deste projeto é demonstrar a aplicação de técnicas avançadas de ciência de dados para resolver problemas de negócio específicos da ClickBus. Cada desafio foi concebido para ser uma unidade independente, mas complementar, visando aprimorar a compreensão do comportamento do cliente, prever suas futuras ações e oferecer recomendações personalizadas.

## 📂 Estrutura do Repositório

A organização do repositório foi pensada para facilitar a navegação e a compreensão de cada desafio. A estrutura principal é a seguinte:

```
ClickBus/
├── Desafios/                       # Contém os diretórios para cada desafio individual
│   ├── desafio1/                   # Solução para o Desafio 1
│   │   ├── README.md               # Detalhes específicos do Desafio 1
│   │   └── notebooks/              # Notebooks Jupyter para análise e modelagem
│   │       └── segmentacao.ipynb   # Notebook de segmentação de clientes
│   ├── desafio2/                   # Solução para o Desafio 2
│   │   ├── README.md               # Detalhes específicos do Desafio 2
│   │   ├── api/                    # API REST para predições
│   │   │   ├── app.py              # Aplicação Flask da API
│   │   │   ├── docker/             # Arquivos Docker para a API
│   │   │   │   └── Dockerfile
│   │   │   ├── modelos/            # Modelos treinados (LightGBM, XGBoost)
│   │   │   └── requirements.txt    # Dependências da API
│   │   └── notebooks/              # Notebooks Jupyter para tratamento de dados e modelagem
│   │       └── tratamento.ipynb    # Notebook de tratamento de dados
│   ├── desafio3/                   # Solução para o Desafio 3
│   │   ├── README.md               # Detalhes específicos do Desafio 3
│   │   └── notebooks/              # Notebooks Jupyter para o sistema de recomendação
│   │       └── recomendacao_rotas.ipynb # Notebook de recomendação de rotas
├── data/                           # Dados utilizados nos desafios
│   └── processed/                  # Dados após processamento
│       └── preparacao.ipynb        # Notebook de preparação de dados
├── webhook_gcp/                    # Webhook para integração com GCP
│   ├── main.py                     # Lógica principal do webhook
│   └── models/                     # Modelos utilizados pelo webhook
├── .gitignore                      # Arquivo de ignorar do Git
├── LICENSE                         # Licença do projeto
├── README.md                       # README original do projeto
└── requirements.txt                # Dependências gerais do projeto
```

## 🎯 Desafios Detalhados

### Desafio 1 – Decodificando o Comportamento do Cliente

*   **Objetivo**: Segmentar clientes em grupos distintos (e.g., VIP, frequentes, ocasionais, dormindo) com base em seu histórico de compras. Isso permite uma compreensão aprofundada do perfil de cada cliente e a criação de estratégias de marketing mais direcionadas.
*   **Extra**: Desenvolvimento de um dashboard interativo para monitorar a evolução desses grupos de clientes ao longo do tempo, oferecendo insights dinâmicos sobre o comportamento do consumidor.
*   **Entregáveis Principais**:
    *   Apresentação executiva (slides) com os principais achados da segmentação.
    *   Relatório detalhado (material de backup) com a metodologia e resultados completos.
    *   Scripts Python para a implementação da metodologia RFM (Recência, Frequência, Valor Monetário) e algoritmos de clusterização.
    *   Dashboard interativo (utilizando Streamlit ou Dash) para visualização e acompanhamento dos segmentos de clientes.
    *   Arquivo CSV contendo a predefinição dos clusters de clientes.
*   **Tecnologias Utilizadas**: Python, Pandas, Scikit-learn, Streamlit/Dash (para dashboard).

### Desafio 2 – O Timing é Tudo

*   **Objetivo**: Prever a probabilidade de um cliente realizar uma nova compra nos próximos 7 ou 30 dias (problema de classificação binária). Essa previsão é crucial para campanhas de marketing e gestão de estoque.
*   **Extra**: Prever o número exato de dias até a próxima compra do cliente (problema de regressão), permitindo um planejamento ainda mais preciso.
*   **Entregáveis Principais**:
    *   Apresentação executiva com os resultados e impactos dos modelos preditivos.
    *   Relatório detalhado (material de backup) sobre a construção e validação dos modelos.
    *   Modelos de Machine Learning treinados (LightGBM e XGBoost) para classificação e regressão.
    *   Pipeline de pré-processamento de dados e ferramentas de AutoML (Optuna/FLAML) para otimização dos modelos.
    *   API REST para predições em tempo real, implementada com Flask e conteinerizada com Docker.
    *   Arquivo CSV com as predições para um conjunto de 50.000 clientes.
*   **Tecnologias Utilizadas**: Python, Pandas, Scikit-learn, LightGBM, XGBoost, Optuna/FLAML, Flask, Docker.

### Desafio 3 – A Estrada à Frente

*   **Objetivo**: Prever o próximo trecho (origem → destino) que cada cliente irá comprar (problema de classificação multi-classe ou recomendação). Isso possibilita a oferta de rotas personalizadas e relevantes.
*   **Extra**: Integrar a previsão da data da próxima compra com a previsão do trecho, oferecendo uma recomendação completa de 


rota e data.
*   **Entregáveis Principais**:
    *   Apresentação executiva com a estratégia e os resultados do sistema de recomendação.
    *   Relatório detalhado (material de backup) sobre a arquitetura e implementação do sistema.
    *   Sistema de recomendação híbrido, combinando técnicas como Collaborative Filtering, grafos e, opcionalmente, Transformers.
    *   Micro-serviço de recomendação, implementado com FastAPI/Flask e conteinerizado com Docker, para integração em sistemas de produção.
    *   Arquivo CSV com rotas sugeridas e datas para um conjunto de 50.000 clientes.
*   **Tecnologias Utilizadas**: Python, Pandas, Scikit-learn, FastAPI/Flask, Docker, bibliotecas para grafos e Transformers (opcional).

## 📦 Dados e Confidencialidade

Os dados utilizados neste desafio são simulados e anonimizados, representando um sample de aproximadamente 800.000 clientes. As informações são fornecidas em formato de tabelas SQL, contendo colunas como `nk_order_id` (ID do pedido), `fk_contact` (ID do cliente), `date_purchase` (data da compra), `gmv_success` (valor bruto da mercadoria), entre outras. É importante ressaltar que, em um cenário real, tais dados seriam restritos e não poderiam ser compartilhados ou utilizados fora do contexto do desafio, garantindo a privacidade e segurança das informações.

## 🚀 Como Começar

Para configurar e executar os projetos localmente, siga os passos abaixo:

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/PedroHSSoares-Dev/ClickBus.git
    cd ClickBus
    ```

2.  **Instale as dependências gerais**:
    ```bash
    pip install -r requirements.txt
    ```
    As dependências listadas em `requirements.txt` incluem:
    *   `pandas`: Para manipulação e análise de dados.
    *   `numpy`: Para operações numéricas.
    *   `scikit-learn`: Para algoritmos de Machine Learning.
    *   `python-dotenv`: Para gerenciamento de variáveis de ambiente.
    *   `lightgbm`: Para o algoritmo LightGBM, utilizado em modelos preditivos.

3.  **Execute os desafios**:
    *   Navegue até o diretório de cada desafio (`Desafios/desafioX/`).
    *   Dentro de cada diretório, consulte o `README.md` específico para instruções detalhadas sobre como executar os notebooks Jupyter (localizados em `notebooks/`) e os scripts Python (se houver).
    *   Para as APIs e dashboards, as instruções de execução e conteinerização com Docker estarão nos `README.md` correspondentes.

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Para mais detalhes, consulte o arquivo `LICENSE` presente na raiz do repositório.

## 🧑‍💻 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests. Por favor, siga as boas práticas de desenvolvimento e mantenha o código limpo e documentado.

## 📞 Contato

Para dúvidas ou sugestões, entre em contato com o autor do repositório através do GitHub.