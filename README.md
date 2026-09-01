# 🧠 Asistente de Escritura Predictivo (Python + IA)

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red) ![Azure](https://img.shields.io/badge/Azure-Blob%20Storage-0078D4)

Proyecto realizado en el curso de especialización en **AI Big Data**.

Es una pequeña aplicación en **Python** que funciona como un "autocompletado inteligente" de frases en español. Tú escribes una o dos palabras, y el programa te sugiere cómo podrías continuar la frase, basándose en un corpus de texto (un conjunto de textos que el programa ha "leído" previamente).

Tiene dos formas de usarse:
- 💻 **Por consola**, escribiendo palabras y recibiendo sugerencias por terminal.
- 🌐 **Con interfaz visual**, gracias a [Streamlit](https://streamlit.io/), donde puedes escribir y hacer clic directamente sobre las sugerencias.

---

## 💻 Tecnologías con las que trabajo

Más allá de las librerías concretas, este proyecto pone en práctica dos bloques principales:

- **Python** como lenguaje base de todo el desarrollo: desde la lógica de procesamiento de texto hasta la construcción de los modelos de predicción (n-gramas) y la interfaz de usuario.
- **Microsoft Azure**, en concreto el servicio **Azure Blob Storage**, para poder alojar el corpus de texto en la nube y que el programa lo descargue automáticamente en lugar de depender solo de archivos locales. Si no hay conexión configurada, el programa cae de forma automática ("fallback") a usar los archivos locales de la carpeta `data/`.

---

## 🛠️ Librerías utilizadas

| Librería | Para qué se usa |
|---|---|
| `streamlit` | Crear la interfaz visual (web) de la aplicación |
| `requests` | Descargar contenido de páginas web (scraping) |
| `beautifulsoup4` | Extraer y limpiar el texto de esas páginas web |
| `matplotlib` | Mostrar gráficos con las palabras más frecuentes del corpus |
| `azure-storage-blob` | Conectarse a la nube de Microsoft Azure para descargar el corpus |
| `python-dotenv` | Leer variables de configuración sensibles (claves, rutas) desde un archivo `.env` sin exponerlas en el código |

> El proyecto también usa librerías propias de Python
> - **`re`** (expresiones regulares) 
> - **`collections`** → para contar palabras y organizar las sugerencias por frecuencia.
> - **`random`** → para elegir sugerencias de forma variada y generar frases aleatorias.
>

---

## 🔄 ¿Cómo funciona? (flujo del programa)

El programa sigue estos pasos, en orden:

**1️⃣ Conseguir el texto (el corpus)**
El programa necesita "material" de lectura para poder aprender patrones del lenguaje. Este texto puede venir de tres sitios:
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

![Primera captura](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183224.png)
![Escribimos una o mas palabras](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183245.png)
![Seguimos escribiendo](./Ejemplos/Captura%20de%20pantalla%202026-09-01%2018349.png)
![Resultado final](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183403.png)

---

