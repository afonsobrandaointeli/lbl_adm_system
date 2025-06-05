import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

st.set_page_config(page_title="🔍 Verificação de Macro Temas e Assuntos", layout="wide")
st.title("📊 Diagnóstico: Macro Temas e Assuntos Não Contemplados")

# Conexão com o banco
@st.cache_resource
def get_connection():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Erro na conexão com o banco de dados: {e}")
        return None

engine = get_connection()

def carregar_macro_temas_nao_contemplados():
    query = """
        SELECT mt.id, mt.macro_tema, mt.timestamp
        FROM macro_tema mt
        LEFT JOIN area a ON a.macro_tema_id = mt.id
        WHERE a.id IS NULL;
    """
    return pd.read_sql(query, engine)

def carregar_assuntos_sem_lbl():
    query = """
        SELECT ass.id, ass.assunto, d.nome AS disciplina, sa.subarea, ar.area, mt.macro_tema
        FROM assunto ass
        LEFT JOIN assunto_lbl al ON ass.id = al.assunto_id
        INNER JOIN disciplina d ON ass.disciplina_id = d.id
        INNER JOIN subarea sa ON d.subarea_id = sa.id
        INNER JOIN area ar ON sa.area_id = ar.id
        INNER JOIN macro_tema mt ON ar.macro_tema_id = mt.id
        WHERE al.lbl_id IS NULL;
    """
    return pd.read_sql(query, engine)

# Interface
st.header("📌 Macro Temas sem nenhuma Área vinculada")
df_macro_nao_contemplado = carregar_macro_temas_nao_contemplados()
st.dataframe(df_macro_nao_contemplado, use_container_width=True)
st.caption(f"🔴 Total de macro temas não contemplados: {len(df_macro_nao_contemplado)}")

st.divider()

st.header("📌 Assuntos sem vínculo com nenhum LBL")
df_assuntos_sem_lbl = carregar_assuntos_sem_lbl()
st.dataframe(df_assuntos_sem_lbl, use_container_width=True)
st.caption(f"🟠 Total de assuntos sem vínculo com LBLs: {len(df_assuntos_sem_lbl)}")

st.divider()

st.header("📋 Quantidade Total de Assuntos por Macro Tema")

def carregar_total_assuntos_por_macro_tema():
    query = """
        SELECT
            mt.macro_tema,
            COUNT(a.id) AS total_assuntos
        FROM macro_tema mt
        LEFT JOIN area ar ON mt.id = ar.macro_tema_id
        LEFT JOIN subarea sa ON ar.id = sa.area_id
        LEFT JOIN disciplina d ON sa.id = d.subarea_id
        LEFT JOIN assunto a ON d.id = a.disciplina_id
        GROUP BY mt.macro_tema
        ORDER BY total_assuntos DESC;
    """
    return pd.read_sql(query, engine)

# Carregar e exibir a tabela
df_total_assuntos_macro = carregar_total_assuntos_por_macro_tema()
st.dataframe(df_total_assuntos_macro, use_container_width=True)

# Exibir total global
st.caption(f"🔵 Total global de assuntos cadastrados: {df_total_assuntos_macro['total_assuntos'].sum()}")
