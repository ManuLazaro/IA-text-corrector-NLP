
#* =========================================
#* GUARDA LAS CONSTANTES DE TODO EL PROYECTO
#* =========================================

STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "se", "del", "las",
    "un", "una", "por", "con", "para", "su", "es", "al", "lo"
}

DATA_PATHS = {
    "original": "data/hacker.txt",
    "extra": "data/hacker_corpus_extra.txt",
    "combined": "data/hacker_total.txt"
}

PENALIZACION_STOPWORDS = 0.4
DIAS_ACTUALIZACION_CORPUS = 7