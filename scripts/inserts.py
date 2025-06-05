# scripts/inserts.py
import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def insert_lbl(lbl_num, nome, descricao):
    """Insere um novo LBL com descrição."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lbl (lbl, nome, descricao) VALUES (%s, %s, %s)",
            (lbl_num, nome, descricao),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir LBL: {e}")
        return False


def insert_macro_tema(macro_tema):
    """Insere um novo macro tema."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO macro_tema (macro_tema) VALUES (%s)", (macro_tema,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir Macro Tema: {e}")
        return False


def insert_area(area, macro_tema_id):
    """Insere uma nova área."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO area (area, macro_tema_id) VALUES (%s, %s)",
            (area, macro_tema_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir Área: {e}")
        return False


def insert_subarea(subarea, area_id):
    """Insere uma nova subárea."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO subarea (subarea, area_id) VALUES (%s, %s)",
            (subarea, area_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir Subárea: {e}")
        return False


def insert_disciplina(nome, subarea_id):
    """Insere uma nova disciplina."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO disciplina (nome, subarea_id) VALUES (%s, %s)",
            (nome, subarea_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir Disciplina: {e}")
        return False


def insert_assunto(nome, disciplina_id):
    """Insere um novo assunto."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO assunto (assunto, disciplina_id) VALUES (%s, %s)",
            (nome, disciplina_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir Assunto: {e}")
        return False


def insert_assunto_lbl(assunto_id, lbl_id):
    """Associa um assunto a um LBL."""
    if not DATABASE_URL:
        st.error("Variável DATABASE_URL não encontrada no .env")
        return False
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO assunto_lbl (assunto_id, lbl_id) VALUES (%s, %s)",
            (assunto_id, lbl_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao associar Assunto-LBL: {e}")
        return False
