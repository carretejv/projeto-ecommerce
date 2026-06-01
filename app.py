import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="E-commerce Brasil — Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilo global ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card{background:#f0f4ff;border-radius:10px;padding:16px 20px;margin-bottom:8px;border-left:5px solid #4a6cf7}
.metric-value{font-size:1.6rem;font-weight:700;color:#1a237e}
.metric-label{font-size:0.85rem;color:#555}
section[data-testid="stSidebar"]{background:#1a237e}
section[data-testid="stSidebar"] *{color:white !important}
h1{color:#1a237e}
h2,h3{color:#283593}
</style>
""", unsafe_allow_html=True)

# ── Carregamento de dados ────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    caminho = os.path.join(os.path.dirname(__file__), "dados", "simulacao_ecommerce_brasil.csv")
    df = pd.read_csv(caminho)
    df["data"] = pd.to_datetime(df["data"])
    return df

df_raw = carregar_dados()

# ── Sidebar — filtros ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shopping-cart.png", width=60)
    st.title("Filtros")

    anos = sorted(df_raw["ano"].unique())
    anos_sel = st.multiselect("Ano", anos, default=anos)

    meses_nomes = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
                   7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    meses_sel = st.multiselect("Mês", list(meses_nomes.keys()),
                               format_func=lambda x: meses_nomes[x],
                               default=list(meses_nomes.keys()))

    regioes = sorted(df_raw["regiao"].unique())
    regioes_sel = st.multiselect("Região", regioes, default=regioes)

    ufs = sorted(df_raw[df_raw["regiao"].isin(regioes_sel)]["uf"].unique())
    ufs_sel = st.multiselect("Estado (UF)", ufs, default=ufs)

    cats = sorted(df_raw["categoria"].unique())
    cats_sel = st.multiselect("Categoria", cats, default=cats)

    canais = sorted(df_raw["canal_venda"].unique())
    canais_sel = st.multiselect("Canal de Venda", canais, default=canais)

# ── Filtragem ────────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["ano"].isin(anos_sel) &
    df_raw["mes"].isin(meses_sel) &
    df_raw["regiao"].isin(regioes_sel) &
    df_raw["uf"].isin(ufs_sel) &
    df_raw["categoria"].isin(cats_sel) &
    df_raw["canal_venda"].isin(canais_sel)
].copy()

if df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.title("🛒 Vendas em E-commerce no Brasil")
st.markdown("""
**Análise de vendas no comércio eletrônico brasileiro (2015–2024).**  
Explore faturamento, lucro, sazonalidade, desempenho regional e muito mais.
""")
st.markdown("---")

# ── KPIs ─────────────────────────────────────────────────────────────────────
st.subheader("📊 Indicadores-Chave de Desempenho (KPIs)")

fat_total   = df["faturamento"].sum()
lucro_total = df["lucro"].sum()
ticket_med  = df["faturamento"].mean()
margem      = (lucro_total / fat_total * 100) if fat_total > 0 else 0
prod_top    = df.groupby("produto")["quantidade"].sum().idxmax()
cat_top     = df.groupby("categoria")["lucro"].sum().idxmax()
reg_top     = df.groupby("regiao")["faturamento"].sum().idxmax()
prazo_med   = df["prazo_entrega"].mean()
aval_med    = df["avaliacao_cliente"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Faturamento Total",   f"R$ {fat_total/1e6:,.2f} M")
k2.metric("📈 Lucro Total",         f"R$ {lucro_total/1e6:,.2f} M")
k3.metric("🧾 Ticket Médio",        f"R$ {ticket_med:,.0f}")
k4.metric("📦 Produto Mais Vendido", prod_top)
k5.metric("🏆 Categoria Top",        cat_top)

k6, k7, k8 = st.columns(3)
k6.metric("🌎 Região Destaque",  reg_top)
k7.metric("🚚 Prazo Médio (dias)", f"{prazo_med:.1f}")
k8.metric("⭐ Avaliação Média",    f"{aval_med:.2f} / 5.0")

st.markdown("---")

# ── Seção 1 — Evolução temporal ──────────────────────────────────────────────
st.subheader("📅 Evolução Temporal das Vendas")

col1, col2 = st.columns(2)

with col1:
    fat_ano = df.groupby("ano")["faturamento"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(fat_ano["ano"], fat_ano["faturamento"]/1e6, marker="o",
            color="#4a6cf7", linewidth=2.5)
    ax.fill_between(fat_ano["ano"], fat_ano["faturamento"]/1e6, alpha=0.15, color="#4a6cf7")
    ax.set_title("Faturamento Anual (R$ Milhões)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Ano"); ax.set_ylabel("R$ Milhões")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))
    ax.grid(axis="y", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    fat_mes = df.groupby("mes")["faturamento"].mean().reset_index()
    fat_mes["mes_nome"] = fat_mes["mes"].map(meses_nomes)
    fig, ax = plt.subplots(figsize=(7, 4))
    cores = ["#ff7043" if m in [11, 12] else "#4a6cf7" for m in fat_mes["mes"]]
    ax.bar(fat_mes["mes_nome"], fat_mes["faturamento"]/1e3, color=cores)
    ax.set_title("Faturamento Médio por Mês (R$ Mil)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Mês"); ax.set_ylabel("R$ Mil")
    ax.grid(axis="y", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

st.info("📌 O faturamento cresce consistentemente ao longo dos anos. Novembro e dezembro (em laranja) costumam apresentar picos sazonais relacionados à Black Friday e festas de fim de ano.")

# ── Seção 2 — Heatmap de sazonalidade ───────────────────────────────────────
st.subheader("🗓️ Sazonalidade — Heatmap Mensal por Ano")

pivot = df.pivot_table(values="faturamento", index="ano", columns="mes", aggfunc="sum")
pivot.columns = [meses_nomes[c] for c in pivot.columns]
fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(pivot/1e6, annot=True, fmt=".1f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "R$ Milhões"})
ax.set_title("Faturamento por Mês e Ano (R$ Milhões)", fontsize=14, fontweight="bold")
ax.set_xlabel("Mês"); ax.set_ylabel("Ano")
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Seção 3 — Análise regional ───────────────────────────────────────────────
st.subheader("🗺️ Comparação Regional")

col1, col2 = st.columns(2)

with col1:
    reg_fat = df.groupby("regiao")["faturamento"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    cores_reg = sns.color_palette("Blues_d", len(reg_fat))
    reg_fat.plot(kind="barh", ax=ax, color=cores_reg)
    ax.set_title("Faturamento por Região (R$)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Faturamento (R$)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax.grid(axis="x", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    uf_fat = df.groupby("uf")[["faturamento","lucro"]].sum().sort_values("faturamento", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(uf_fat))
    w = 0.4
    ax.bar(x - w/2, uf_fat["faturamento"]/1e6, w, label="Faturamento", color="#4a6cf7")
    ax.bar(x + w/2, uf_fat["lucro"]/1e6, w, label="Lucro", color="#26c6da")
    ax.set_xticks(x); ax.set_xticklabels(uf_fat.index)
    ax.set_title("Top 10 UFs — Faturamento vs Lucro (R$ Milhões)", fontsize=13, fontweight="bold")
    ax.set_ylabel("R$ Milhões"); ax.legend()
    ax.grid(axis="y", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

# ── Ticket médio por região ──────────────────────────────────────────────────
ticket_reg = df.groupby("regiao")["faturamento"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 3))
cores_t = ["#ff7043" if v == ticket_reg.max() else "#90a4ae" for v in ticket_reg]
ax.bar(ticket_reg.index, ticket_reg/1e3, color=cores_t)
ax.set_title("Ticket Médio por Região (R$ Mil)", fontsize=13, fontweight="bold")
ax.set_ylabel("R$ Mil"); ax.grid(axis="y", alpha=0.3)
sns.despine(ax=ax)
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Seção 4 — Análise por categoria ─────────────────────────────────────────
st.subheader("🏷️ Análise por Categoria de Produto")

col1, col2 = st.columns(2)

with col1:
    cat_fat = df.groupby("categoria")["faturamento"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    cat_fat.plot(kind="barh", ax=ax, color=sns.color_palette("Set2", len(cat_fat)))
    ax.set_title("Faturamento por Categoria", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax.grid(axis="x", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    cat_lucro = df.groupby("categoria")["lucro"].sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    wedge_props = dict(width=0.5, edgecolor="white")
    ax.pie(cat_lucro, labels=cat_lucro.index, autopct="%1.1f%%",
           colors=sns.color_palette("Set2", len(cat_lucro)),
           wedgeprops=wedge_props, startangle=90)
    ax.set_title("Participação no Lucro Total por Categoria", fontsize=13, fontweight="bold")
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Seção 5 — Canal de venda ─────────────────────────────────────────────────
st.subheader("📡 Desempenho por Canal de Venda")

col1, col2 = st.columns(2)

with col1:
    canal_fat = df.groupby("canal_venda")["faturamento"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    canal_fat.plot(kind="bar", ax=ax, color=["#4a6cf7","#26c6da","#ff7043"])
    ax.set_title("Faturamento por Canal", fontsize=13, fontweight="bold")
    ax.set_ylabel("R$"); ax.set_xticklabels(canal_fat.index, rotation=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax.grid(axis="y", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    canal_aval = df.groupby("canal_venda")["avaliacao_cliente"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    canal_aval.plot(kind="bar", ax=ax, color=["#26c6da","#4a6cf7","#ff7043"])
    ax.set_title("Avaliação Média por Canal", fontsize=13, fontweight="bold")
    ax.set_ylabel("Nota (0–5)"); ax.set_xticklabels(canal_aval.index, rotation=0)
    ax.set_ylim(0, 5); ax.grid(axis="y", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Seção 6 — Dispersão lucro x faturamento ─────────────────────────────────
st.subheader("💹 Relação Lucro × Faturamento por Categoria")

fig, ax = plt.subplots(figsize=(10, 5))
categorias = df["categoria"].unique()
palette = sns.color_palette("Set2", len(categorias))
for i, cat in enumerate(categorias):
    sub = df[df["categoria"] == cat]
    ax.scatter(sub["faturamento"], sub["lucro"], label=cat,
               color=palette[i], alpha=0.5, s=30)
ax.set_title("Dispersão: Lucro × Faturamento", fontsize=14, fontweight="bold")
ax.set_xlabel("Faturamento (R$)"); ax.set_ylabel("Lucro (R$)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e3:.0f}k"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e3:.0f}k"))
ax.legend(title="Categoria"); ax.grid(alpha=0.3)
sns.despine(ax=ax)
st.pyplot(fig)
plt.close()

st.markdown("---")

# ── Seção 7 — Logística ──────────────────────────────────────────────────────
st.subheader("🚚 Análise Logística")

col1, col2 = st.columns(2)

with col1:
    prazo_cat = df.groupby("categoria")["prazo_entrega"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    prazo_cat.plot(kind="barh", ax=ax,
                   color=["#26c6da" if v == prazo_cat.min() else "#90a4ae" for v in prazo_cat])
    ax.set_title("Prazo Médio de Entrega por Categoria (dias)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Dias"); ax.grid(axis="x", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    prazo_reg = df.groupby("regiao")["prazo_entrega"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    prazo_reg.plot(kind="barh", ax=ax, color="#4a6cf7")
    ax.set_title("Prazo Médio de Entrega por Região (dias)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Dias"); ax.grid(axis="x", alpha=0.3)
    sns.despine(ax=ax)
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ── Seção 8 — Tabela dinâmica ────────────────────────────────────────────────
st.subheader("📋 Tabela Dinâmica — Exploração Detalhada")

agg_col = st.selectbox("Agrupar por:", ["categoria", "regiao", "uf", "canal_venda", "produto", "ano"])
tabela = (
    df.groupby(agg_col)
    .agg(
        Faturamento=("faturamento", "sum"),
        Lucro=("lucro", "sum"),
        Quantidade=("quantidade", "sum"),
        Ticket_Medio=("faturamento", "mean"),
        Avaliacao=("avaliacao_cliente", "mean"),
        Prazo_Entrega=("prazo_entrega", "mean"),
    )
    .sort_values("Faturamento", ascending=False)
    .reset_index()
)
tabela["Faturamento"] = tabela["Faturamento"].map("R$ {:,.0f}".format)
tabela["Lucro"]       = tabela["Lucro"].map("R$ {:,.0f}".format)
tabela["Ticket_Medio"]= tabela["Ticket_Medio"].map("R$ {:,.0f}".format)
tabela["Avaliacao"]   = tabela["Avaliacao"].map("{:.2f}".format)
tabela["Prazo_Entrega"]= tabela["Prazo_Entrega"].map("{:.1f} dias".format)
st.dataframe(tabela, use_container_width=True)

st.markdown("---")

# ── Conclusão executiva ──────────────────────────────────────────────────────
st.subheader("📝 Conclusão Executiva")

st.markdown(f"""
Com base na análise do período selecionado, destacam-se os seguintes achados:

- **Faturamento total** de **R$ {fat_total:,.0f}**, com margem de lucro de **{margem:.1f}%**.
- **{reg_top}** é a região de maior faturamento, enquanto o ticket médio mais elevado revela oportunidades de concentração de valor.
- **{cat_top}** é a categoria mais lucrativa do portfólio — estratégias de expansão neste segmento são recomendadas.
- A **sazonalidade** evidencia picos em novembro e dezembro (Black Friday / Natal), sugerindo planejamento antecipado de estoque e logística.
- O prazo médio de entrega de **{prazo_med:.1f} dias** e avaliação média de **{aval_med:.2f}/5.0** indicam {'boa satisfação dos clientes' if aval_med >= 4.0 else 'oportunidade de melhoria na experiência do cliente'}.
- O crescimento consistente do faturamento ao longo dos anos confirma a expansão do e-commerce como canal estratégico no Brasil.

> *Este painel foi desenvolvido como projeto acadêmico da disciplina de Linguagem de Programação — Análise e Visualização de Dados com Python.*
> *João Victor Carrete*
""")
