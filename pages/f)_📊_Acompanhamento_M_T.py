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

# Interface
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
