import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

st.set_page_config(page_title="Assuntos sem LBL", page_icon="📋", layout="wide")
st.title("📋 Assuntos ainda não associados a nenhum LBL")

@st.cache_resource
def connect():
    if not DATABASE_URL:
        st.error("❌ DATABASE_URL não definida no .env")
        st.stop()
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        st.stop()

conn = connect()

query = """
    SELECT 
        a.id AS assunto_id,
        a.assunto,
        d.nome AS disciplina,
        s.subarea,
        ar.area,
        mt.macro_tema
    FROM assunto a
    JOIN disciplina d ON a.disciplina_id = d.id
    JOIN subarea s ON d.subarea_id = s.id
    JOIN area ar ON s.area_id = ar.id
    JOIN macro_tema mt ON ar.macro_tema_id = mt.id
    LEFT JOIN assunto_lbl al ON a.id = al.assunto_id
    WHERE al.lbl_id IS NULL
    ORDER BY mt.macro_tema, ar.area, s.subarea, d.nome, a.assunto;
"""

try:
    df = pd.read_sql(query, conn)
    if df.empty:
        st.success("🎉 Todos os assuntos estão associados a pelo menos um LBL!")
    else:
        st.warning(f"⚠️ Foram encontrados {len(df)} assuntos sem LBL associado.")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", csv, "assuntos_sem_lbl.csv", "text/csv")
except Exception as e:
    st.error(f"Erro ao consultar o banco: {e}")
finally:
    conn.close()
