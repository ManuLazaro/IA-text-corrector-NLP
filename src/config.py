
#* =========================================
#* GUARDA LAS CONSTANTES DE TODO EL PROYECTO
#* =========================================

import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("spanish"))

DATA_PATHS = {
    "original": "data/hacker.txt",
    "extra": "data/hacker_corpus_extra.txt",
    "combined": "data/hacker_total.txt"
}

PENALIZACION_STOPWORDS = 0.4
DIAS_ACTUALIZACION_CORPUS = 7