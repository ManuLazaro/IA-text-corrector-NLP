# <img src="https://api.iconify.design/lucide:brain.svg?color=%236366f1" height="26" style="vertical-align: -5px;" /> Asistente de Escritura Predictivo (Python + IA)

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red) ![Azure](https://img.shields.io/badge/Azure-Blob%20Storage-0078D4)

Proyecto realizado en el curso de especialización en **AI Big Data**.

Es una pequeña aplicación en **Python** que funciona como un "autocompletado inteligente" de frases en español. Tú escribes una o dos palabras, y el programa te sugiere cómo podrías continuar la frase, basándose en un corpus de texto (un conjunto de textos que el programa ha "leído" previamente).

Tiene dos formas de usarse:
- <img src="https://api.iconify.design/lucide:terminal.svg?color=%238B90A0" height="16" style="vertical-align: -3px;" /> **Por consola**, escribiendo palabras y recibiendo sugerencias por terminal.
- <img src="https://api.iconify.design/lucide:monitor.svg?color=%238B90A0" height="16" style="vertical-align: -3px;" /> **Con interfaz visual**, gracias a [Streamlit](https://streamlit.io/), donde puedes escribir y hacer clic directamente sobre las sugerencias.

---

## <img src="https://api.iconify.design/lucide:cpu.svg?color=%2310b981" height="20" style="vertical-align: -4px;" /> Tecnologías con las que trabajo

Más allá de las librerías concretas, este proyecto pone en práctica dos bloques principales:

- **Python** como lenguaje base de todo el desarrollo: desde la lógica de procesamiento de texto hasta la construcción de los modelos de predicción (n-gramas) y la interfaz de usuario.
- **Microsoft Azure**, en concreto el servicio **Azure Blob Storage**, para poder alojar el corpus de texto en la nube y que el programa lo descargue automáticamente en lugar de depender solo de archivos locales. Si no hay conexión configurada, el programa cae de forma automática ("fallback") a usar los archivos locales de la carpeta `data/`.

---

## <img src="https://api.iconify.design/lucide:package.svg?color=%230284c7" height="20" style="vertical-align: -4px;" /> Tecnologías y librerías utilizadas

| Librería | Para qué se usa |
|---|---|
| `streamlit` | Crear la interfaz visual (web) de la aplicación |
| `pandas` | Organizar el corpus y las frecuencias de palabras en tablas (DataFrames), fáciles de ordenar y consultar |
| `numpy` | Cálculo numérico: elegir la siguiente palabra de forma ponderada (dando menos peso a las stopwords) |
| `nltk` | Procesamiento de lenguaje natural: tokenización del texto en español |
| `plotly` | Gráficos interactivos con las palabras más frecuentes del corpus (tanto por consola como en la interfaz web) |
| `requests` | Descargar contenido de páginas web (scraping) |
| `beautifulsoup4` | Extraer y limpiar el texto de esas páginas web |
| `azure-storage-blob` | Conectarse a la nube de Microsoft Azure para descargar el corpus |
| `python-dotenv` | Leer variables de configuración sensibles (claves, rutas) desde un archivo `.env` sin exponerlas en el código |

> El proyecto también usa librerías propias de Python que no requieren instalación aparte:
> - **`re`** (expresiones regulares) → limpia el texto: quita etiquetas HTML, símbolos raros y espacios sobrantes antes de trabajar con él.
> - **`collections`** → para contar palabras y organizar las sugerencias por frecuencia.
> - **`random`** → para elegir sugerencias de forma variada y generar frases aleatorias.

---

## <img src="https://api.iconify.design/lucide:rocket.svg?color=%23f59e0b" height="20" style="vertical-align: -4px;" /> Puesta en marcha

### 1. Instalar dependencias

```bash
git clone <url-del-repositorio>
cd PrimeraPractica_IA
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ejecutar por consola

```bash
cd src
python main.py
```

Al arrancar, el programa hace esto en orden:
1. Comprueba si el corpus adicional está desactualizado y, si toca, lanza el scraper para refrescarlo.
2. Carga y limpia el corpus (desde Azure si hay conexión configurada, o desde `data/` en local).
3. Muestra por pantalla un gráfico con las palabras más frecuentes.
4. Genera una frase de ejemplo completamente aleatoria.
5. Abre el asistente interactivo por terminal:
   - Escribe **1 palabra** (usa bigramas) o **2 palabras** (usa trigramas) para empezar.
   - El programa te muestra hasta 5 sugerencias para continuar la frase.
   - Escribe la siguiente palabra (o varias) para seguir construyendo la frase.
   - Comandos disponibles en cualquier momento: `nueva` (empezar otra frase) y `salir` (terminar el programa).

### 3. Ejecutar con interfaz gráfica

```bash
cd src
streamlit run app.py
```

Se abrirá una pestaña en el navegador con la versión visual del asistente: la frase se ve como si la estuvieras escribiendo en un editor, y las sugerencias aparecen debajo como botones en los que puedes hacer clic.

---

## <img src="https://api.iconify.design/lucide:workflow.svg?color=%238b5cf6" height="20" style="vertical-align: -4px;" /> ¿Cómo funciona? (flujo del programa)

El programa sigue estos pasos, en orden:

**1. Conseguir el texto (el corpus)**
El programa necesita "material" de lectura para poder aprender patrones del lenguaje. Este texto puede venir de tres sitios posibles:
- Desde **Azure** (la nube), si hay una conexión configurada.
- Desde los archivos **locales** guardados en `data/`.
- Ampliado automáticamente con un **scraper**, que visita algunas páginas web y añade texto nuevo al corpus si detecta que está desactualizado (más de X días).

**2. Limpiar y preparar el texto**
Se quitan símbolos raros, etiquetas HTML, mayúsculas, etc., dejando solo palabras "limpias" en español.

**3. Trocear el texto en palabras (tokenización)**
El texto limpio se separa en palabras individuales, listas para ser analizadas.

**4. Construir los diccionarios de predicción**
Aquí está el corazón del asistente: se generan dos diccionarios que guardan qué palabras suelen ir después de otras:
- **Bigramas**: predicen la siguiente palabra mirando solo **la última palabra** escrita.
- **Trigramas**: predicen la siguiente palabra mirando **las últimas dos palabras**, siendo más precisos.

Si los trigramas no encuentran una sugerencia, el programa "da un paso atrás" y prueba con bigramas, para no dejar al usuario sin opciones.

**5. Interactuar con el usuario**
El usuario escribe una o dos palabras, el programa consulta los diccionarios y devuelve varias sugerencias para continuar la frase. Esto se puede hacer:
- Por consola (`sugeridor_autodetect`)
- O de forma visual con botones clicables en Streamlit (`app.py`)

También existe la opción de generar una **frase completamente aleatoria** a partir del corpus, como demostración del modelo.

---

## <img src="https://api.iconify.design/lucide:image.svg?color=%230284c7" height="20" style="vertical-align: -4px;" /> Ejemplo de uso

![Primera captura](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183224.png)
![Escribimos una o mas palabras](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183245.png)
![Seguimos escribiendo](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183349.png)
![Resultado final](./Ejemplos/Captura%20de%20pantalla%202026-09-01%20183403.png)

---

## <img src="https://api.iconify.design/lucide:check-circle-2.svg?color=%2310b981" height="20" style="vertical-align: -4px;" /> Resumen

Este proyecto demuestra el uso de:
- Python aplicado a procesamiento de lenguaje natural (NLP) básico
- Modelos estadísticos simples de texto (n-gramas)
- Web scraping responsable
- Conexión con servicios en la nube (Azure)
- Creación de una interfaz visual sencilla con Streamlit
