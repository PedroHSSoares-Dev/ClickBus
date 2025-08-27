# Desafio 3 – A Estrada à Frente: Sistema de Recomendação de Rotas

## 🎯 Objetivo

Desenvolver um sistema de recomendação para prever a próxima rota (origem → destino) mais provável para cada cliente, com o objetivo de personalizar a experiência do usuário e aumentar a conversão.

---

## ✔️ Solução Implementada

A solução final consiste em um sistema de recomendação que opera em modo batch, com uma lógica robusta para lidar com diferentes perfis de clientes e validada através de backtesting.

### 1. Modelo de Recomendação Baseado em Histórico

O núcleo do sistema é um modelo de baseline forte que recomenda as **5 rotas mais frequentes** no histórico de compras de cada cliente. Esta abordagem capitaliza a alta lealdade e o comportamento de repetição dos usuários, que foi identificado como o padrão mais forte durante a análise.

### 2. Estratégia de Fallback para "Cold Start"

Para lidar com clientes novos ou com histórico de compras insuficiente (apenas uma transação), foi implementada uma estratégia de fallback. Em vez de não fornecer uma recomendação, o sistema sugere as **5 rotas mais populares da plataforma no geral**. Isso garante que todos os clientes recebam uma recomendação relevante, melhorando a experiência do usuário.

### 3. Validação com Backtesting Temporal

A eficácia do modelo foi validada utilizando uma metodologia de **backtesting com divisão temporal**. Os dados foram divididos em um período de treino (passado) e um período de teste (futuro), simulando um ambiente de produção real. Esta abordagem garantiu uma avaliação honesta e confiável da performance do modelo.

-   **Métrica Chave:** A métrica principal utilizada foi o **Recall@5**, que mede a porcentagem de vezes que a rota correta comprada pelo cliente estava entre as 5 rotas recomendadas.
-   **Resultado:** O modelo alcançou um `Recall@5` de aproximadamente **47%**, validando que a abordagem é comercialmente valiosa.

### 4. Arquitetura de Batch Scoring

As recomendações não são calculadas em tempo real a cada requisição. Em vez disso, elas são pré-calculadas em um processo "batch" (offline) e salvas em um arquivo CSV. A API então apenas consulta este arquivo, garantindo uma resposta em tempo real (<50ms) com altíssima performance e escalabilidade.

---

## 🚀 Entregáveis Finais

1.  **Notebook de Análise e Modelagem (`recomendacao_rotas.ipynb`):** Contém todo o processo de análise, treinamento do modelo, backtesting e a geração dos artefatos finais.

2.  **Artefato para a API (`recomendacoes_completas_api.csv`):** Um arquivo CSV contendo as 5 rotas recomendadas (personalizadas ou de fallback) para **todos os clientes** com histórico de compras, pronto para ser consumido pela API do Desafio 2.
