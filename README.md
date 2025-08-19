# 🚌 Challenge ClickBus – Roadmap e Entregáveis

Este repositório reúne a solução para o **Challenge ClickBus**, dividido em três projetos:

- **Desafio 1 - Decodificando o Comportamento do Cliente**  
- **Desafio 2 - O Timing é Tudo**  
- **Desafio 3 - A Estrada à Frente**  

---

## 📂 Estrutura do Projeto
```
📁 Challenge_ClickBus/           # Documentação e arquivos do challenge
├── 📄 README.md                 # Visão geral do challenge
├── 📄 LICENSE                   # Licença do challenge
├── 📄 requirements.txt          # Dependências do challenge
├── 📁 data/                     # Dados utilizados no desafio
│   ├── 📁 raw/                  # Dados originais
│   └── 📁 processed/            # Dados após processamento
├── 📁 desafios/                 # Diretório principal para os desafios
│   ├── 📁 desafioX_.../         # Estrutura que vai se replicar na pasta do desafio 1 | 2 | 3
│   │   ├── 📄 README.md         # Detalhes do desafio
│   │   ├── 📁 notebooks/        # Notebooks Jupyter da Sprint
│   │   └── 📁 relatorios/       # Relatórios e apresentações
│   │       └── 📁 figuras/      # Imagens e gráficos
├── 📁 docs/                     # Documentação geral do challenge
└── 📁 testes/                   # Scripts de testes automatizados
```

---

## 🎯 Objetivos e Entregáveis

### Desafio 1 – Decodificando o Comportamento do Cliente  
- **Objetivo**: Segmentar clientes em grupos (VIP, frequentes, ocasionais, dormindo) com base no histórico de compras.  
- **Extra**: Construir um dashboard interativo para monitorar a evolução desses grupos ao longo do tempo.  
- **Entregáveis**:  
  - Apresentação executiva (slides)  
  - Material de backup (relatório detalhado)  
  - Scripts Python para RFM + clusterização  
  - Dashboard (Streamlit/Dash)  
  - Predefinição de clusters exportada (CSV)

### Desafio 2 – O Timing é Tudo  
- **Objetivo**: Prever se cliente comprará nos próximos 7 ou 30 dias (classificação binária).  
- **Extra**: Prever quantos dias até essa próxima compra (regressão).  
- **Entregáveis**:  
  - Apresentação executiva  
  - Material de backup  
  - Modelos LightGBM e XGBoost treinados  
  - Pipeline de pré-processamento e AutoML (Optuna/FLAML)  
  - API REST para predições (Flask + Docker)  
  - Arquivo CSV com predições para 50.000 clientes

### Desafio 3 – A Estrada à Frente  
- **Objetivo**: Prever o próximo trecho (origem → destino) de cada cliente (classificação multi-classe ou recomendação).  
- **Extra**: Juntar previsão de data + trecho em uma única entrega.  
- **Entregáveis**:  
  - Apresentação executiva  
  - Material de backup  
  - Sistema de recomendação híbrido (Collaborative Filtering + grafos + Transformer opcional)  
  - Micro-serviço de recomendação (FastAPI/Flask + Docker)  
  - CSV com rotas sugeridas + datas para 50.000 clientes

---

## 📦 Dados e Confidencialidade

- **Sample**: ~800.000 clientes (anonimizado)  
- **Formato**: tabelas SQL com colunas como `nk_order_id`, `fk_contact`, `date_purchase`, `gmv_success`, etc.  
- **Sigilo**: os dados são restritos e não podem ser compartilhados ou utilizados fora deste desafio.

---

## 🚀 Como Começar

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/PedroHSSoares-Dev/Challenge_ClickBus.git
   cd Challenge_ClickBus
   ```
2. **Instale as dependências**
  ```bash
   pip install -r ../requirements.txt
   ```
3. **Execute**
  - No diretório de cada sprint, use os notebooks para EDA e scripts em src/ para reproduzir análises e modelos.
  - Para rodar dashboards/API, consulte as instruções no README de cada sprint.

---

## 📄 Licença
Este projeto está licenciado sob a *MIT License*. Consulte o arquivo LICENSE para detalhes.
