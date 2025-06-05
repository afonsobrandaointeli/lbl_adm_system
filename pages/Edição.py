import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

from scripts.inserts import (
    insert_lbl,
    insert_macro_tema,
    insert_area,
    insert_subarea,
    insert_disciplina,
    insert_assunto,
    insert_assunto_lbl,
)
from scripts.queries import (
    get_macro_temas,
    get_areas_by_macro_tema,
    get_subareas_by_area,
    get_disciplinas_by_subarea,
    get_assuntos,
    get_lbls,
)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def update_lbl(lbl_id, lbl_num, nome, descricao):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE lbl
           SET lbl = %s,
               nome = %s,
               descricao = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (lbl_num, nome, descricao, lbl_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def update_macro_tema(mt_id, nome):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE macro_tema
           SET macro_tema = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (nome, mt_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def update_area(area_id, nome, mt_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE area
           SET area = %s,
               macro_tema_id = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (nome, mt_id, area_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def update_subarea(sub_id, nome, area_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE subarea
           SET subarea = %s,
               area_id = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (nome, area_id, sub_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def update_disciplina(disc_id, nome, sub_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE disciplina
           SET nome = %s,
               subarea_id = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (nome, sub_id, disc_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def update_assunto(assunto_id, nome, disc_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE assunto
           SET assunto = %s,
               disciplina_id = %s,
               timestamp = CURRENT_TIMESTAMP
         WHERE id = %s
        """,
        (nome, disc_id, assunto_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def fetch_lbls():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, lbl, nome, descricao FROM lbl ORDER BY lbl")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_macro_temas():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, macro_tema FROM macro_tema ORDER BY macro_tema")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_areas_with_macro():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ar.id, mt.macro_tema, ar.area, ar.macro_tema_id
          FROM area AS ar
          JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
         ORDER BY mt.macro_tema, ar.area
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_subareas_with_hierarchy():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id,
               mt.macro_tema,
               ar.area,
               s.subarea,
               s.area_id
          FROM subarea AS s
          JOIN area AS ar ON s.area_id = ar.id
          JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
         ORDER BY mt.macro_tema, ar.area, s.subarea
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_disciplinas_with_hierarchy():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT d.id,
               mt.macro_tema,
               ar.area,
               s.subarea,
               d.nome,
               d.subarea_id
          FROM disciplina AS d
          JOIN subarea AS s ON d.subarea_id = s.id
          JOIN area AS ar ON s.area_id = ar.id
          JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
         ORDER BY mt.macro_tema, ar.area, s.subarea, d.nome
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_assuntos_with_hierarchy():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.id,
               mt.macro_tema,
               ar.area,
               s.subarea,
               d.nome AS disciplina,
               a.assunto,
               a.disciplina_id
          FROM assunto AS a
          JOIN disciplina AS d ON a.disciplina_id = d.id
          JOIN subarea AS s ON d.subarea_id = s.id
          JOIN area AS ar ON s.area_id = ar.id
          JOIN macro_tema AS mt ON ar.macro_tema_id = mt.id
         ORDER BY mt.macro_tema, ar.area, s.subarea, d.nome, a.assunto
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

st.set_page_config(
    page_title="✏️ Sistema de Edição Hierárquica",
    page_icon="🖊️",
    layout="wide",
)
st.title("✏️ Sistema de Edição Hierárquica")
st.markdown("Selecione o registro que deseja editar em cada aba e altere os campos.")

tabs = st.tabs(
    [
        "✏️ Editar LBL",
        "✏️ Editar Macro Tema",
        "✏️ Editar Área",
        "✏️ Editar Subárea",
        "✏️ Editar Disciplina",
        "✏️ Editar Assunto",
    ]
)

with tabs[0]:
    st.header("✏️ Editar LBL")
    lbls = fetch_lbls()
    if lbls:
        options = {f"{row[1]} - {row[2]}": row for row in lbls}
        selecionado = st.selectbox(
            "Selecione LBL para editar:",
            options=list(options.keys())
        )
        lbl_id, lbl_num, lbl_nome, lbl_desc = options[selecionado]
        with st.form("form_edit_lbl", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                novo_num = st.number_input(
                    "Número do LBL:", min_value=1, step=1, value=lbl_num
                )
                novo_nome = st.text_input("Nome do LBL:", value=lbl_nome)
            with col2:
                nova_desc = st.text_area(
                    "Descrição do LBL:", value=lbl_desc if lbl_desc else ""
                )
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome do LBL não pode ficar vazio.")
                else:
                    update_lbl(lbl_id, novo_num, novo_nome.strip(), nova_desc.strip() or None)
                    st.success("✔️ LBL atualizado com sucesso.")
    else:
        st.info("Nenhum LBL cadastrado ainda.")

with tabs[1]:
    st.header("✏️ Editar Macro Tema")
    mts = fetch_macro_temas()
    if mts:
        options = {row[1]: row for row in mts}
        selecionado = st.selectbox(
            "Selecione Macro Tema para editar:",
            options=list(options.keys())
        )
        mt_id, mt_nome = options[selecionado]
        with st.form("form_edit_mt", clear_on_submit=False):
            novo_nome = st.text_input("Nome do Macro Tema:", value=mt_nome)
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome do Macro Tema não pode ficar vazio.")
                else:
                    update_macro_tema(mt_id, novo_nome.strip())
                    st.success("✔️ Macro Tema atualizado com sucesso.")
    else:
        st.info("Nenhum Macro Tema cadastrado ainda.")

with tabs[2]:
    st.header("✏️ Editar Área")
    areas = fetch_areas_with_macro()
    if areas:
        options = {f"{row[1]} – {row[2]}": (row[0], row[3], row[2]) for row in areas}
        selecionado = st.selectbox(
            "Selecione Área para editar:",
            options=list(options.keys())
        )
        area_id, mt_id_atual, area_nome_atual = options[selecionado]
        macro_temas = fetch_macro_temas()
        with st.form("form_edit_area", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome da Área:", value=area_nome_atual)
            with col2:
                mt_options = {mt[1]: mt[0] for mt in macro_temas}
                novo_mt = st.selectbox(
                    "Macro Tema pai:", options=list(mt_options.keys()), index=list(mt_options.values()).index(mt_id_atual)
                )
                novo_mt_id = mt_options[novo_mt]
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome da Área não pode ficar vazio.")
                else:
                    update_area(area_id, novo_nome.strip(), novo_mt_id)
                    st.success("✔️ Área atualizada com sucesso.")
    else:
        st.info("Nenhuma Área cadastrada ainda.")

with tabs[3]:
    st.header("✏️ Editar Subárea")
    subs = fetch_subareas_with_hierarchy()
    areas = fetch_areas_with_macro()
    if subs:
        options = {
            f"{row[1]} – {row[2]} – {row[3]}": (row[0], row[4], row[3])
            for row in subs
        }
        selecionado = st.selectbox(
            "Selecione Subárea para editar:",
            options=list(options.keys())
        )
        sub_id, area_id_atual, sub_nome_atual = options[selecionado]
        areas_com_macro = [(r[0], f"{r[1]} – {r[2]}") for r in areas]
        with st.form("form_edit_subarea", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome da Subárea:", value=sub_nome_atual)
            with col2:
                area_options = {label: aid for aid, label in areas_com_macro}
                current_label = next(label for aid, label in areas_com_macro if aid == area_id_atual)
                novo_area_label = st.selectbox(
                    "Área pai:", options=list(area_options.keys()), index=list(area_options.keys()).index(current_label)
                )
                novo_area_id = area_options[novo_area_label]
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome da Subárea não pode ficar vazio.")
                else:
                    update_subarea(sub_id, novo_nome.strip(), novo_area_id)
                    st.success("✔️ Subárea atualizada com sucesso.")
    else:
        st.info("Nenhuma Subárea cadastrada ainda.")

with tabs[4]:
    st.header("✏️ Editar Disciplina")
    discs = fetch_disciplinas_with_hierarchy()
    if discs:
        options = {
            f"{row[1]} – {row[2]} – {row[3]} – {row[4]}": (row[0], row[5], row[4])
            for row in discs
        }
        selecionado = st.selectbox(
            "Selecione Disciplina para editar:",
            options=list(options.keys())
        )
        disc_id, sub_id_atual, disc_nome_atual = options[selecionado]
        subareas_completo = [
            (r[0], f"{r[1]} – {r[2]} – {r[3]}") for r in subs
        ]
        with st.form("form_edit_disciplina", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome da Disciplina:", value=disc_nome_atual)
            with col2:
                sub_options = {label: sid for sid, label in subareas_completo}
                current_label = next(label for sid, label in subareas_completo if sid == sub_id_atual)
                novo_sub_label = st.selectbox(
                    "Subárea pai:", options=list(sub_options.keys()), index=list(sub_options.keys()).index(current_label)
                )
                novo_sub_id = sub_options[novo_sub_label]
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome da Disciplina não pode ficar vazio.")
                else:
                    update_disciplina(disc_id, novo_nome.strip(), novo_sub_id)
                    st.success("✔️ Disciplina atualizada com sucesso.")
    else:
        st.info("Nenhuma Disciplina cadastrada ainda.")

with tabs[5]:
    st.header("✏️ Editar Assunto")
    assuntos = fetch_assuntos_with_hierarchy()
    if assuntos:
        options = {
            f"{row[1]} – {row[2]} – {row[3]} – {row[4]} – {row[5]}": (row[0], row[6], row[5])
            for row in assuntos
        }
        selecionado = st.selectbox(
            "Selecione Assunto para editar:",
            options=list(options.keys())
        )
        assunto_id, disc_id_atual, assunto_nome_atual = options[selecionado]
        disciplinas_completo = [
            (r[0], f"{r[1]} – {r[2]} – {r[3]} – {r[4]}") for r in discs
        ]
        with st.form("form_edit_assunto", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome do Assunto:", value=assunto_nome_atual)
            with col2:
                disc_options = {label: did for did, label in disciplinas_completo}
                current_label = next(label for did, label in disciplinas_completo if did == disc_id_atual)
                novo_disc_label = st.selectbox(
                    "Disciplina pai:", options=list(disc_options.keys()), index=list(disc_options.keys()).index(current_label)
                )
                novo_disc_id = disc_options[novo_disc_label]
            submit = st.form_submit_button("💾 Salvar Alterações")
            if submit:
                if not novo_nome.strip():
                    st.error("O nome do Assunto não pode ficar vazio.")
                else:
                    update_assunto(assunto_id, novo_nome.strip(), novo_disc_id)
                    st.success("✔️ Assunto atualizado com sucesso.")
    else:
        st.info("Nenhum Assunto cadastrado ainda.")

st.markdown("---")
st.markdown("*Página de edição hierárquica com Streamlit*")
