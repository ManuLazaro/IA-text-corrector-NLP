import random
from collections import Counter
from config import STOPWORDS, PENALIZACION_STOPWORDS
#* ==================================================================
#? Asistente
#* Contiene la lógica de generación de frases y del asistente de escritura,
#* incluyendo la ponderación y penalización de stopwords.
#* =================================================================

# ====================================================================================
# !Función: penalizadora de stopwords comunes
# Esto lo que hace es penalizar la frecuencias con la que aparecen las stopwords que hemos guardado
# El objetivo es que salgan MENOS, pero que sigan saliendo
# ==============================================================================
def elegir_ponderado_penalizado(lista_palabras):
    contador = Counter(lista_palabras) 
    total = sum(contador.values())

    # Si todas son stopwords, no penalizamos (para no romper la gramática)
    if all(pal in STOPWORDS for pal in contador):
        penalizador = {p: 1.0 for p in contador}
    else:
        # Si hay mezcla, reducimos el peso de las stopwords (p.ej. multiplicando por 0.4)
        penalizador = {p: (PENALIZACION_STOPWORDS if p in STOPWORDS else 1.0) for p in contador}

    # Creamos una lista ponderada aplicando la penalización
    ponderados = []
    for palabra, freq in contador.items():
        peso = freq * penalizador[palabra]
        ponderados.extend([palabra] * int(peso))

    if not ponderados:
        # por si la lista esta vacia
        return random.choice(lista_palabras)
    return random.choice(ponderados)

# ==================================
# ! Generador de frase aleatoria 
# Función que genera una frase a partir del diccionario de n-gramas
# ==================================
def generar_frase_random(diccionario, longitud=20, historial_repeticiones=3):
    """
    Genera una frase aleatoria a partir de un diccionario de n-gramas.
    Evita repeticiones y guarda automáticamente la frase generada.
    """
    secuencia = []

    # Elegir una clave inicial aleatoria del diccionario
    clave_inicial = random.choice(list(diccionario.keys()))
    secuencia.extend(clave_inicial)

    while len(secuencia) < longitud:
        # Usamos la última palabra como clave para bigramas
        clave_actual = tuple(secuencia[-1:])
        posibles_siguientes = diccionario.get(clave_actual)

        if not posibles_siguientes:
            break  # No hay más palabras posibles

        # Elegimos ponderado y penalizado
        siguiente_palabra = elegir_ponderado_penalizado(posibles_siguientes)

        # Evitar repeticiones inmediatas y globales (últimas 3 palabras)
        if siguiente_palabra in secuencia[-historial_repeticiones:]:
            alternativas = [p for p in posibles_siguientes if p not in secuencia[-historial_repeticiones:]]
            if alternativas:
                siguiente_palabra = random.choice(alternativas)

        secuencia.append(siguiente_palabra)

    # Guardar y mostrar
    print("Frase generada aleatoriamente:")
    frase_texto = ' '.join(secuencia)
    print(frase_texto)
    guardar_frase_final(secuencia)
    return frase_texto

# ==========================
# ! Guardar frases generadas
# ==========================
def guardar_frase_final(frase):
    """Muestra y guarda la frase generada al final del proceso."""
    if not frase:
        return
    frase_texto = ' '.join(frase)
    print("\n📝 Frase generada:")
    print(frase_texto)
    print("-" * 60)

# ==========================
# ! Sugeridor 
# ==========================
def sugeridor_autodetect(dic2, dic3):
    # --- EXPLICACION ---
    # Este es como un Asistente de Escritura. 
    # Bigramas (dic2): Predice la siguiente palabra basándose ÚNICAMENTE en la palabra anterior
    # Trigramas (dic3): Predice la siguiente palabra basándose en las DOS palabras anteriores
    # Intenta usar trigramas (más precisos) siempre que puede, y si no encuentra
    # una continuación, automáticamente 'hace un paso atrás' (backoff) y usa bigramas.
    # --------------------------------------------
    print("\n=== ASISTENTE DE ESCRITURA (auto-detect) ===")
    print("Introduce 1 palabra (para bigramas) o 2 palabras separadas por espacio (para trigramas).")
    print("Comandos dentro: 'nueva' (empezar otra secuencia), 'salir' (terminar programa).")

    while True:
        entrada = input("\nIntroduce 1 o 2 palabras iniciales (o 'salir'): ").strip().lower()
        if entrada == "salir":
            print("Saliendo. ¡Hasta luego!")
            break
        if not entrada:
            continue

        palabras = entrada.split()
        if len(palabras) == 1:
            clave = (palabras[0],)
            if clave not in dic2:
                print("La palabra no aparece en el corpus como clave (sin continuación). Prueba otra.")
                continue
            n, dic, secuencia = 2, dic2, [palabras[0]]

        elif len(palabras) == 2:
            clave = (palabras[0], palabras[1])
            if clave not in dic3:
                fallback = (palabras[1],)
                if fallback in dic2:
                    print("Haciendo backoff a bigramas usando la última palabra como clave.")
                    n, dic, secuencia = 2, dic2, [palabras[1]]
                else:
                    print("Prueba otra pareja o escribe una sola palabra.")
                    continue
            else:
                n, dic, secuencia = 3, dic3, [palabras[0], palabras[1]]
        else:
            print("Introduce únicamente 1 o 2 palabras (las 3+ no están soportadas como entrada inicial).")
            continue

        while True:
            key = tuple(secuencia[-(n-1):])
            siguientes = dic.get(key, [])

            if not siguientes and n == 3:
                key2 = (secuencia[-1],)
                siguientes = dic2.get(key2, [])
                if siguientes:
                    print("(Backoff: usando bigramas con la última palabra.)")
                    n, dic = 2, dic2

            if siguientes:
                # Filtrar stopwords de las sugerencias (aunque existan en corpus)
                contador = Counter(siguientes)
                sugerencias_filtradas = [w for w, _ in contador.most_common(15) if w not in STOPWORDS]

                #  Tomar top 5 más frecuentes y no repetidos respecto a última palabra
                sugerencias = []
                for w in sugerencias_filtradas:
                    if not secuencia or w != secuencia[-1]:
                        sugerencias.append(w)
                    if len(sugerencias) >= 5:
                        break

                if sugerencias:
                    print("Sugerencias:", ", ".join(sugerencias))
                else:
                    print("(Solo había stopwords o repeticiones, mostrando palabras originales.)")
                    sugerencias = [w for w, _ in contador.most_common(5)]
                    print("Sugerencias:", ", ".join(sugerencias))
            else:
                print("No hay sugerencias disponibles para la secuencia actual.")

            entrada_sig = input("Siguiente palabra (o 'nueva'/'salir'): ").strip().lower()
            if not entrada_sig:
                continue
            if entrada_sig == "salir":
                guardar_frase_final(secuencia)
                print("Saliendo. ¡Hasta luego!")
                return
            if entrada_sig == "nueva":
                guardar_frase_final(secuencia)
                print("Empezando nueva secuencia...")
                break

            #  Si mete varias palabras, las añadimos una a una
            nuevas_palabras = entrada_sig.split()
            secuencia.extend(nuevas_palabras)
