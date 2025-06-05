import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

st.set_page_config(
    page_title="📊 Relatório de Assuntos por LBL e Macro Tema",
    page_icon="📈",
    layout="wide",
)

st.title("📊 Relatório de Assuntos por LBL e Macro Tema")
st.markdown(
    """
    Selecione um LBL à esquerda — ou escolha **Todos** — para ver quantos assuntos estão associados,
    como eles se distribuem entre os macro temas, e outras análises.  
    Os gráficos são interativos via Plotly.
    """
)

with st.sidebar:
    st.header("🔎 Filtro de LBL")
    lbls_df = pd.read_sql(
        "SELECT id, lbl || ' - ' || nome AS label FROM lbl ORDER BY lbl", engine
    )
    all_option = {"id": 0, "label": "Todos"}
    lbls_list = pd.concat([pd.DataFrame([all_option]), lbls_df], ignore_index=True)
    choice = st.selectbox(
        "Selecione LBL:",
        options=lbls_list["label"].tolist(),
        format_func=lambda x: x,
    )
    lbl_id_map = dict(zip(lbls_list["label"], lbls_list["id"]))
    selected_lbl_id = lbl_id_map[choice]

@st.cache_data(ttl=60)
def get_assuntos_por_lbl():
    query = """
        SELECT
          l.id AS lbl_id,
          l.lbl || ' - ' || l.nome AS lbl_label,
          COUNT(al.assunto_id) AS total_assuntos
        FROM lbl AS l
        LEFT JOIN assunto_lbl AS al ON l.id = al.lbl_id
        GROUP BY l.id, lbl_label
        ORDER BY total_assuntos DESC
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=60)
def get_assuntos_por_macro():
    query = """
        SELECT
          mt.id AS macro_id,
          mt.macro_tema AS macro_label,
          COUNT(a.id) AS total_assuntos
        FROM macro_tema AS mt
        JOIN area AS ar ON mt.id = ar.macro_tema_id
        JOIN subarea AS s ON ar.id = s.area_id
        JOIN disciplina AS d ON s.id = d.subarea_id
        JOIN assunto AS a ON d.id = a.disciplina_id
        GROUP BY mt.id, macro_label
        ORDER BY total_assuntos DESC
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=60)
def get_macro_por_lbl(lbl_id: int):
    query = f"""
        SELECT
          mt.macro_tema AS macro_label,
          COUNT(a.id) AS total_assuntos
        FROM assunto_lbl AS al
        JOIN assunto AS a ON al.assunto_id = a.id
        JOIN disciplina AS d ON a.disciplina_id = d.id
        JOIN subarea AS s ON d.subarea_id = s.id
        JOIN area AS ar ON s.area_id = ar.id
        JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
        WHERE al.lbl_id = {lbl_id}
        GROUP BY mt.macro_tema
        ORDER BY total_assuntos DESC
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=60)
def get_tabela_assuntos_lbl(lbl_id: int):
    query = f"""
        SELECT
          a.assunto                       AS assunto,
          d.nome                          AS disciplina,
          s.subarea                       AS subarea,
          ar.area                         AS area,
          mt.macro_tema                   AS macro_tema
        FROM assunto_lbl AS al
        JOIN assunto AS a ON al.assunto_id = a.id
        JOIN disciplina AS d ON a.disciplina_id = d.id
        JOIN subarea AS s ON d.subarea_id = s.id
        JOIN area AS ar ON s.area_id = ar.id
        JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
        WHERE al.lbl_id = {lbl_id}
        ORDER BY mt.macro_tema, ar.area, s.subarea, d.nome, a.assunto
    """
    return pd.read_sql(query, engine)

if selected_lbl_id == 0:
    st.subheader("📋 Todos os LBLs: Quantidade de Assuntos Associados")
    df_lbl_counts = get_assuntos_por_lbl()
    fig1 = px.bar(
        df_lbl_counts,
        x="lbl_label",
        y="total_assuntos",
        labels={"lbl_label": "LBL", "total_assuntos": "Total de Assuntos"},
        title="Assuntos por LBL",
    )
    fig1.update_layout(xaxis_tickangle=0)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📋 Macro Temas: Quantidade Total de Assuntos")
    df_macro_counts = get_assuntos_por_macro()
    fig2 = px.bar(
        df_macro_counts,
        x="total_assuntos",
        y="macro_label",
        orientation="h",
        labels={"macro_label": "Macro Tema", "total_assuntos": "Total de Assuntos"},
        title="Assuntos por Macro Tema (Todos os LBLs)",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.write(
        "Selecione um LBL específico para ver o detalhamento por Macro Tema e lista de assuntos."
    )

else:
    lbl_label = choice
    st.subheader(f"📋 Análise para LBL: {lbl_label}")

    total_query = f"SELECT COUNT(*) AS total_assuntos FROM assunto_lbl WHERE lbl_id = {selected_lbl_id}"
    total_assuntos = pd.read_sql(total_query, engine)["total_assuntos"].iloc[0]
    st.metric(label="Total de Assuntos Neste LBL", value=int(total_assuntos))

    df_macro_lbl = get_macro_por_lbl(selected_lbl_id)
    if df_macro_lbl.empty:
        st.info("Este LBL ainda não possui assuntos associados.")
    else:
        fig3 = px.bar(
            df_macro_lbl,
            x="total_assuntos",
            y="macro_label",
            orientation="h",
            labels={"macro_label": "Macro Tema", "total_assuntos": "Total de Assuntos"},
            title="Distribuição de Assuntos por Macro Tema",
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("🗂️ Lista de Assuntos Associados")
        df_tabela = get_tabela_assuntos_lbl(selected_lbl_id)
        st.dataframe(df_tabela, use_container_width=True)

        top3 = df_macro_lbl.head(3)
        if not top3.empty:
            st.write("**Top 3 Macro Temas com mais Assuntos neste LBL:**")
            st.table(top3.rename(columns={"macro_label": "Macro Tema", "total_assuntos": "Assuntos"}))

# Novos gráficos consolidados
st.markdown("---")
st.subheader("🏷️ Áreas por Macro Tema")
df_macro_area = pd.read_sql(
    """
    SELECT
      mt.macro_tema AS macro_tema,
      COUNT(ar.id) AS total_areas
    FROM area AS ar
    JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
    GROUP BY mt.macro_tema
    ORDER BY total_areas DESC
    """,
    engine,
)
fig4 = px.bar(
    df_macro_area,
    x="total_areas",
    y="macro_tema",
    orientation="h",
    labels={"macro_tema": "Macro Tema", "total_areas": "Total de Áreas"},
    title="Total de Áreas por Macro Tema",
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📂 Subáreas por Área")
df_area_sub = pd.read_sql(
    """
    SELECT
      ar.area AS area,
      COUNT(s.id) AS total_subareas
    FROM subarea AS s
    JOIN area AS ar ON s.area_id = ar.id
    GROUP BY ar.area
    ORDER BY total_subareas DESC
    """,
    engine,
)
fig5 = px.bar(
    df_area_sub,
    x="total_subareas",
    y="area",
    orientation="h",
    labels={"area": "Área", "total_subareas": "Total de Subáreas"},
    title="Total de Subáreas por Área",
)
st.plotly_chart(fig5, use_container_width=True)

st.subheader("📑 Disciplinas por Subárea")
df_sub_disc = pd.read_sql(
    """
    SELECT
      s.subarea AS subarea,
      COUNT(d.id) AS total_disciplinas
    FROM disciplina AS d
    JOIN subarea AS s ON d.subarea_id = s.id
    GROUP BY s.subarea
    ORDER BY total_disciplinas DESC
    """,
    engine,
)
fig6 = px.bar(
    df_sub_disc,
    x="total_disciplinas",
    y="subarea",
    orientation="h",
    labels={"subarea": "Subárea", "total_disciplinas": "Total de Disciplinas"},
    title="Total de Disciplinas por Subárea",
)
st.plotly_chart(fig6, use_container_width=True)

st.subheader("📝 Assuntos por Disciplina")
df_disc_asm = pd.read_sql(
    """
    SELECT
      d.nome AS disciplina,
      COUNT(a.id) AS total_assuntos
    FROM assunto AS a
    JOIN disciplina AS d ON a.disciplina_id = d.id
    GROUP BY d.nome
    ORDER BY total_assuntos DESC
    """,
    engine,
)
fig7 = px.bar(
    df_disc_asm,
    x="total_assuntos",
    y="disciplina",
    orientation="h",
    labels={"disciplina": "Disciplina", "total_assuntos": "Total de Assuntos"},
    title="Total de Assuntos por Disciplina",
)
st.plotly_chart(fig7, use_container_width=True)
