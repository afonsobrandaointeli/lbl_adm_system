# Macro_Tema_DCN.py
"""
Streamlit app explicativo que apresenta os 15 macro‑temas previstos pela
Resolução CNE/CES nº 5/2021 para o Bacharelado em Administração, organizados
pelos três eixos formativos: Formação Básica, Formação Profissional e Integração
Extensão‑Pesquisa‑Prática.

Execução
========
$ streamlit run Macro_Tema_DCN.py

O aplicativo mostra uma visão geral da DCN 2021, a carga horária mínima e um
expander para **cada macro‑tema em linha única (vertical)**, facilitando a
leitura conforme solicitado.
"""

import streamlit as st

# -----------------------------------------------------------------------------
# Configuração da página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Macro‑Temas da DCN Administração (2021)",
    page_icon="📚",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Estrutura de dados dos eixos e macro‑temas
# -----------------------------------------------------------------------------
EIXOS = {
    "Formação Básica": [1, 2, 3, 4],
    "Formação Profissional": [5, 6, 7, 8, 9, 10, 12],
    "Integração Extensão‑Pesquisa‑Prática": [11, 13, 14, 15],
}

MACRO_TEMAS = {
    1: (
        "Fundamentos das Ciências Sociais, Humanas e Éticas",
        "Compreende filosofia, sociologia, psicologia, ética, cidadania e diversidade cultural, dando base crítica ao pensamento administrativo.",
    ),
    2: (
        "Economia e Ambiente Macrossocial",
        "Abrange micro e macroeconomia, economia internacional, políticas públicas e análise de conjuntura, essenciais para decisões estratégicas e de mercado.",
    ),
    3: (
        "Contabilidade, Finanças e Análise de Investimentos",
        "Inclui contabilidade societária, custos, controladoria, finanças corporativas, mercados financeiros e valuation, sustentando a saúde econômico‑financeira das organizações.",
    ),
    4: (
        "Métodos Quantitativos, Estatística e Modelagem de Dados",
        "Envolve estatística aplicada, econometria, pesquisa operacional, Big Data e métodos para tomada de decisão baseada em evidências.",
    ),
    5: (
        "Marketing, Vendas e Relações com o Mercado",
        "Trata de comportamento do consumidor, inteligência de mercado, comunicação, branding e canais digitais, visando a criação e a captura de valor.",
    ),
    6: (
        "Gestão de Pessoas e Comportamento Organizacional",
        "Integra atração, desenvolvimento, desempenho, cultura, liderança e relações de trabalho, enfatizando competências socioemocionais.",
    ),
    7: (
        "Operações, Logística e Cadeia de Suprimentos",
        "Cobre gestão de processos, qualidade, manufatura enxuta, SCM e serviços, relacionando produtividade a sustentabilidade.",
    ),
    8: (
        "Sistemas de Informação e Transformação Digital",
        "Explora ERP, BI, analytics, cibersegurança, Governança de TI e impactos de IA, conformando o pilar tecnológico exigido pela DCN.",
    ),
    9: (
        "Estratégia, Planejamento e Governança Corporativa",
        "Abrange formulação e implementação de estratégias, análise competitiva, governança, compliance e gestão de riscos.",
    ),
    10: (
        "Empreendedorismo, Inovação e Modelos de Negócio",
        "Inclui criação de startups, design thinking, lean startup, propriedade intelectual e gestão de portfólios de inovação.",
    ),
    11: (
        "Sustentabilidade, ESG e Responsabilidade Socioambiental",
        "Integra gestão ambiental, contabilidade socioambiental, ODS/Agenda 2030, governança ESG e ética nos negócios.",
    ),
    12: (
        "Projetos, Processos e Metodologias Ágeis",
        "Contempla PMBOK, SCRUM, Kanban, gestão de portfólios e melhoria contínua de processos organizacionais.",
    ),
    13: (
        "Pesquisa Científica e Metodologia Aplicada",
        "Abrange epistemologia, métodos qualitativos/quantitativos, elaboração de TCC e produção de artigos, garantindo rigor acadêmico.",
    ),
    14: (
        "Estágio Supervisionado e Vivências Profissionais",
        "Prevê, conforme a DCN, pelo menos 400 h de estágio articulado ao projeto integrador e às demandas regionais de mercado.",
    ),
    15: (
        "Extensão Universitária, Projetos Integradores e Internacionalização",
        "Engloba ações de impacto social, incubadoras, consultorias juniores, intercâmbios e atividades extensionistas que devem compor no mínimo 10 % da carga horária total.",
    ),
}

# -----------------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------------
st.title("📚 Macro‑Temas da DCN 2021 – Administração")

st.markdown(
    """
A **Resolução CNE/CES n.º 5/2021** estabelece as Diretrizes Curriculares Nacionais do
Bacharelado em Administração. São exigidas **3 000 h** mínimas, com **≥ 400 h** de
estágio supervisionado e **≥ 10 %** em atividades de extensão, estruturadas em
três eixos formativos.
"""
)

with st.expander("ℹ️ Entenda os três eixos", expanded=False):
    st.markdown(
        """
* **Formação Básica** – fundamentos humanísticos, econômicos e quantitativos.
* **Formação Profissional** – competências funcionais da Administração.
* **Integração Extensão‑Pesquisa‑Prática** – teoria aplicada a problemas reais
  via projetos, estágios e ações de impacto social.
"""
    )

st.divider()

# -----------------------------------------------------------------------------
# Exibir cada macro‑tema em linha (um abaixo do outro)
# -----------------------------------------------------------------------------
for eixo, ids in EIXOS.items():
    st.subheader(f"🔸 {eixo}")
    for tema_id in ids:
        nome, desc = MACRO_TEMAS[tema_id]
        with st.expander(f"{tema_id}. {nome}", expanded=False):
            st.markdown(desc)
    st.markdown("\n")

st.divider()

# -----------------------------------------------------------------------------
# Rodapé com referências
# -----------------------------------------------------------------------------
with st.expander("📄 Referências oficiais", expanded=False):
    st.markdown(
        """
* **Resolução CNE/CES 5/2021** – Conselho Nacional de Educação / MEC.  
* **Parecer CNE/CES 438/2020** – Fundamentação da atualização das DCNs.  
* **Guia de Implementação das DCNs** – Conselho Federal de Administração.  
* PPCs publicados (ex.: IF Goiano – 2022) que já seguem a nova diretriz.

_Este app é informativo e não substitui a leitura integral dos atos normativos._
"""
    )
