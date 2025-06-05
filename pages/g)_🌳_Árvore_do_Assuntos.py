import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Conexão com o banco de dados
@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# Carregar assuntos
def carregar_assuntos():
    query = """
        SELECT id, assunto FROM assunto ORDER BY assunto
    """
    return pd.read_sql(query, engine)

# Carregar árvore hierárquica
def carregar_arvore(assunto_id):
    query = f"""
        SELECT
            ass.assunto,
            d.nome AS disciplina,
            sa.subarea,
            ar.area,
            mt.macro_tema
        FROM assunto ass
        INNER JOIN disciplina d ON ass.disciplina_id = d.id
        INNER JOIN subarea sa ON d.subarea_id = sa.id
        INNER JOIN area ar ON sa.area_id = ar.id
        INNER JOIN macro_tema mt ON ar.macro_tema_id = mt.id
        WHERE ass.id = {assunto_id}
    """
    return pd.read_sql(query, engine).iloc[0]

# Página Streamlit
st.title("🌳 Visualização da Hierarquia: Assunto até Macro Tema")

# Escolha do Assunto
assuntos_df = carregar_assuntos()
assunto_selecionado = st.selectbox("Selecione um assunto:", assuntos_df["assunto"])
assunto_id = assuntos_df.loc[assuntos_df["assunto"] == assunto_selecionado, "id"].iloc[0]

# Carrega a hierarquia
hierarquia = carregar_arvore(assunto_id)

# Exibição textual da hierarquia
st.markdown(f"""
### 📌 Hierarquia Completa:

- **Macro Tema:** {hierarquia['macro_tema']}
  - **Área:** {hierarquia['area']}
    - **Subárea:** {hierarquia['subarea']}
      - **Disciplina:** {hierarquia['disciplina']}
        - **Assunto:** {hierarquia['assunto']}
""")
