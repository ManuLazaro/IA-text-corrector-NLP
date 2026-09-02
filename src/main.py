import random
import plotly.express as px
from collections import Counter

#* imports locales
from config import STOPWORDS, PENALIZACION_STOPWORDS 
from corpus import (
    cargar_corpus,
    preprocesar_texto,
    tokenizar,
    construir_diccionario,
    contar_frecuencias
)
from asistente import (
    elegir_ponderado_penalizado,
    generar_frase_random,
    sugeridor_autodetect
)
from scraper import ejecutar_scraper_si_necesario


# =========================================
#? MAIN
#* Flujo principal del programa
# =========================================

# 0️⃣ Actualizar corpus si es necesario
ejecutar_scraper_si_necesario()

# 1️⃣ Cargar, limpiar y tokenizar (desde Azure o local)
texto = cargar_corpus()
texto = preprocesar_texto(texto)  
tokens = tokenizar(texto)


# 2️⃣ Análisis de las frecuencias de las palabras (con pandas + plotly)
def mostrar_frecuencias(tokens, top=20):
    """Cuenta las palabras más comunes y muestra un gráfico interactivo."""
    df_frecuencias = contar_frecuencias(tokens)
    df_top = df_frecuencias.head(top)

    print("Palabras más comunes:")
    print(df_top.to_string(index=False))

    fig = px.bar(
        df_top,
        x="palabra",
        y="frecuencia",
        title="Palabras más frecuentes (≥2 letras, incluyendo acentos)",
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()

mostrar_frecuencias(tokens)

# 3️⃣ Construcción de n-gramas
diccionario_bigramas = construir_diccionario(tokens, n=2)
diccionario_trigramas = construir_diccionario(tokens, n=3)

# 4️⃣ Generar frase aleatoria
generar_frase_random(diccionario_bigramas, longitud=20)

# 5️⃣ Ejecutar asistente de escritura
sugeridor_autodetect(diccionario_bigramas, diccionario_trigramas)