import re
import streamlit as st

st.set_page_config(
    page_title="JobMatch AI",
    page_icon="🎯",
    layout="wide",
)

SKILLS = {
    "Python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "Lógica de Programação": ["lógica", "logica", "algoritmo", "algoritmos", "estrutura de dados"],
    "APIs / REST": ["api", "apis", "rest", "restful", "http", "json"],
    "Banco de Dados": ["banco de dados", "database", "db", "modelagem de dados"],
    "Cloud": ["aws", "azure", "gcp", "cloud", "docker"],
    "Linux": ["linux", "bash", "shell"],
    "Testes": ["teste", "testes", "pytest", "unittest", "qa"],
    "Power BI / Dados": ["power bi", "powerbi", "excel", "dashboard", "bi"],
    "Automação": ["automação", "automacao", "script", "automação de processos", "rpa"],
    "Indústria 4.0": ["indústria 4.0", "industria 4.0", "iot", "manufatura", "automação industrial", "plc", "clp"],
}

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
    "Python": ["função", "tratamento", "erro", "try", "except", "lista", "validação"],
    "SQL": ["select", "join", "group", "sum", "order", "limit", "having"],
    "Git": ["branch", "commit", "pull", "merge", "rebase", "pull request"],
    "Lógica de Programação": ["condição", "repetição", "if", "for", "while", "algoritmo"],
    "APIs / REST": ["endpoint", "http", "json", "status", "validação", "post", "get"],
    "Banco de Dados": ["tabela", "chave", "relacionamento", "id", "foreign key", "sql"],
    "Cloud": ["custo", "escala", "segurança", "aws", "monitoramento", "disponibilidade"],
    "Linux": ["top", "ps", "free", "kill", "journalctl", "memória", "processo"],
    "Testes": ["assert", "pytest", "caso", "entrada", "saída", "teste"],
    "Power BI / Dados": ["indicador", "kpi", "dashboard", "dado", "filtro", "visualização"],
    "Automação": ["script", "processo", "tempo", "erro", "ganho", "python"],
    "Indústria 4.0": ["sensor", "iot", "dados", "alerta", "manutenção", "máquina"],
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def extract_skills(text: str):
    normalized = norm(text)
    found = []
    for skill, variants in SKILLS.items():
        if any(
            re.search(r"(?<![a-z0-9])" + re.escape(variant) + r"(?![a-z0-9])", normalized)
            for variant in variants
        ):
            found.append(skill)
    return found


def analyze(resume: str, job: str):
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job)
    matched = [skill for skill in job_skills if skill in resume_skills]
    gaps = [skill for skill in job_skills if skill not in resume_skills]
    score = round((len(matched) / max(len(job_skills), 1)) * 100)
    question_skills = (gaps + matched)[:3] or ["Lógica de Programação", "Python", "SQL"]
    return resume_skills, job_skills, matched, gaps, score, question_skills


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
        placeholder="Ex.: Estudante de Sistemas de Informação...\nPython, Git, SQL...\nProjeto de automação de relatórios...",
    )
with col2:
    job = st.text_area(
        "02 — Vaga desejada",
        height=260,
        placeholder="Ex.: Procuramos pessoa desenvolvedora júnior...\nRequisitos: Python, Git, SQL, APIs REST...",
    )

if st.button("Analisar meu perfil →", type="primary", use_container_width=True):
    if not resume.strip() or not job.strip():
        st.error("Preencha o currículo e o anúncio da vaga para executar o diagnóstico.")
    else:
        resume_skills, job_skills, matched, gaps, score, question_skills = analyze(resume, job)
        st.session_state.analysis = {
            "resume_skills": resume_skills,
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
            st.write(" • ".join(data["matched"]))
        else:
            st.info("Nenhuma competência em comum identificada.")
    with b:
        st.markdown("**Habilidades citadas na vaga**")
        if data["job_skills"]:
            st.write(" • ".join(data["job_skills"]))
        else:
            st.info("Não foi possível detectar habilidades conhecidas na vaga.")
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
                score, level, message = feedback(skill, answer)
                st.session_state[f"feedback_{i}"] = (score, level, message)

        if f"feedback_{i}" in st.session_state:
            score, level, message = st.session_state[f"feedback_{i}"]
            st.success(f"{score}/100 — {level}")
            st.write(message)
        st.divider()

st.caption("MVP acadêmico • análise por palavras-chave • feedback heurístico • estrutura pronta para integração com IA generativa")
