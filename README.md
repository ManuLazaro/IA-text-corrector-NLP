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

---

## 🔄 **¿Cómo funciona?** (flujo del programa)

El programa sigue estos pasos, en orden:

**Conseguir el texto (el corpuus)**
El programa necesita "material" de lectura para poder aprender patrones del lenguaje. Este texto puede venir de tres sitios:
- Desde la nube (**Azure**), si hay una conexión configurada.
- Desde los archivos **locales** guardados en `data/`.
- Ampliado automáticamente con un **scraper**, que visita algunas páginas web y añade texto nuevo al corpus si detecta que está desactualizado (más de 7 días).

# ** Limpiar y preparar el texto**
Se quitan símbolos raros, etiquetas HTML, mayúsculas, etc., dejando solo palabras "limpias" en español.

** Trocear el texto en palabras (tokenización)**
El texto limpio se separa en palabras individuales, listas para ser analizadas.

** Construir los diccionarios de predicción**
Se generan dos diccionarios que guardan qué palabras suelen ir después de otras:
- **Bigramas**: predicen la siguiente palabra mirando solo **la última palabra** escrita.
- **Trigramas**: predicen la siguiente palabra mirando **las últimas dos palabras**, siendo más precisos.

Si los trigramas no encuentran una sugerencia, el programa "da un paso atrás" y prueba con bigramas, para no dejar al usuario sin opciones.

** Interactuar con el usuario**
El usuario escribe una o dos palabras, el programa consulta los diccionarios y devuelve varias sugerencias para continuar la frase. Esto se puede hacer:
- Por consola (`sugeridor_autodetect`)
- O de forma visual con botones clicables en Streamlit (`app.py`)

También existe la opción de generar una **frase completamente aleatoria** a partir del corpus, como demostración del modelo.

---

## Ejemplo de uso


---

