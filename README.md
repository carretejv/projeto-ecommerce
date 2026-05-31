# 🛒 Vendas em E-commerce no Brasil

**Projeto G2 — Tema 13 | Disciplina: Linguagem de Programação — Análise e Visualização de Dados com Python**

---

## 📌 Descrição

Análise completa de dados de vendas em e-commerce brasileiro (2015–2024), contemplando faturamento, lucro, sazonalidade, desempenho regional e logístico por meio de um dashboard interativo em Streamlit.

---

## 🎯 Objetivos

- Analisar a evolução temporal do faturamento
- Identificar categorias e produtos mais lucrativos
- Comparar regiões e estados por desempenho
- Investigar sazonalidade de consumo
- Avaliar desempenho logístico e satisfação do cliente

---

## 🗂️ Estrutura do Projeto

```
projeto-ecommerce/
│
├── app.py                    ← Dashboard Streamlit
├── requirements.txt          ← Dependências Python
├── README.md                 ← Este arquivo
├── index.html                ← Página GitHub Pages
├── dados/
│   └── simulacao_ecommerce_brasil.csv
├── notebooks/
│   └── analise_ecommerce.ipynb
├── database/                 ← (SQLite, se utilizado)
└── imagens/                  ← Capturas de tela
```

---

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/projeto-ecommerce.git
cd projeto-ecommerce

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| Pandas | Manipulação de dados |
| Matplotlib | Visualizações estáticas |
| Seaborn | Estilização de gráficos |
| NumPy | Cálculos numéricos |
| Streamlit | Dashboard interativo |
| GitHub | Controle de versão |
| GitHub Pages | Página web do projeto |
| Streamlit Cloud | Deploy do dashboard |

---

## 📊 Funcionalidades do Dashboard

- **KPIs dinâmicos**: faturamento total, lucro, ticket médio, avaliação
- **Filtros múltiplos**: ano, mês, região, UF, categoria, canal de venda
- **Evolução temporal**: gráficos de linha por ano e barra por mês
- **Heatmap de sazonalidade**: mês × ano
- **Comparação regional**: faturamento e ticket médio por região e UF
- **Análise por categoria**: faturamento e participação no lucro
- **Canal de venda**: faturamento e avaliação por canal
- **Dispersão lucro × faturamento**: por categoria
- **Análise logística**: prazo de entrega por categoria e região
- **Tabela dinâmica interativa**: agrupamento configurável
- **Conclusão executiva**: gerada dinamicamente com base nos filtros

---

## 🔗 Links

- 📁 **GitHub**: [GitHub](https://github.com/carretejv/projeto-ecommerce)
- 🌐 **GitHub Pages**: [GitHub Pages](https://carretejv.github.io/projeto-ecommerce/)
- 📊 **Streamlit**: [Dashboard Streamlit]([https://seu-app.streamlit.app](https://carretejv.github.io/projeto-ecommerce/)

---

## 📚 Base de Dados

Dataset simulado com **4.440 registros** e **16 colunas** cobrindo vendas de 2015 a 2024 em todo o Brasil.

| Coluna | Descrição |
|---|---|
| ano / mes / data | Período da venda |
| regiao / uf / cidade | Localização |
| canal_venda | Marketplace, Site próprio, Aplicativo |
| categoria / produto | Tipo e nome do produto |
| quantidade / preco_unitario | Volume e preço |
| faturamento / custo / lucro | Resultado financeiro |
| prazo_entrega | Dias para entrega |
| avaliacao_cliente | Nota de 0 a 5 |

---

Projeto G2 · Tema 13 — Vendas em E-commerce no Brasil
