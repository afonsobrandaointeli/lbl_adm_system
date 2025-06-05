import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Importar funções de inserts e queries dos módulos em scripts/
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

# Carrega variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# Função auxiliar para construir lista de áreas no formato "Macro Tema – Área"
def build_areas_with_macro():
    choices = []
    for mt_id, mt_name in get_macro_temas():
        for area_id, area_name in get_areas_by_macro_tema(mt_id):
            choices.append((area_id, f"{mt_name} – {area_name}"))
    return choices


# Função auxiliar para construir lista de subáreas no formato "Macro Tema – Área – Subárea"
def build_subareas_with_area_macro():
    choices = []
    for mt_id, mt_name in get_macro_temas():
        for area_id, area_name in get_areas_by_macro_tema(mt_id):
            for sub_id, sub_name in get_subareas_by_area(area_id):
                choices.append((sub_id, f"{mt_name} – {area_name} – {sub_name}"))
    return choices


# --- STREAMLIT APP ---
st.set_page_config(
    page_title="📚 Sistema de Cadastro Hierárquico",
    page_icon="📖",
    layout="wide",
)
st.title("📚 Sistema de Cadastro Hierárquico")

tabs = st.tabs(
    [
        "🏷️ LBL",
        "🎯 Macro Tema",
        "📖 Área",
        "📝 Subárea",
        "📚 Disciplina",
        "📄 Assunto",
        "🔗 Associar Assunto-LBL",
    ]
)

# ---- ABA 1: LBL ----
with tabs[0]:
    st.header("🏷️ Cadastrar LBL")
    with st.form("form_lbl", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            lbl_numero = st.number_input(
                "Número do LBL:",
                min_value=1,
                step=1,
                help="Número único que identifica este LBL",
            )
            lbl_nome = st.text_input(
                "Nome do LBL:",
                placeholder="Ex: Matemática Básica",
                help="Nome descritivo do LBL",
            )
        with col2:
            lbl_descricao = st.text_area(
                "Descrição do LBL:",
                placeholder="Descreva detalhadamente o que este LBL representa…",
                help="Texto explicativo sobre o LBL",
                height=100,
            )
        submitted_lbl = st.form_submit_button("✅ Cadastrar LBL")
        if submitted_lbl:
            if not lbl_nome.strip():
                st.error("⚠️ O nome do LBL é obrigatório!")
            else:
                sucesso = insert_lbl(
                    lbl_numero,
                    lbl_nome.strip(),
                    lbl_descricao.strip() if lbl_descricao else None,
                )
                if sucesso:
                    st.success("✅ LBL cadastrado com sucesso!")

    st.subheader("📋 LBLs Cadastrados")
    lbls_cadastrados = get_lbls()
    if lbls_cadastrados:
        df_lbl = pd.DataFrame(
            lbls_cadastrados, columns=["ID", "LBL", "Nome", "Descrição"]
        )
        st.dataframe(df_lbl, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum LBL cadastrado ainda.")


# ---- ABA 2: Macro Tema ----
with tabs[1]:
    st.header("🎯 Cadastrar Macro Tema")
    with st.form("form_macro_tema", clear_on_submit=True):
        macro_tema_nome = st.text_input(
            "Nome do Macro Tema:",
            placeholder="Ex: Ciências Exatas",
            help="Nome do macro tema",
        )
        submitted_macro = st.form_submit_button("✅ Cadastrar Macro Tema")
        if submitted_macro:
            if not macro_tema_nome.strip():
                st.error("⚠️ O nome do Macro Tema é obrigatório!")
            else:
                sucesso = insert_macro_tema(macro_tema_nome.strip())
                if sucesso:
                    st.success("✅ Macro Tema cadastrado com sucesso!")

    st.subheader("📋 Macro Temas Cadastrados")
    macro_temas_cadastrados = get_macro_temas()
    if macro_temas_cadastrados:
        df_macro = pd.DataFrame(
            macro_temas_cadastrados, columns=["ID", "Macro Tema"]
        )
        st.dataframe(df_macro, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum Macro Tema cadastrado ainda.")


# ---- ABA 3: Área ----
with tabs[2]:
    st.header("📖 Cadastrar Área")
    macro_temas = get_macro_temas()
    if macro_temas:
        with st.form("form_area", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                macro_tema_selecionado = st.selectbox(
                    "Selecione o Macro Tema:",
                    options=macro_temas,
                    format_func=lambda x: x[1],
                    key="macro_para_area",
                )
            with col2:
                area_nome = st.text_input(
                    "Nome da Área:",
                    placeholder="Ex: Matemática",
                    help="Nome da área",
                )
            submitted_area = st.form_submit_button("✅ Cadastrar Área")
            if submitted_area:
                if not area_nome.strip():
                    st.error("⚠️ O nome da Área é obrigatório!")
                else:
                    sucesso = insert_area(
                        area_nome.strip(), macro_tema_selecionado[0]
                    )
                    if sucesso:
                        st.success("✅ Área cadastrada com sucesso!")
    else:
        st.info("📝 Cadastre pelo menos um Macro Tema primeiro.")

    st.subheader("📋 Áreas Cadastradas (Macro Tema – Área)")
    all_areas = build_areas_with_macro()
    if all_areas:
        df_areas = pd.DataFrame(all_areas, columns=["Área_ID", "Macro Tema – Área"])
        st.dataframe(df_areas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma Área cadastrada ainda.")


# ---- ABA 4: Subárea ----
with tabs[3]:
    st.header("📝 Cadastrar Subárea")
    areas_com_macro = build_areas_with_macro()

    if areas_com_macro:
        with st.form("form_subarea", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                area_selecionada = st.selectbox(
                    "Selecione a Área (Macro Tema – Área):",
                    options=areas_com_macro,
                    format_func=lambda x: x[1],
                    key="area_para_subarea",
                )
            with col2:
                subarea_nome = st.text_input(
                    "Nome da Subárea:",
                    placeholder="Ex: Marketing Digital",
                    help="Nome da subárea",
                )
            submitted_subarea = st.form_submit_button("✅ Cadastrar Subárea")
            if submitted_subarea:
                if not subarea_nome.strip():
                    st.error("⚠️ O nome da Subárea é obrigatório!")
                else:
                    sucesso = insert_subarea(
                        subarea_nome.strip(), area_selecionada[0]
                    )
                    if sucesso:
                        st.success("✅ Subárea cadastrada com sucesso!")
    else:
        st.info("📝 Cadastre pelo menos uma Área primeiro.")

    st.subheader("📋 Subáreas Cadastradas")
    registro_subs = []
    for area_id, label in areas_com_macro:
        for sub_id, sub_name in get_subareas_by_area(area_id):
            registro_subs.append((sub_id, sub_name, label))
    if registro_subs:
        df_subs = pd.DataFrame(
            registro_subs, columns=["ID", "Subárea", "Macro Tema – Área"]
        )
        st.dataframe(df_subs, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma Subárea cadastrada ainda.")


# ---- ABA 5: Disciplina ----
with tabs[4]:
    st.header("📚 Cadastrar Disciplina")
    subareas_completo = build_subareas_with_area_macro()

    if subareas_completo:
        with st.form("form_disciplina", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                subarea_selecionada = st.selectbox(
                    "Selecione a Subárea (Macro Tema – Área – Subárea):",
                    options=subareas_completo,
                    format_func=lambda x: x[1],
                    key="subarea_para_disciplina",
                )
            with col2:
                disciplina_nome = st.text_input(
                    "Nome da Disciplina:",
                    placeholder="Ex: Geometria Avançada",
                    help="Nome detalhado da disciplina",
                )
            submitted_disciplina = st.form_submit_button("✅ Cadastrar Disciplina")
            if submitted_disciplina:
                if not disciplina_nome.strip():
                    st.error("⚠️ O nome da Disciplina é obrigatório!")
                else:
                    sucesso = insert_disciplina(
                        disciplina_nome.strip(), subarea_selecionada[0]
                    )
                    if sucesso:
                        st.success("✅ Disciplina cadastrada com sucesso!")
    else:
        st.info("📝 Cadastre pelo menos uma Subárea primeiro.")

    st.subheader("📋 Disciplinas Cadastradas")
    todos_registros = []
    for sub_id, label in subareas_completo:
        for disc_id, disc_name in get_disciplinas_by_subarea(sub_id):
            todos_registros.append((disc_id, disc_name, label))
    if todos_registros:
        df_disc = pd.DataFrame(
            todos_registros, columns=["ID", "Disciplina", "Macro Tema – Área – Subárea"]
        )
        st.dataframe(df_disc, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma Disciplina cadastrada ainda.")


# ---- ABA 6: Assunto ----
with tabs[5]:
    st.header("📄 Cadastrar Assunto")

    # Pré-carregar hierarquia para a seleção em cascata
    macro_temas = get_macro_temas()
    selected_macro = st.selectbox(
        "Macro Tema:",
        options=macro_temas,
        format_func=lambda x: x[1],
        key="macro_para_assunto",
    )

    # Carregar áreas do macro tema selecionado
    areas_ass = get_areas_by_macro_tema(selected_macro[0]) if selected_macro else []
    selected_area = None
    if areas_ass:
        selected_area = st.selectbox(
            "Área:",
            options=areas_ass,
            format_func=lambda x: x[1],
            key="area_para_assunto",
        )

    # Carregar subáreas da área selecionada
    subareas_ass = []
    selected_subarea = None
    if selected_area:
        subareas_ass = get_subareas_by_area(selected_area[0])
        if subareas_ass:
            selected_subarea = st.selectbox(
                "Subárea:",
                options=subareas_ass,
                format_func=lambda x: x[1],
                key="subarea_para_assunto",
            )

    # Carregar disciplinas da subárea selecionada
    disciplinas_ass = []
    selected_disciplina = None
    if selected_subarea:
        disciplinas_ass = get_disciplinas_by_subarea(selected_subarea[0])
        if disciplinas_ass:
            selected_disciplina = st.selectbox(
                "Disciplina:",
                options=disciplinas_ass,
                format_func=lambda x: x[1],
                key="disciplina_para_assunto",
            )

    # Input de nome do assunto
    assunto_nome = st.text_input(
        "Nome do Assunto:",
        placeholder="Ex: Equações Diferenciais",
        help="Nome detalhado do assunto",
    )

    # Botão de cadastro fora de formulário para atualizar cascata corretamente
    if st.button("✅ Cadastrar Assunto"):
        if not assunto_nome.strip():
            st.error("⚠️ O nome do Assunto é obrigatório!")
        elif not selected_disciplina:
            st.error("⚠️ Selecione uma Disciplina!")
        else:
            sucesso = insert_assunto(assunto_nome.strip(), selected_disciplina[0])
            if sucesso:
                st.success("✅ Assunto cadastrado com sucesso!")

    # Exibir hierarquia e lista de assuntos
    st.subheader("📋 Assuntos Cadastrados")
    # Montar registros para exibição: Assunto → Disciplina → Subárea → Área → Macro Tema
    registros_assuntos = []
    for ass_id, ass_text, disciplina, subarea, area, macro in get_assuntos():
        registros_assuntos.append(
            (ass_id, ass_text, disciplina, subarea, area, macro)
        )
    if registros_assuntos:
        df_assuntos = pd.DataFrame(
            registros_assuntos,
            columns=["ID", "Assunto", "Disciplina", "Subárea", "Área", "Macro Tema"],
        )
        st.dataframe(df_assuntos, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum Assunto cadastrado ainda.")


# ---- ABA 7: Associar Assunto-LBL ----
with tabs[6]:
    st.header("🔗 Associar Assunto ao LBL")
    assuntos = get_assuntos()
    lbls = get_lbls()

    if assuntos and lbls:
        with st.form("form_associacao", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                assunto_selecionado = st.selectbox(
                    "Selecione o Assunto:",
                    options=assuntos,
                    format_func=lambda x: f"{x[1]} ({x[2]} ▸ {x[3]} ▸ {x[4]} ▸ {x[5]})",
                )

            with col2:
                lbl_selecionado = st.selectbox(
                    "Selecione o LBL:",
                    options=lbls,
                    format_func=lambda x: f"LBL {x[1]} - {x[2]}",
                )
                if lbl_selecionado and lbl_selecionado[3]:
                    st.info(f"**Descrição do LBL:** {lbl_selecionado[3]}")

            submitted_associacao = st.form_submit_button("🔗 Criar Associação")
            if submitted_associacao:
                sucesso = insert_assunto_lbl(
                    assunto_selecionado[0], lbl_selecionado[0]
                )
                if sucesso:
                    st.success("✅ Associação criada com sucesso!")
    else:
        if not assuntos:
            st.info("📝 Cadastre pelo menos um Assunto primeiro.")
        if not lbls:
            st.info("📝 Cadastre pelo menos um LBL primeiro.")

# Rodapé
st.markdown("---")
st.markdown("*Sistema de cadastro hierárquico com PostgreSQL e Streamlit*")
