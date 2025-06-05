# scripts/queries.py
import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


@st.cache_data(ttl=60)
def get_macro_temas():
    """Recupera todos os macro temas."""
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, macro_tema FROM macro_tema ORDER BY macro_tema")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar Macro Temas: {e}")
        return []


@st.cache_data(ttl=60)
def get_areas_by_macro_tema(macro_tema_id):
    """Recupera áreas por macro tema."""
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, area FROM area WHERE macro_tema_id = %s ORDER BY area",
            (macro_tema_id,),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar Áreas: {e}")
        return []


@st.cache_data(ttl=60)
def get_subareas_by_area(area_id):
    """Recupera subáreas por área."""
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, subarea FROM subarea WHERE area_id = %s ORDER BY subarea",
            (area_id,),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar Subáreas: {e}")
        return []


@st.cache_data(ttl=60)
def get_disciplinas_by_subarea(subarea_id):
    """Recupera disciplinas por subárea."""
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nome FROM disciplina WHERE subarea_id = %s ORDER BY nome",
            (subarea_id,),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar Disciplinas: {e}")
        return []


@st.cache_data(ttl=60)
def get_assuntos():
    """
    Recupera todos os assuntos com hierarquia completa:
    assunto → disciplina → subárea → área → macro_tema
    """
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = """
            SELECT
                a.id,
                a.assunto,
                d.nome        AS disciplina,
                s.subarea     AS subarea,
                ar.area       AS area,
                mt.macro_tema AS macro_tema
            FROM assunto a
            JOIN disciplina d ON a.disciplina_id = d.id
            JOIN subarea s   ON d.subarea_id     = s.id
            JOIN area ar     ON s.area_id        = ar.id
            JOIN macro_tema mt ON ar.macro_tema_id = mt.id
            ORDER BY mt.macro_tema, ar.area, s.subarea, d.nome, a.assunto
        """
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar Assuntos: {e}")
        return []


@st.cache_data(ttl=60)
def get_lbls():
    """Recupera todos os LBLs com descrição."""
    if not DATABASE_URL:
        return []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, lbl, nome, descricao FROM lbl ORDER BY lbl")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao buscar LBLs: {e}")
        return []
