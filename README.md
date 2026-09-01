# 🧠 Asistente de Escritura Predictivo (Python + IA)

Proyecto realizado en el curso de especialización en **AI Big Data**.

Es una pequeña aplicación en **Python** que funciona como un "autocompletado inteligente" de frases en español. Tú escribes una o dos palabras, y el programa te sugiere cómo podrías continuar la frase, basándose en un corpus de texto (un conjunto de textos que el programa ha "leído" previamente).

Tiene dos formas de usarse:
- 💻 **Por consola**, escribiendo palabras y recibiendo sugerencias por terminal.
- 🌐 **Con interfaz visual**, gracias a [Streamlit](https://streamlit.io/), donde puedes escribir y hacer clic directamente sobre las sugerencias.

---

## 🛠️ Tecnologías y librerías utilizadas

| Librería | Para qué se usa |
|---|---|
| `streamlit` | Crear la interfaz visual (web) de la aplicación |
| `requests` | Descargar contenido de páginas web (scraping) |
| `beautifulsoup4` | Extraer y limpiar el texto de esas páginas web |
| `matplotlib` | Mostrar gráficos con las palabras más frecuentes del corpus |
| `azure-storage-blob` | Conectarse a la nube de Microsoft Azure para descargar el corpus |
| `python-dotenv` | Leer variables de configuración sensibles (claves, rutas) desde un archivo `.env` sin exponerlas en el código |

> El proyecto también usa librerías propias de Python como `re` (expresiones regulares), `collections` y `random`, que no requieren instalación aparte.

---

## 📂 Estructura del proyecto

```
PrimeraPractica_IA/
│
├── data/                       # Corpus de texto (la "materia prima" del asistente)
│   ├── hacker.txt              # Corpus original
│   ├── hacker_corpus_extra.txt # Corpus adicional obtenido por scraping
│   └── hacker_total.txt        # Corpus combinado (original + extra)
│
├── src/
│   ├── main.py         # Punto de entrada: ejecuta todo el flujo
│   ├── config.py       # Configuración general del proyecto (rutas, ajustes)
│   ├── corpus.py       # Carga, limpieza y tokenización del texto
│   ├── asistente.py    # Lógica de sugerencias y generación de frases
│   ├── scraper.py      # Descarga texto de internet para ampliar el corpus
│   ├── app.py          # Interfaz visual con Streamlit
│   └── prueba.py       # Archivo de pruebas
│
├── .env_example         # Ejemplo de variables de entorno necesarias
├── requirements.txt      # Lista de librerías necesarias para instalar el proyecto
└── README.md
```

---

## 🔄 ¿Cómo funciona? (flujo del programa)

El programa sigue estos pasos, en orden:

**1️⃣ Conseguir el texto (el corpus)**
El programa necesita "material" de lectura para poder aprender patrones del lenguaje. Este texto puede venir de tres sitios posibles:
- Desde **Azure** (la nube), si hay una conexión configurada.
- Desde los archivos **locales** guardados en `data/`.
- Ampliado automáticamente con un **scraper**, que visita algunas páginas web y añade texto nuevo al corpus si detecta que está desactualizado (más de X días).

**2️⃣ Limpiar y preparar el texto**
Se quitan símbolos raros, etiquetas HTML, mayúsculas, etc., dejando solo palabras "limpias" en español.

**3️⃣ Trocear el texto en palabras (tokenización)**
El texto limpio se separa en palabras individuales, listas para ser analizadas.

**4️⃣ Construir los diccionarios de predicción**
Aquí está el corazón del asistente: se generan dos diccionarios que guardan qué palabras suelen ir después de otras:
- **Bigramas**: predicen la siguiente palabra mirando solo **la última palabra** escrita.
- **Trigramas**: predicen la siguiente palabra mirando **las últimas dos palabras**, siendo más precisos.

Si los trigramas no encuentran una sugerencia, el programa "da un paso atrás" y prueba con bigramas, para no dejar al usuario sin opciones.

**5️⃣ Interactuar con el usuario**
El usuario escribe una o dos palabras, el programa consulta los diccionarios y devuelve varias sugerencias para continuar la frase. Esto se puede hacer:
- Por consola (`sugeridor_autodetect`)
- O de forma visual con botones clicables en Streamlit (`app.py`)

También existe la opción de generar una **frase completamente aleatoria** a partir del corpus, como demostración del modelo.

---

## 📸 Ejemplo de uso

*(Aquí irán las capturas de pantalla mostrando la aplicación en funcionamiento)*

---

## ✅ Resumen

Este proyecto demuestra el uso de:
- Python aplicado a procesamiento de lenguaje natural (NLP) básico
- Modelos estadísticos simples de texto (n-gramas)
- Web scraping responsable
- Conexión con servicios en la nube (Azure)
- Creación de una interfaz visual sencilla con Streamlit
