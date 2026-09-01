import random
import matplotlib.pyplot as plt
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


# 2️⃣ Análisis de las frecuencias de las palabras
def mostrar_frecuencias(tokens, top=20):
    """Cuenta las palabras más comunes y muestra un gráfico."""
    frecuencia = contar_frecuencias(tokens)
    palabras_comunes = frecuencia.most_common(top)
    print("Palabras más comunes:", palabras_comunes)

    palabras, counts = zip(*palabras_comunes)
    plt.figure(figsize=(12, 6))
    plt.bar(palabras, counts)
    plt.xticks(rotation=45)
    plt.title("Palabras más frecuentes (≥2 letras, incluyendo acentos)")
    plt.show()

mostrar_frecuencias(tokens)

# 3️⃣ Construcción de n-gramas
diccionario_bigramas = construir_diccionario(tokens, n=2)
diccionario_trigramas = construir_diccionario(tokens, n=3)

# 4️⃣ Generar frase aleatoria
generar_frase_random(diccionario_bigramas, longitud=20)

# 5️⃣ Ejecutar asistente de escritura
sugeridor_autodetect(diccionario_bigramas, diccionario_trigramas)
