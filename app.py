import streamlit as st
import pandas as pd
import spacy
import pickle
import requests
from io import BytesIO

def ReadTextFile(path_text):
    test_tmp = []
    for line in open(path_text): 
        if line!='\n':
            test_tmp.append(line)
    text = ''.join(test_tmp)
    return text

@st.cache_resource
def cargar_modelo(SPACY_MODEL):
    nlp = spacy.load(SPACY_MODEL)
    return nlp 

def lematizar_texto(texto, nlp):
    doc = nlp(texto)
    lemas = [token.lemma_ for token in doc]
    return ' '.join(lemas)

def main():
    height = 500
    st.title("Lematizador de Texto")

    SPACY_MODEL = 'es_core_news_sm'
    nlp = cargar_modelo(SPACY_MODEL)

    DATA = "es"
    uploaded_file = ReadTextFile(f'data/data-{DATA}.txt')

    if uploaded_file is not None:
        texto = uploaded_file
        st.subheader("Texto cargado")
        st.text_area("Texto original", texto, height=height)
        
        # Lematizar el texto
        texto_lema = lematizar_texto(texto, nlp)
        st.subheader("Texto lematizado")
        st.text_area("Texto lematizado", texto_lema, height=height)
    
if __name__ == "__main__":
    main()

