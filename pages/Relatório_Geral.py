import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

st.set_page_config(
    page_title="📑 Tabela Hierárquica Completa",
    page_icon="📋",
    layout="wide",
)

st.title("📑 Tabela Hierárquica Completa")

query = """
SELECT
  mt.macro_tema AS macro_tema,
  ar.area AS area,
  s.subarea AS subarea,
  d.nome AS disciplina,
  a.assunto AS assunto,
  COALESCE('LBL ' || l.lbl || ' - ' || l.nome, '') AS lbl
FROM assunto AS a
JOIN disciplina AS d ON a.disciplina_id = d.id
JOIN subarea AS s ON d.subarea_id = s.id
JOIN area AS ar ON s.area_id = ar.id
JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
LEFT JOIN assunto_lbl AS al ON a.id = al.assunto_id
LEFT JOIN lbl AS l ON al.lbl_id = l.id
ORDER BY
  mt.macro_tema,
  ar.area,
  s.subarea,
  d.nome,
  a.assunto,
  l.lbl
"""

df = pd.read_sql(query, engine)
st.dataframe(df, use_container_width=True)
