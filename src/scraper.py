# scraper.py
import requests
from bs4 import BeautifulSoup
import time
import re
import os
from datetime import datetime, timedelta
from config import DATA_PATHS, DIAS_ACTUALIZACION_CORPUS

#* =====================================================================================
#? SCRAPER INTELIGENTE
#* Se encarga de obtener texto de fuentes online SOLO cuando es necesario.
#* La idea es NO ralentizar el programa ni abusar de peticiones HTTP innecesarias.
#* Solo descarga si:
#*   - No existe el corpus extra (data/hacker_corpus_extra.txt)
#*   - O si el archivo tiene más de 7 días desde su última actualización.
#* =====================================================================================

# =========================================
# ! Configuración de URLs a analizar
# =========================================
URLS = [
    "https://www.elladodelmal.com/",
    "https://www.incibe.es/",
    "https://ciberseguridad.blog/",
    "https://es.wikipedia.org/wiki/Hacker",
]

# ============================
# ! Funciones de limpieza
# ============================
def limpiar_texto(texto):
    """Elimina saltos de línea y espacios innecesarios."""
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# ========================================
# ! Función principal de extracción
# ========================================
def extraer_texto(url):
    """Extrae texto relevante (párrafos, títulos, artículos) desde una URL."""
    print(f"🔍 Extrayendo texto de: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; scraping-educativo/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        textos = []
        for tag in soup.find_all(["p", "h1", "h2", "article"]):
            contenido = tag.get_text(separator=" ", strip=True)
            if len(contenido.split()) > 5:  # evita texto corto o basura
                textos.append(contenido)

        texto_final = limpiar_texto(" ".join(textos))
        return texto_final

    except Exception as e:
        print(f"❌ Error con {url}: {e}")
        return ""

# ========================================
# ! Scraper controlado por fecha
# ========================================
def necesita_actualizar_corpus(path, dias=DIAS_ACTUALIZACION_CORPUS):
    """Devuelve True si el corpus no existe o tiene más de X días."""
    if not os.path.exists(path):
        return True
    fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(path))
    return (datetime.now() - fecha_modificacion) > timedelta(days=dias)

# ========================================
# ! Ejecución condicional
# ========================================
def ejecutar_scraper_si_necesario():
    """Ejecuta el scraper solo si el corpus no existe o está desactualizado."""
    path_extra = DATA_PATHS["extra"]

    if necesita_actualizar_corpus(path_extra):
        print("⚙️  Actualizando corpus adicional (descargando nuevas fuentes)...")
        corpus_total = []

        for url in URLS:
            texto = extraer_texto(url)
            if texto:
                corpus_total.append(texto)
            time.sleep(2)  # espera responsable entre peticiones

        texto_combinado = "\n\n".join(corpus_total)
        with open(path_extra, "w", encoding="utf-8") as f:
            f.write(texto_combinado)
        print("✅ Corpus adicional actualizado y guardado correctamente.")
    else:
        print("⏩ Corpus adicional reciente, no se necesita actualizar.")
