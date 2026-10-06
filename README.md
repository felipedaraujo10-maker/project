# JobMatch AI — Python + Streamlit

MVP acadêmico do **JobMatch AI**, liderado por **Felipe Araújo**.

O projeto não utiliza Flask. A interface e a lógica ficam em um único aplicativo Python com Streamlit.

## Funcionalidades

- Comparação de competências técnicas entre currículo e vaga.
- Score de compatibilidade.
- Identificação de lacunas de competências.
- Geração de 3 perguntas técnicas com base no perfil.
- Campo de resposta para cada pergunta.
- Feedback imediato por heurísticas de conteúdo e profundidade.

## Como executar

### Windows

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abrirá o aplicativo no navegador.

## Evolução para IA generativa

A função `feedback()` pode ser substituída por uma chamada a um provedor de LLM para avaliar respostas de maneira contextual. A função `analyze()` também pode evoluir para uma análise semântica mais robusta.
