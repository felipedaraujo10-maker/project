import random
import re
import unicodedata
from typing import Dict, List, Tuple

import streamlit as st

st.set_page_config(
    page_title="JobMatch AI — Diagnóstico de Currículo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "# JobMatch AI\nMVP acadêmico liderado por Felipe Araújo."
    },
)

# =========================
# Base de competências
# =========================
SKILLS: Dict[str, List[str]] = {
    "Python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle"],
    "Git": ["git", "github", "gitlab", "bitbucket", "versionamento"],
    "Lógica de Programação": [
        "lógica", "logica", "algoritmo", "algoritmos", "estrutura de dados",
        "programação", "programacao"
    ],
    "APIs / REST": ["api", "apis", "rest", "restful", "http", "json", "endpoint"],
    "Banco de Dados": [
        "banco de dados", "database", "db", "modelagem de dados", "modelagem de banco"
    ],
    "Cloud": ["aws", "azure", "gcp", "cloud", "docker", "devops"],
    "Linux": ["linux", "bash", "shell", "ubuntu", "terminal"],
    "Testes": ["teste", "testes", "pytest", "unittest", "qa", "testes automatizados"],
    "Power BI / Dados": ["power bi", "powerbi", "excel", "dashboard", "bi", "data studio"],
    "Automação": ["automação", "automacao", "script", "rpa", "automação de processos", "automacao de processos"],
    "Indústria 4.0": [
        "indústria 4.0", "industria 4.0", "iot", "manufatura", "automação industrial",
        "automacao industrial", "plc", "clp"
    ],
}

ROLE_SKILLS = [
    (
        ["desenvolvedor", "desenvolvedora", "developer", "programador", "programadora", "desenvolvimento de software"],
        ["Python", "Git", "SQL", "APIs / REST", "Lógica de Programação"],
    ),
    (
        ["analista de dados", "data analyst", "business intelligence", "analista de bi", " bi"],
        ["SQL", "Python", "Power BI / Dados", "Banco de Dados"],
    ),
    (
        ["devops", "engenheiro devops", "engenheira devops", "sre", "infraestrutura"],
        ["Git", "Cloud", "Linux", "Python"],
    ),
    (
        ["suporte de ti", "suporte técnico", "suporte tecnico", "help desk", "service desk", "analista de suporte"],
        ["Linux", "Lógica de Programação", "Banco de Dados"],
    ),
    (
        ["automação industrial", "automacao industrial", "indústria", "industria", "manutenção industrial", "manutencao industrial"],
        ["Automação", "Indústria 4.0", "Python"],
    ),
]

SUPPORTED_ROLES = [
    "Desenvolvedor Python Júnior",
    "Desenvolvedor Web Júnior",
    "Analista de Sistemas Júnior",
    "Analista de Dados Júnior",
    "Analista de BI Júnior",
    "Analista de QA / Testes",
    "Analista de Suporte Técnico",
    "Analista DevOps Júnior",
    "Analista de Automação",
    "Analista de Indústria 4.0",
]

QUESTION_BANK = {
    "Python": [
        "Como você organizaria um código Python para processar dados de uma API com tratamento de erros?",
        "Como você usaria funções e estruturas de dados em Python para resolver um problema real de automação?",
        "Qual a diferença entre lista, tupla e dicionário em Python e quando você escolheria cada uma?",
        "Como você faria uma validação de dados recebidos por uma aplicação Python antes de processá-los?",
        "Como você investigaria um erro em uma aplicação Python que funciona localmente, mas falha em produção?",
    ],
    "SQL": [
        "Imagine uma tabela de vendas e outra de clientes. Como você faria uma consulta SQL para identificar os 5 clientes com maior valor total comprado?",
        "Como você usaria JOIN, GROUP BY e ORDER BY para gerar um relatório de vendas por cliente?",
        "Qual a diferença entre INNER JOIN e LEFT JOIN e em que situação você usaria cada um?",
        "Como você evitaria resultados duplicados ao relacionar duas tabelas em SQL?",
        "Como você otimizaria uma consulta SQL que está demorando muito para retornar os resultados?",
    ],
    "Git": [
        "Em um projeto com várias pessoas, qual seria seu fluxo de trabalho com Git para desenvolver uma funcionalidade sem impactar a branch principal?",
        "Como você resolveria um conflito de merge no Git e garantiria que nenhuma alteração importante fosse perdida?",
        "Qual a diferença entre commit, branch, merge e pull request?",
        "Como você organizaria branches para trabalhar em uma nova funcionalidade e depois entregá-la para revisão?",
        "O que você faria se percebesse que publicou uma credencial por engano em um commit do Git?",
    ],
    "Lógica de Programação": [
        "Como você explicaria a diferença entre uma estrutura de repetição e uma estrutura condicional usando um exemplo prático?",
        "Como você resolveria um problema em que precisa percorrer uma lista e encontrar os valores que atendem a uma condição?",
        "O que é um algoritmo e como você transformaria um problema do cotidiano em passos lógicos para um programa?",
        "Como você escolheria entre usar if/else, for e while para resolver um problema?",
        "Como você verificaria se uma solução lógica está correta antes de implementá-la em código?",
    ],
    "APIs / REST": [
        "O que é uma API REST e como você validaria uma requisição antes de gravar dados em um sistema?",
        "Como você explicaria a diferença entre GET, POST, PUT e DELETE em uma API REST?",
        "O que você faria para tratar autenticação e autorização em uma API?",
        "Como você lidaria com uma API que retorna erro 500 de forma intermitente?",
        "Quais validações você faria ao receber dados de um cliente antes de enviá-los para o banco de dados?",
    ],
    "Banco de Dados": [
        "Como você modelaria um banco de dados simples para relacionar candidatos, vagas e candidaturas?",
        "Qual a diferença entre chave primária e chave estrangeira? Dê um exemplo prático.",
        "Como você evitaria inconsistências ao atualizar dados relacionados em duas tabelas?",
        "Quando faria sentido normalizar uma tabela e quando poderia considerar uma estrutura mais simples?",
        "Como você investigaria um banco de dados que começou a apresentar consultas muito lentas?",
    ],
    "Cloud": [
        "Quais fatores você analisaria antes de escolher entre executar uma aplicação em servidor local ou em uma nuvem como AWS?",
        "O que você avaliaria para decidir entre máquinas virtuais, containers e serviços gerenciados em nuvem?",
        "Como você monitoraria uma aplicação hospedada em nuvem para identificar indisponibilidade ou aumento de custos?",
        "Quais cuidados de segurança você teria ao publicar uma aplicação na nuvem?",
        "Como você explicaria a diferença entre escalar verticalmente e horizontalmente?",
    ],
    "Linux": [
        "Quais comandos Linux você usaria para investigar um processo consumindo muita memória em um servidor?",
        "Como você verificaria espaço em disco, memória e processos ativos em um servidor Linux?",
        "Como você identificaria qual processo está ocupando uma determinada porta?",
        "Como você analisaria logs de uma aplicação rodando em Linux?",
        "Como você usaria permissões e usuários do Linux para proteger arquivos de uma aplicação?",
    ],
    "Testes": [
        "Como você criaria um teste automatizado para uma função de cálculo de salário ou validação de cadastro?",
        "Qual a diferença entre teste unitário e teste de integração?",
        "Como você escolheria casos de teste para uma função que recebe diferentes tipos de entrada?",
        "O que você faria quando um teste funciona na sua máquina, mas falha no ambiente de CI?",
        "Como os testes automatizados ajudam a reduzir regressões em um projeto?",
    ],
    "Power BI / Dados": [
        "Qual seria sua abordagem para transformar uma planilha de indicadores em um dashboard útil para tomada de decisão?",
        "Quais indicadores você escolheria para avaliar o desempenho de uma operação e por quê?",
        "Como você trataria dados duplicados ou incompletos antes de criar um dashboard?",
        "Como você explicaria um indicador complexo para uma pessoa da área de negócio?",
        "Como você garantiria que um dashboard não apenas mostrasse dados, mas ajudasse na tomada de decisão?",
    ],
    "Automação": [
        "Que tarefa repetitiva de RH ou indústria você automatizaria com Python e como mediria o ganho de produtividade?",
        "Como você identificaria uma tarefa candidata à automação dentro de um processo operacional?",
        "Quais cuidados você tomaria ao criar uma automação que manipula dados de clientes ou funcionários?",
        "Como você trataria falhas em uma automação para evitar que um processo inteiro pare?",
        "Como você provaria que uma automação trouxe resultado para a empresa?",
    ],
    "Indústria 4.0": [
        "Como sensores e software podem se integrar para detectar uma falha de máquina antes de uma parada de produção?",
        "Como você usaria dados de sensores para apoiar a manutenção preditiva de uma máquina?",
        "Qual o papel da integração entre sistemas, sensores e análise de dados em uma fábrica inteligente?",
        "Como você avaliaria o impacto de uma solução de Indústria 4.0 antes de colocá-la em produção?",
        "Que riscos técnicos você consideraria ao conectar equipamentos industriais a sistemas digitais?",
    ],
}

CUES = {
    "Python": ["funcao", "tratamento", "erro", "try", "except", "lista", "validacao"],
    "SQL": ["select", "join", "group", "sum", "order", "limit", "having"],
    "Git": ["branch", "commit", "pull", "merge", "rebase", "pull request"],
    "Lógica de Programação": ["condicao", "repeticao", "if", "for", "while", "algoritmo"],
    "APIs / REST": ["endpoint", "http", "json", "status", "validacao", "post", "get"],
    "Banco de Dados": ["tabela", "chave", "relacionamento", "id", "foreign key", "sql"],
    "Cloud": ["custo", "escala", "seguranca", "aws", "monitoramento", "disponibilidade"],
    "Linux": ["top", "ps", "free", "kill", "journalctl", "memoria", "processo"],
    "Testes": ["assert", "pytest", "caso", "entrada", "saida", "teste"],
    "Power BI / Dados": ["indicador", "kpi", "dashboard", "dado", "filtro", "visualizacao"],
    "Automação": ["script", "processo", "tempo", "erro", "ganho", "python"],
    "Indústria 4.0": ["sensor", "iot", "dados", "alerta", "manutencao", "maquina"],
}


def norm(text: str) -> str:
    text = (text or "").lower().strip()
    text = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", text)


def contains_variant(text: str, variant: str) -> bool:
    normalized_text = norm(text)
    normalized_variant = norm(variant)
    if " " in normalized_variant:
        return normalized_variant in normalized_text
    return bool(
        re.search(
            r"(?<![a-z0-9_])" + re.escape(normalized_variant) + r"(?![a-z0-9_])",
            normalized_text,
        )
    )


def unique(items: List[str]) -> List[str]:
    return list(dict.fromkeys(items))


def extract_skills(text: str) -> List[str]:
    found = []
    for skill, variants in SKILLS.items():
        if any(contains_variant(text, variant) for variant in variants):
            found.append(skill)
    return found


def infer_role_skills(text: str) -> List[str]:
    inferred = []
    normalized = norm(text)
    for triggers, skills in ROLE_SKILLS:
        if any(norm(trigger) in normalized for trigger in triggers):
            inferred.extend(skill for skill in skills if skill not in inferred)
    return inferred


def generate_questions(skills: List[str], amount: int = 3) -> List[Tuple[str, str]]:
    available = [skill for skill in unique(skills) if skill in QUESTION_BANK]
    if not available:
        available = ["Lógica de Programação", "Python", "SQL"]

    # Prioriza competências diferentes; depois completa com perguntas variadas.
    chosen_skills = random.sample(available, k=min(amount, len(available)))
    questions = [(skill, random.choice(QUESTION_BANK[skill])) for skill in chosen_skills]

    while len(questions) < amount:
        skill = random.choice(available)
        candidates = [q for q in QUESTION_BANK[skill] if (skill, q) not in questions]
        question = random.choice(candidates or QUESTION_BANK[skill])
        questions.append((skill, question))

    return questions[:amount]


def analyze(resume: str, job: str):
    resume_explicit = extract_skills(resume)
    job_explicit = extract_skills(job)
    job_inferred = [s for s in infer_role_skills(job) if s not in job_explicit]
    resume_inferred = [s for s in infer_role_skills(resume) if s not in resume_explicit]

    job_skills = unique(job_explicit + job_inferred)
    matched = [skill for skill in job_skills if skill in resume_explicit]
    gaps = [skill for skill in job_skills if skill not in resume_explicit]
    score = round((len(matched) / max(len(job_skills), 1)) * 100) if job_skills else 0
    question_skills = unique(gaps + matched)[:3] or ["Lógica de Programação", "Python", "SQL"]

    return {
        "resume_explicit": resume_explicit,
        "resume_inferred": resume_inferred,
        "job_explicit": job_explicit,
        "job_inferred": job_inferred,
        "job_skills": job_skills,
        "matched": matched,
        "gaps": gaps,
        "score": score,
        "question_skills": question_skills,
    }


def feedback(answer: str, skill: str):
    words = len(answer.split())
    if words < 8:
        return 45, "Aprofunde", "Sua resposta está curta. Explique o raciocínio, cite um exemplo e diga como você validaria o resultado."

    answer_norm = norm(answer)
    hits = sum(1 for cue in CUES.get(skill, []) if cue in answer_norm)
    score = min(95, 55 + hits * 7 + min(words, 80) // 10)
    level = "Muito bom" if score >= 82 else "Bom começo" if score >= 68 else "Aprofunde"

    if score >= 82:
        message = "Resposta forte: você demonstra domínio dos conceitos e consegue conectar a parte técnica com uma aplicação prática."
    elif score >= 68:
        message = "Você trouxe conceitos relevantes. Para ganhar força, conecte a resposta a uma situação prática e explique suas decisões técnicas."
    else:
        message = "A resposta mostra uma direção, mas ainda pode ganhar profundidade. Defina os conceitos, descreva os passos e inclua um exemplo."

    return score, level, message


def inject_css(dark_mode: bool = False):
    st.markdown(
        """
        <style>
        :root {
            --jm-primary: #2457ff;
            --jm-primary-2: #6b7cff;
            --jm-ink: #101828;
            --jm-muted: #667085;
            --jm-line: #e4e7ec;
            --jm-soft: #f6f8fc;
            --jm-white: #ffffff;
            --jm-success: #157347;
            --jm-success-bg: #e9f8f0;
            --jm-warning: #a15c00;
            --jm-warning-bg: #fff5e8;
            --jm-danger: #b42318;
            --jm-danger-bg: #fff0ef;
            --jm-shadow: 0 18px 45px rgba(16, 24, 40, 0.08);
            --jm-radius: 20px;
        }

        .stApp {
            background: linear-gradient(180deg, #f7f9fc 0%, #eef3fb 100%);
        }
        [data-testid="stHeader"] { background: rgba(247,249,252,0.82); }
        [data-testid="stToolbar"] { right: 1rem; }
        .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1240px; }

        .jm-topbar {
            display:flex; justify-content:space-between; align-items:center;
            padding: 12px 0 18px; border-bottom:1px solid rgba(228,231,236,.85);
            margin-bottom: 26px;
        }
        .jm-brand { font-size: 1.1rem; font-weight: 800; letter-spacing:-.03em; color:var(--jm-ink); }
        .jm-brand span { color:var(--jm-primary); }
        .jm-badge {
            padding:7px 11px; border:1px solid #dbe2f0; border-radius:999px;
            color:#48536a; background:rgba(255,255,255,.82); font-size:.76rem; font-weight:700;
        }

        .jm-hero {
            background: linear-gradient(135deg, #0f1b38 0%, #172b5d 45%, #2457ff 100%);
            border-radius: 28px; padding: 34px 36px; color:white; box-shadow: 0 24px 55px rgba(23,43,93,.18);
            position:relative; overflow:hidden; margin-bottom:24px;
        }
        .jm-hero:after { content:""; position:absolute; width:340px; height:340px; border-radius:50%; border:1px solid rgba(255,255,255,.12); right:-120px; top:-150px; }
        .jm-eyebrow { font-size:.74rem; letter-spacing:.14em; text-transform:uppercase; font-weight:800; color:#b7c9ff; }
        .jm-title { font-size:2.65rem; line-height:1.03; font-weight:850; letter-spacing:-.045em; margin:.55rem 0 .7rem; max-width:760px; }
        .jm-subtitle { max-width:790px; color:#d7e0f8; line-height:1.6; margin-bottom:0; }
        .jm-hero-meta { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; }
        .jm-hero-pill { border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.08); border-radius:999px; padding:8px 11px; font-size:.75rem; color:#e7edff; }

        .jm-section-title { font-size:1.05rem; font-weight:800; color:var(--jm-ink); margin: 28px 0 8px; }
        .jm-section-copy { color:var(--jm-muted); font-size:.86rem; margin-bottom:14px; }
        .jm-role-wrap { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:8px; }
        .jm-role { border:1px solid #dfe4ed; background:white; color:#344054; border-radius:999px; padding:8px 11px; font-size:.75rem; font-weight:700; box-shadow:0 3px 12px rgba(16,24,40,.04); }

        .jm-card-title { font-size:1rem; font-weight:800; color:var(--jm-ink); margin-bottom:2px; }
        .jm-card-copy { color:var(--jm-muted); font-size:.78rem; line-height:1.5; margin-bottom:12px; }
        .jm-number { display:inline-flex; width:27px; height:27px; border-radius:9px; align-items:center; justify-content:center; background:#edf2ff; color:var(--jm-primary); font-size:.72rem; font-weight:900; margin-right:7px; }
        div[data-testid="stVerticalBlockBorderWrapper"] { border-radius:var(--jm-radius); border-color:var(--jm-line); box-shadow:var(--jm-shadow); background:rgba(255,255,255,.94); }
        .stTextArea textarea { border-radius:14px !important; background:#fbfcfe !important; border-color:#dfe4ed !important; }
        .stTextArea textarea:focus { border-color:#9db2ff !important; box-shadow:0 0 0 4px #edf1ff !important; }
        .stButton > button { border-radius:13px; font-weight:800; min-height:44px; }
        div.stButton > button[kind="primary"] { background:var(--jm-primary); border-color:var(--jm-primary); }
        div.stButton > button[kind="secondary"] { background:#f4f6fa; border-color:#e1e6ef; color:#344054; }

        [data-testid="stMetric"] { background:#fff; border:1px solid var(--jm-line); padding:16px; border-radius:16px; box-shadow:0 10px 28px rgba(16,24,40,.05); }
        [data-testid="stMetricLabel"] p { color:var(--jm-muted) !important; font-weight:700; }
        [data-testid="stMetricValue"] { color:var(--jm-ink); }

        .jm-status { padding:13px 14px; border-radius:14px; margin-top:8px; font-size:.82rem; line-height:1.55; }
        .jm-status.ok { background:var(--jm-success-bg); color:var(--jm-success); border:1px solid #cceedd; }
        .jm-status.warn { background:var(--jm-warning-bg); color:var(--jm-warning); border:1px solid #f6dfb8; }
        .jm-status.danger { background:var(--jm-danger-bg); color:var(--jm-danger); border:1px solid #f4c7c3; }
        .jm-chip-row { display:flex; flex-wrap:wrap; gap:7px; margin-top:8px; }
        .jm-chip { padding:6px 9px; border-radius:999px; background:#f2f4f7; color:#344054; font-size:.72rem; font-weight:750; }
        .jm-chip.ok { background:#eaf8f1; color:#157347; }
        .jm-chip.miss { background:#fff2ef; color:#b42318; }

        .jm-question {
            border:1px solid var(--jm-line); background:#fbfcff; padding:16px; border-radius:16px; margin-top:12px;
        }
        .jm-question-head { display:flex; gap:10px; align-items:flex-start; }
        .jm-qnum { width:30px; height:30px; border-radius:10px; background:#edf2ff; color:var(--jm-primary); display:flex; align-items:center; justify-content:center; font-weight:900; flex:0 0 auto; }
        .jm-focus { color:var(--jm-primary); font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
        .jm-qtext { color:var(--jm-ink); font-size:.96rem; line-height:1.5; font-weight:750; margin-top:2px; }
        .jm-feedback { padding:12px 14px; border-radius:14px; background:#f4f7fb; border:1px solid #e4e8f0; margin-top:10px; font-size:.82rem; line-height:1.55; }
        .jm-footer { color:#98a2b3; text-align:center; font-size:.72rem; margin-top:30px; }
        @media (max-width: 900px) {
            .jm-title { font-size:2rem; }
            .jm-hero { padding:26px 22px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    if dark_mode:
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(180deg, #0a0f1b 0%, #11182a 100%) !important;
            }
            [data-testid="stHeader"] {
                background: rgba(10, 15, 27, 0.9) !important;
            }
            .jm-topbar {
                border-bottom-color: #253047 !important;
            }
            .jm-brand, .jm-section-title, .jm-card-title, .jm-qtext {
                color: #f3f6ff !important;
            }
            .jm-section-copy, .jm-card-copy, .jm-subtitle, .jm-footer {
                color: #a8b2c7 !important;
            }
            .jm-badge {
                background: #141d30 !important;
                border-color: #2a3853 !important;
                color: #dce4f5 !important;
            }
            .jm-role {
                background: #171f31 !important;
                border-color: #2a3853 !important;
                color: #e1e8f5 !important;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: #121827 !important;
                border-color: #253047 !important;
                box-shadow: 0 18px 45px rgba(0, 0, 0, 0.28) !important;
            }
            [data-testid="stMetric"] {
                background: #121827 !important;
                border-color: #253047 !important;
            }
            [data-testid="stMetricLabel"] p, [data-testid="stMetricValue"] {
                color: #f3f6ff !important;
            }
            .stTextArea textarea {
                background: #0e1626 !important;
                color: #eef3ff !important;
                border-color: #2a3853 !important;
            }
            .stTextArea textarea::placeholder {
                color: #76839b !important;
            }
            .jm-question {
                background: #0f1727 !important;
                border-color: #29364d !important;
            }
            .jm-feedback {
                background: #161f31 !important;
                border-color: #29364d !important;
                color: #c7d0e1 !important;
            }
            .jm-chip {
                background: #1c2639 !important;
                color: #d8e0ef !important;
            }
            .jm-chip.ok {
                background: #103526 !important;
                color: #75ddb0 !important;
            }
            .jm-chip.miss {
                background: #351b20 !important;
                color: #ff9b9f !important;
            }
            .jm-status.ok {
                background: #103526 !important;
                border-color: #19583f !important;
                color: #75ddb0 !important;
            }
            .jm-status.warn {
                background: #352719 !important;
                border-color: #69471f !important;
                color: #ffbf75 !important;
            }
            .jm-status.danger {
                background: #351b20 !important;
                border-color: #6b2829 !important;
                color: #ff9b9f !important;
            }
            div.stButton > button[kind="secondary"] {
                background: #1b2437 !important;
                color: #e4eaf7 !important;
                border-color: #2a3853 !important;
            }
            [data-testid="stCaption"] {
                color: #a8b2c7 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

def badge(text: str, cls: str = "") -> str:
    return f'<span class="jm-chip {cls}">{text}</span>'


def render_role_section():
    roles_html = "".join(f'<span class="jm-role">{role}</span>' for role in SUPPORTED_ROLES)
    st.markdown('<div class="jm-section-title">🎯 Cargos que o JobMatch atende</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="jm-section-copy">Cole qualquer anúncio de TI, Dados ou Indústria. Estes são os principais perfis que o diagnóstico consegue contextualizar.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="jm-role-wrap">{roles_html}</div>', unsafe_allow_html=True)


def render_analysis(data: dict):
    st.markdown('<div class="jm-section-title">Seu diagnóstico</div>', unsafe_allow_html=True)
    st.markdown('<div class="jm-section-copy">Veja rapidamente o alinhamento técnico, o que já aparece no currículo e onde estão as lacunas.</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="medium")
    m1.metric("Compatibilidade", f"{data['score']}%")
    m2.metric("Competências na vaga", len(data["job_skills"]))
    m3.metric("Lacunas prioritárias", len(data["gaps"]))
    st.progress(data["score"] / 100, text=f"Aderência técnica: {data['score']}%")

    a, b, c = st.columns(3, gap="medium")
    with a:
        with st.container(border=True):
            st.markdown('<div class="jm-card-title">Competências encontradas</div>', unsafe_allow_html=True)
            st.markdown('<div class="jm-card-copy">Competências identificadas explicitamente no currículo.</div>', unsafe_allow_html=True)
            if data["matched"]:
                st.markdown('<div class="jm-chip-row">' + ''.join(badge(x, "ok") for x in data["matched"]) + '</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="jm-status danger">Nenhuma competência técnica explícita em comum foi identificada.</div>', unsafe_allow_html=True)
            if data["resume_explicit"]:
                st.caption("Também detectadas no currículo: " + " • ".join(data["resume_explicit"]))
            else:
                st.warning("Adicione uma seção de habilidades, cursos ou projetos técnicos no currículo.")

    with b:
        with st.container(border=True):
            st.markdown('<div class="jm-card-title">Habilidades da vaga</div>', unsafe_allow_html=True)
            st.markdown('<div class="jm-card-copy">O sistema separa o que foi escrito na vaga do que foi inferido pelo cargo.</div>', unsafe_allow_html=True)
            if data["job_explicit"]:
                st.markdown('<div class="jm-chip-row">' + ''.join(badge(x) for x in data["job_explicit"]) + '</div>', unsafe_allow_html=True)
            else:
                st.info("Nenhum requisito técnico explícito detectado.")
            if data["job_inferred"]:
                st.caption("Sugestões pelo contexto do cargo: " + " • ".join(data["job_inferred"]))

    with c:
        with st.container(border=True):
            st.markdown('<div class="jm-card-title">Lacunas prioritárias</div>', unsafe_allow_html=True)
            st.markdown('<div class="jm-card-copy">Competências da vaga que ainda não têm evidência textual no currículo.</div>', unsafe_allow_html=True)
            if data["gaps"]:
                for gap in data["gaps"]:
                    st.markdown(f'<div class="jm-status warn"><strong>{gap}</strong><br>Inclua projeto, curso ou evidência prática dessa competência.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="jm-status ok">Nenhuma lacuna crítica identificada. Seu currículo está alinhado às competências analisadas.</div>', unsafe_allow_html=True)


def render_interview(data: dict):
    st.markdown('<div class="jm-section-title">03 — Entrevista técnica personalizada</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="jm-section-copy">As perguntas são sorteadas aleatoriamente, mas sempre fundamentadas nas competências identificadas na vaga. Você pode gerar outra rodada sem refazer o diagnóstico.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1], gap="medium")
    with left:
        st.markdown("**Como funciona**")
        st.caption("1. O sistema seleciona até 3 competências.  2. Sorteia perguntas do banco técnico.  3. Você responde.  4. O JobMatch atribui um feedback heurístico.")
    with right:
        if st.button("↻ Sortear novas perguntas", key="shuffle_questions", use_container_width=True):
            st.session_state.interview_questions = generate_questions(data["question_skills"], 3)
            for i in range(3):
                st.session_state.pop(f"feedback_{i}", None)
                st.session_state.pop(f"answer_{i}", None)
            st.rerun()

    for i, (skill, question) in enumerate(st.session_state.interview_questions):
        with st.container(border=True):
            st.markdown(
                f'<div class="jm-question"><div class="jm-question-head"><div class="jm-qnum">{i + 1}</div><div><div class="jm-focus">Foco: {skill}</div><div class="jm-qtext">{question}</div></div></div></div>',
                unsafe_allow_html=True,
            )
            answer = st.text_area(
                "Sua resposta",
                key=f"answer_{i}",
                height=140,
                placeholder="Responda como se estivesse diante do recrutador. Explique o raciocínio e, quando possível, use um exemplo prático.",
            )
            if st.button(f"Receber feedback — pergunta {i + 1}", key=f"feedback_btn_{i}", use_container_width=True):
                if not answer.strip():
                    st.warning("Digite uma resposta antes de solicitar o feedback.")
                else:
                    st.session_state[f"feedback_{i}"] = feedback(answer, skill)
            if f"feedback_{i}" in st.session_state:
                score_feedback, level, message = st.session_state[f"feedback_{i}"]
                st.markdown(
                    f'<div class="jm-feedback"><strong>{score_feedback}/100 — {level}</strong><br>{message}</div>',
                    unsafe_allow_html=True,
                )


def main():
    dark_mode = st.session_state.get("dark_mode", False)
    inject_css(dark_mode)

    brand_col, badge_col, theme_col = st.columns([5.2, 2.6, 2.2], vertical_alignment="center")
    with brand_col:
        st.markdown(
            '<div class="jm-topbar" style="justify-content:flex-start;"><div class="jm-brand">JobMatch <span>AI</span></div></div>',
            unsafe_allow_html=True,
 
    with theme_col:
        st.markdown('<div style="font-size:.7rem;color:#667085;font-weight:800;margin:2px 0 -8px;">Tema</div>', unsafe_allow_html=True)
        st.toggle("🌙 Modo escuro", key="dark_mode", help="Alterne entre os modos claro e escuro."))

    st.markdown(
        '<div class="jm-hero"><div class="jm-eyebrow">Diagnóstico de currículo + simulador de entrevista</div><div class="jm-title">Descubra o que falta para seu perfil chegar mais perto da vaga.</div><div class="jm-subtitle">Compare seu currículo com a descrição de uma vaga, identifique competências e treine para perguntas técnicas com base no que o mercado está pedindo.</div><div class="jm-hero-meta"><span class="jm-hero-pill">✓ Comparação de habilidades</span><span class="jm-hero-pill">✓ Lacunas prioritárias</span><span class="jm-hero-pill">✓ 3 perguntas aleatórias</span><span class="jm-hero-pill">✓ Feedback imediato</span></div></div>',
        unsafe_allow_html=True,
    )

    render_role_section()

    st.markdown('<div class="jm-section-title">Comece seu diagnóstico</div>', unsafe_allow_html=True)
    st.markdown('<div class="jm-section-copy">Preencha os dois campos abaixo. Quanto mais completa a descrição, mais útil será o diagnóstico.</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="jm-card-title"><span class="jm-number">01</span>Seu currículo</div>', unsafe_allow_html=True)
            st.markdown('<div class="jm-card-copy">Inclua experiências, projetos, cursos e habilidades.</div>', unsafe_allow_html=True)
            resume = st.text_area(
                "Currículo",
                height=270,
                label_visibility="collapsed",
                placeholder="Ex.: João Silva\nDesenvolvedor de Software Júnior\n\nHabilidades: Python, Git, SQL e APIs REST.\nProjeto de automação de relatórios com Python...",
            )

    with right:
        with st.container(border=True):
            st.markdown('<div class="jm-card-title"><span class="jm-number">02</span>Vaga desejada</div>', unsafe_allow_html=True)
            st.markdown('<div class="jm-card-copy">Cole o anúncio ou apenas os requisitos principais da vaga.</div>', unsafe_allow_html=True)
            job = st.text_area(
                "Descrição da vaga",
                height=270,
                label_visibility="collapsed",
                placeholder="Ex.: Desenvolvedor Python Júnior\n\nRequisitos: Python, Git, SQL, APIs REST e lógica de programação.\nDiferencial: Docker...",
            )

    st.write("")
    if st.button("Analisar meu perfil →", type="primary", use_container_width=True):
        if not resume.strip() or not job.strip():
            st.error("Preencha o currículo e o anúncio da vaga para executar o diagnóstico.")
        else:
            st.session_state.analysis = analyze(resume, job)
            st.session_state.interview_questions = generate_questions(st.session_state.analysis["question_skills"], 3)
            for i in range(3):
                st.session_state.pop(f"answer_{i}", None)
                st.session_state.pop(f"feedback_{i}", None)

    if "analysis" in st.session_state:
        data = st.session_state.analysis
        st.divider()
        render_analysis(data)
        st.divider()
        render_interview(data)

    st.markdown(
        '<div class="jm-footer">MVP acadêmico • análise por palavras-chave + inferência de contexto do cargo • perguntas técnicas aleatórias por competência • feedback heurístico • pronto para futura integração com IA generativa</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
