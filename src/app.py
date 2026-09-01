# src/app.py
import streamlit as st
from collections import Counter
from config import STOPWORDS
from corpus import cargar_corpus, preprocesar_texto, tokenizar, construir_diccionario

# ============================
# Inicialización del modelo
# ============================
@st.cache_resource
def inicializar_modelo():
    """Carga y prepara diccionarios de bigramas y trigramas."""
    texto = cargar_corpus()
    texto = preprocesar_texto(texto)
    tokens = tokenizar(texto)
    dic2 = construir_diccionario(tokens, n=2)
    dic3 = construir_diccionario(tokens, n=3)
    return dic2, dic3

dic2, dic3 = inicializar_modelo()

# ============================
# Inicialización de session state
# ============================
if "secuencia" not in st.session_state:
    st.session_state["secuencia"] = []
if "ultima_sugerencia" not in st.session_state:
    st.session_state["ultima_sugerencia"] = []
if "entrada_usuario" not in st.session_state:
    st.session_state["entrada_usuario"] = ""

# ============================
# Configuración de página
# ============================
st.set_page_config(page_title="Asistente de Escritura", page_icon="🧠", layout="centered")

# ============================
# Estilos personalizados
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #14161B;
    --panel: #1B1E26;
    --border: #2A2E38;
    --text: #ECEAE4;
    --muted: #8B90A0;
    --accent: #E8A54B;
    --accent-soft: rgba(232, 165, 75, 0.14);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

[data-testid="stSidebar"] {
    background-color: var(--panel);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] h3 { color: var(--accent) !important; }

.app-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: -0.02em;
    margin-bottom: 0.1rem;
    color: var(--text);
}
.app-subtitle {
    color: var(--muted);
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
}

.section-label {
    font-size: 0.78rem;
    color: var(--muted);
    margin: 1.4rem 0 0.5rem 2px;
    text-transform: none;
}

/* Tarjeta con la frase en construcción, estilo editor */
.editor-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.6rem 1.4rem;
    min-height: 30px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text);
    word-wrap: break-word;
}
.editor-card .placeholder { color: var(--muted); }

.cursor {
    display: inline-block;
    width: 2px;
    height: 1.05em;
    background: var(--accent);
    margin-left: 3px;
    vertical-align: text-bottom;
    animation: blink 1s steps(1) infinite;
}
@keyframes blink { 50% { opacity: 0; } }

/* Input de texto */
[data-testid="stTextInput"] input {
    background-color: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.7rem 0.9rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
[data-testid="stTextInput"] label { color: var(--muted) !important; font-size: 0.85rem !important; }

/* Chips de sugerencias */
.st-key-chip_row .stButton>button {
    background-color: var(--accent-soft);
    border: 1px solid var(--accent);
    color: var(--accent);
    border-radius: 999px;
    padding: 0.45rem 0.3rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.92rem;
    width: 100%;
    transition: background-color 0.15s ease, transform 0.1s ease;
}
.st-key-chip_row .stButton>button:hover {
    background-color: var(--accent);
    color: var(--bg);
    transform: translateY(-1px);
}

.empty-suggestions {
    color: var(--muted);
    font-size: 0.9rem;
    padding: 0.3rem 0 0.2rem 2px;
}

/* Controles secundarios (deshacer / nueva frase / terminar) */
.st-key-control_row .stButton>button {
    background-color: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 8px;
    font-size: 0.85rem;
    padding: 0.5rem 0.8rem;
    width: 100%;
}
.st-key-control_row .stButton>button:hover {
    border-color: var(--text);
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)

# ============================
# Cabecera
# ============================
st.markdown('<div class="app-title"> Asistente de Escritura</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Escribe una o dos palabras y deja que el corpus te sugiera cómo continuar.</div>',
    unsafe_allow_html=True,
)

# ============================
# Barra lateral
# ============================
with st.sidebar:
    st.markdown("### Cómo funciona")
    st.markdown(
        "- Escribe **1 palabra** y pulsa **Enter** para empezar.\n"
        "- Con **2 o más palabras**, las sugerencias son más precisas.\n"
        "- Haz clic en una sugerencia para añadirla a la frase.\n"
        "- Usa **Deshacer** si te equivocas de palabra."
    )
    st.markdown("---")
    st.markdown("### Estado")
    st.metric("Palabras en la frase", len(st.session_state["secuencia"]))

# ============================
# Lógica de sugerencias (sin cambios respecto al modelo)
# ============================
def calcular_sugerencias(secuencia, dic2, dic3, top_n=5):
    """Calcula hasta top_n sugerencias siguiendo la lógica trigram->bigram (backoff)."""
    if not secuencia:
        return []

    siguientes = []
    if len(secuencia) >= 2:
        clave3 = tuple(secuencia[-2:])
        siguientes = dic3.get(clave3, [])
    if not siguientes:
        clave2 = (secuencia[-1],)
        siguientes = dic2.get(clave2, [])

    if not siguientes:
        return []

    contador = Counter(siguientes)
    filtradas = [w for w, _ in contador.most_common(15) if w not in STOPWORDS]

    sugerencias = []
    for w in filtradas:
        if w != secuencia[-1]:
            sugerencias.append(w)
        if len(sugerencias) >= top_n:
            break

    if not sugerencias:
        sugerencias = [w for w, _ in contador.most_common(top_n)]

    return sugerencias


# =================
# Entrada de texto
# =================
def procesar_entrada():
    """Procesa la entrada actual cuando el usuario presiona Enter."""
    entrada = st.session_state.entrada_usuario.strip().lower()
    if not entrada:
        return

    if entrada == "salir":
        st.session_state["secuencia"].clear()
        st.session_state["entrada_usuario"] = ""
        st.stop()

    # Se añaden todas las palabras escritas, no solo las dos primeras
    palabras = entrada.split()
    st.session_state["secuencia"].extend(palabras)
    st.session_state["entrada_usuario"] = ""  # limpiar campo antes del rerun


# ============================
# Frase en construcción (estilo editor)
# ============================
st.markdown('<div class="section-label">Tu frase</div>', unsafe_allow_html=True)
if st.session_state["secuencia"]:
    texto_frase = " ".join(st.session_state["secuencia"])
    st.markdown(
        f'<div class="editor-card">{texto_frase}<span class="cursor"></span></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="editor-card"><span class="placeholder">Escribe la primera palabra para empezar…</span>'
        '<span class="cursor"></span></div>',
        unsafe_allow_html=True,
    )

# Campo de texto con callback limpio
st.text_input(
    "Añadir palabra(s)",
    key="entrada_usuario",
    on_change=procesar_entrada,
    placeholder="una o dos palabras…",
)

# ============================
# Sugerencias (chips clicables)
# ============================
st.markdown('<div class="section-label">Sugerencias</div>', unsafe_allow_html=True)

if st.session_state["secuencia"]:
    sugerencias = calcular_sugerencias(st.session_state["secuencia"], dic2, dic3, top_n=5)
    st.session_state["ultima_sugerencia"] = sugerencias

    if sugerencias:
        with st.container(key="chip_row"):
            cols = st.columns(len(sugerencias))
            for i, s in enumerate(sugerencias):
                with cols[i]:
                    if st.button(s, key=f"sugg_{i}_{len(st.session_state['secuencia'])}"):
                        st.session_state["secuencia"].append(s)
                        st.rerun()
    else:
        st.markdown(
            '<div class="empty-suggestions">Sin sugerencias para esta combinación — prueba con otra palabra.</div>',
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        '<div class="empty-suggestions">Las sugerencias aparecerán aquí en cuanto empieces a escribir.</div>',
        unsafe_allow_html=True,
    )

# ============================
# Controles secundarios
# ============================
with st.container(key="control_row"):
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Deshacer", disabled=not st.session_state["secuencia"]):
            if st.session_state["secuencia"]:
                st.session_state["secuencia"].pop()
            st.rerun()
    with c2:
        if st.button("Nueva frase", disabled=not st.session_state["secuencia"]):
            st.session_state["secuencia"].clear()
            st.session_state["ultima_sugerencia"].clear()
            st.rerun()
    with c3:
        if st.button("Terminar"):
            st.session_state["secuencia"].clear()
            st.session_state["ultima_sugerencia"].clear()
            st.success("Sesión terminada. Recarga la página para empezar de nuevo.")
            st.stop()