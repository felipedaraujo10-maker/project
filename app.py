import re
import unicodedata
import streamlit as st

st.set_page_config(
    page_title="JobMatch AI",
    page_icon="🎯",
    layout="wide",
)

# Competências que o sistema consegue identificar no texto.
SKILLS = {
    "Python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle"],
    "Git": ["git", "github", "gitlab", "bitbucket", "versionamento"],
    "Lógica de Programação": [
        "lógica",
        "logica",
        "algoritmo",
        "algoritmos",
        "estrutura de dados",
        "programação",
        "programacao",
    ],
    "APIs / REST": ["api", "apis", "rest", "restful", "http", "json", "endpoint"],
    "Banco de Dados": [
        "banco de dados",
        "database",
        "db",
        "modelagem de dados",
        "modelagem de banco",
    ],
    "Cloud": ["aws", "azure", "gcp", "cloud", "docker", "devops"],
    "Linux": ["linux", "bash", "shell", "ubuntu", "terminal"],
    "Testes": ["teste", "testes", "pytest", "unittest", "qa", "testes automatizados"],
    "Power BI / Dados": ["power bi", "powerbi", "excel", "dashboard", "bi", "data studio"],
    "Automação": [
        "automação",
        "automacao",
        "script",
        "automação de processos",
        "automacao de processos",
        "rpa",
    ],
    "Indústria 4.0": [
        "indústria 4.0",
        "industria 4.0",
        "iot",
        "manufatura",
        "automação industrial",
        "automacao industrial",
        "plc",
        "clp",
    ],
}

# Quando a vaga informa apenas o cargo, o sistema sugere um conjunto de
# competências normalmente relacionadas ao contexto. Elas ficam marcadas
# como "inferidas" para não parecerem requisitos explicitamente escritos.
ROLE_SKILLS = [
    (
        ["desenvolvedor", "desenvolvedora", "developer", "programador", "programadora", "desenvolvimento de software"],
        ["Python", "Git", "SQL", "APIs / REST", "Lógica de Programação"],
    ),
    (
        ["analista de dados", "analista de dados junior", "analista de dados júnior", "data analyst", "business intelligence", "bi"],
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

QUESTIONS = {
    "Python": "Como você estruturaria uma função Python que recebe uma lista de dados e retorna apenas os itens válidos, tratando erros sem interromper o processamento?",
    "SQL": "Imagine uma tabela de vendas e outra de clientes. Como você faria uma consulta SQL para identificar os 5 clientes com maior valor total comprado?",
    "Git": "Em um projeto com várias pessoas, qual seria seu fluxo de trabalho com Git para desenvolver uma funcionalidade sem impactar a branch principal?",
    "Lógica de Programação": "Como você explicaria a diferença entre uma estrutura de repetição e uma estrutura condicional usando um exemplo prático?",
    "APIs / REST": "O que é uma API REST e como você validaria uma requisição antes de gravar dados em um sistema?",
    "Banco de Dados": "Como você modelaria um banco de dados simples para relacionar candidatos, vagas e candidaturas?",
    "Cloud": "Quais fatores você analisaria antes de escolher entre executar uma aplicação em servidor local ou em uma nuvem como AWS?",
    "Linux": "Quais comandos Linux você usaria para investigar um processo consumindo muita memória em um servidor?",
    "Testes": "Como você criaria um teste automatizado para uma função de cálculo de salário ou validação de cadastro?",
    "Power BI / Dados": "Qual seria sua abordagem para transformar uma planilha de indicadores em um dashboard útil para tomada de decisão?",
    "Automação": "Que tarefa repetitiva de RH ou indústria você automatizaria com Python e como mediria o ganho de produtividade?",
    "Indústria 4.0": "Como sensores e software podem se integrar para detectar uma falha de máquina antes de uma parada de produção?",
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
    """Normaliza espaços, caixa e acentos para facilitar a busca."""
    text = (text or "").lower().strip()
    text = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", text)


def contains_variant(text: str, variant: str) -> bool:
    normalized_text = norm(text)
    normalized_variant = norm(variant)
    # Frases usam busca literal; termos curtos usam limites de palavra.
    if " " in normalized_variant:
        return normalized_variant in normalized_text
    return bool(
        re.search(
            r"(?<![a-z0-9_])" + re.escape(normalized_variant) + r"(?![a-z0-9_])",
            normalized_text,
        )
    )


def extract_skills(text: str):
    found = []
    for skill, variants in SKILLS.items():
        if any(contains_variant(text, variant) for variant in variants):
            found.append(skill)
    return found


def infer_role_skills(text: str):
    inferred = []
    normalized = norm(text)
    for triggers, skills in ROLE_SKILLS:
        if any(norm(trigger) in normalized for trigger in triggers):
            for skill in skills:
                if skill not in inferred:
                    inferred.append(skill)
    return inferred


def unique(items):
    return list(dict.fromkeys(items))


def analyze(resume: str, job: str):
    resume_explicit = extract_skills(resume)
    job_explicit = extract_skills(job)

    # Para vagas vagas demais (ex.: "Desenvolvedor júnior"), inferimos
    # competências prováveis do cargo. Essas sugestões são exibidas separadamente.
    job_inferred = [skill for skill in infer_role_skills(job) if skill not in job_explicit]
    job_skills = unique(job_explicit + job_inferred)

    # No currículo, uma competência só entra como "encontrada" quando há
    # evidência textual. O contexto do cargo é mostrado apenas como sugestão.
    resume_inferred = [skill for skill in infer_role_skills(resume) if skill not in resume_explicit]

    matched = [skill for skill in job_skills if skill in resume_explicit]
    gaps = [skill for skill in job_skills if skill not in resume_explicit]

    score = round((len(matched) / max(len(job_skills), 1)) * 100) if job_skills else 0
    question_skills = unique(gaps + matched)[:3] or ["Lógica de Programação", "Python", "SQL"]

    return (
        resume_explicit,
        resume_inferred,
        job_explicit,
        job_inferred,
        job_skills,
        matched,
        gaps,
        score,
        question_skills,
    )


def feedback(skill: str, answer: str):
    words = len(answer.split())
    if words < 8:
        return 45, "Aprofunde", "Sua resposta está curta. Explique o raciocínio, cite um exemplo e diga como você validaria o resultado."

    answer_norm = norm(answer)
    hits = sum(1 for cue in CUES.get(skill, []) if cue in answer_norm)
    score = min(95, 55 + hits * 8 + min(words, 80) // 10)
    level = "Muito bom" if score >= 82 else "Bom começo" if score >= 68 else "Aprofunde"
    message = "Você trouxe conceitos relevantes. Para ganhar força em uma entrevista, conecte a resposta a uma situação prática e explique suas decisões técnicas."
    if score >= 82:
        message = "Resposta forte: você demonstra domínio dos conceitos e consegue conectar a parte técnica com uma aplicação prática."
    return score, level, message


st.markdown(
    """
    <style>
    .main-title {font-size: 2.7rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: .3rem;}
    .subtitle {color: #667085; font-size: 1.05rem; line-height: 1.55;}
    .metric-box {padding: 1rem 1.1rem; border: 1px solid #e4e7ec; border-radius: 16px; background: #ffffff;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">JobMatch <span style="color:#2457ff">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Diagnóstico de currículo + simulador de entrevista técnica para vagas de TI e Indústria.</div>', unsafe_allow_html=True)
st.caption("Líder do projeto: Felipe Araújo")

col1, col2 = st.columns(2)
with col1:
    resume = st.text_area(
        "01 — Seu currículo",
        height=260,
        placeholder=(
            "Ex.: João Silva\n"
            "Desenvolvedor de Software Júnior\n\n"
            "Habilidades: Python, Git, SQL e APIs REST.\n"
            "Projeto de automação de relatórios com Python..."
        ),
    )
with col2:
    job = st.text_area(
        "02 — Vaga desejada",
        height=260,
        placeholder=(
            "Ex.: Desenvolvedor Python Júnior\n\n"
            "Requisitos: Python, Git, SQL, APIs REST e lógica de programação.\n"
            "Diferencial: Docker..."
        ),
    )

if st.button("Analisar meu perfil →", type="primary", use_container_width=True):
    if not resume.strip() or not job.strip():
        st.error("Preencha o currículo e o anúncio da vaga para executar o diagnóstico.")
    else:
        (
            resume_explicit,
            resume_inferred,
            job_explicit,
            job_inferred,
            job_skills,
            matched,
            gaps,
            score,
            question_skills,
        ) = analyze(resume, job)

        st.session_state.analysis = {
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
        for i in range(3):
            st.session_state.pop(f"answer_{i}", None)
            st.session_state.pop(f"feedback_{i}", None)

if "analysis" in st.session_state:
    data = st.session_state.analysis
    st.divider()
    st.subheader("Diagnóstico do perfil")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Compatibilidade", f"{data['score']}%")
    with m2:
        st.metric("Competências na vaga", len(data["job_skills"]))
    with m3:
        st.metric("Lacunas prioritárias", len(data["gaps"]))

    a, b, c = st.columns(3)
    with a:
        st.markdown("**Competências encontradas**")
        if data["matched"]:
            st.success(" • ".join(data["matched"]))
        else:
            st.info("Nenhuma competência técnica explícita em comum foi identificada.")
        if data["resume_explicit"]:
            st.caption("Detectadas no currículo: " + " • ".join(data["resume_explicit"]))
        else:
            st.warning("Seu currículo não apresenta competências técnicas identificáveis. Adicione uma seção de habilidades, cursos ou projetos.")
        if data["resume_inferred"]:
            st.caption("Contexto do cargo no currículo (não considerado como comprovação): " + " • ".join(data["resume_inferred"]))

    with b:
        st.markdown("**Habilidades citadas na vaga**")
        if data["job_explicit"]:
            st.success(" • ".join(data["job_explicit"]))
        if data["job_inferred"]:
            st.info("Sugeridas pelo cargo: " + " • ".join(data["job_inferred"]))
        if not data["job_explicit"] and not data["job_inferred"]:
            st.warning("Não foi possível detectar habilidades técnicas. Cole os requisitos completos da vaga.")

    with c:
        st.markdown("**Lacunas**")
        if data["gaps"]:
            for gap in data["gaps"]:
                st.warning(f"{gap}: adicione projeto, curso ou evidência prática.")
        else:
            st.success("Nenhuma lacuna crítica identificada.")

    st.divider()
    st.subheader("03 — Entrevista técnica personalizada")
    st.caption("Responda às três perguntas. O feedback abaixo é heurístico e pode depois ser substituído por uma IA generativa.")

    for i, skill in enumerate(data["question_skills"]):
        st.markdown(f"### {i + 1}. Foco: {skill}")
        st.write(QUESTIONS.get(skill, "Explique como você aplicaria essa competência em um projeto real."))
        answer = st.text_area(
            "Sua resposta",
            key=f"answer_{i}",
            height=150,
            placeholder="Digite sua resposta como se estivesse na entrevista...",
        )
        if st.button(f"Receber feedback — pergunta {i + 1}", key=f"feedback_btn_{i}"):
            if not answer.strip():
                st.warning("Digite uma resposta antes de solicitar o feedback.")
            else:
                score_feedback, level, message = feedback(skill, answer)
                st.session_state[f"feedback_{i}"] = (score_feedback, level, message)

        if f"feedback_{i}" in st.session_state:
            score_feedback, level, message = st.session_state[f"feedback_{i}"]
            st.success(f"{score_feedback}/100 — {level}")
            st.write(message)
        st.divider()

st.caption("MVP acadêmico • análise por palavras-chave + inferência de contexto do cargo • feedback heurístico • estrutura pronta para integração com IA generativa")
