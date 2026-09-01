# src/corpus.py
import os
import re
from collections import defaultdict, Counter
from config import DATA_PATHS
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

#* ========================================================
#? CORPUS
#* Se encarga de leer, limpiar, tokenizar y analizar el corpus.
#* Ahora puede cargar desde Azure Blob Storage si hay conexión.
#* ========================================================


# ============================================================== 
# !1️⃣ Preprocesamiento del texto
# Limpia el texto eliminando símbolos, HTML o ruido.
# ============================================================== 
def preprocesar_texto(texto):
    """Limpia texto eliminando caracteres no deseados y espacios extra."""
    texto = texto.lower()
    texto = re.sub(r'<[^>]+>', ' ', texto)   # elimina etiquetas HTML
    texto = re.sub(r'[^a-záéíóúüñ\s]', ' ', texto)  # deja solo letras y espacios
    texto = re.sub(r'\s+', ' ', texto)  # reduce espacios
    return texto.strip()


# ============================
# !2️⃣ Cargar y combinar corpus (con soporte para Azure)
# ============================
def cargar_corpus():
    """
    Carga el corpus desde Azure Blob Storage si hay conexión configurada,
    de lo contrario, usa el corpus local en data/.
    """
    load_dotenv()  # Cargar variables desde .env
    conn_str = os.getenv("AZURE_CONN_STR")
    container_name = os.getenv("AZURE_CONTAINER")
    blob_name = os.getenv("AZURE_BLOB_NAME")

    if conn_str and container_name and blob_name:
        try:
            print("☁️ Conectando a Azure Blob Storage...")
            blob_service = BlobServiceClient.from_connection_string(conn_str)
            container = blob_service.get_container_client(container_name)
            blob_client = container.get_blob_client(blob_name)

            texto = blob_client.download_blob().readall().decode("utf-8")
            print(f"✅ Corpus cargado correctamente desde Azure ({blob_name})")
            return texto.lower()
        except Exception as e:
            print(f"⚠️ No se pudo conectar a Azure ({e}), usando corpus local...")

    # Si falla Azure, continuar con la lógica local
    if not os.path.exists(DATA_PATHS["combined"]):
        try:
            # Combinar corpus original y extra si no existe el combinado
            with open(DATA_PATHS["original"], "r", encoding="utf-8") as f1, \
                 open(DATA_PATHS["extra"], "r", encoding="utf-8") as f2, \
                 open(DATA_PATHS["combined"], "w", encoding="utf-8") as out:
                out.write(f1.read())
                out.write("\n\n")
                out.write(f2.read())
            print("✅ Creado data/hacker_total.txt automáticamente.")
        except FileNotFoundError:
            print("ℹ️ No se pudo crear hacker_total.txt, continúa con hacker.txt original.")

    # Cargar el texto final
    with open(DATA_PATHS["combined"], "r", encoding="utf-8") as f:
        texto = f.read().lower()
    print("📘 Corpus cargado localmente.")
    return texto


# ==============
# !3️⃣ Tokenización
# ==============
def tokenizar(texto):
    """Tokeniza el texto respetando tildes y letras españolas."""
    return re.findall(r'\b[a-záéíóúüñ]{2,}\b', texto)


# =========================
# !4️⃣ Construcción de n-gramas
# =========================
def construir_diccionario(tokens, n=2):
    """Construye diccionario de n-gramas (bigramas, trigramas...)."""
    diccionario = defaultdict(list)
    for i in range(len(tokens) - n + 1):
        key = tuple(tokens[i:i + n - 1])
        next_word = tokens[i + n - 1]
        diccionario[key].append(next_word)
    return diccionario


# ==============================================================
# !5️⃣ Función de análisis de frecuencias 
# Devuelve el contador de palabras.
# ==============================================================
def contar_frecuencias(tokens):
    return Counter(tokens)
