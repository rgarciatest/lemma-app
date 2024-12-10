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
def cargar_modelo():


    url = "https://drive.google.com/uc?id=1zspq3faEXDqRQZzpIn0mxRil_40FczwA&export=download"
    response = requests.get(url)
    if response.status_code == 200:
        archivo_pkl = BytesIO(response.content)
        nlp = pickle.load(archivo_pkl)
        print(nlp)
    else:
        print("Error al descargar el archivo. Código de estado:", response.status_code)

    SPACY_MODEL = 'es_core_news_sm'
    # SPACY_MODEL = 'es_core_news_lg'
    # with open(f"spacy_es/{SPACY_MODEL}.pkl", "rb") as f:
    #     nlp = pickle.load(f)

    # nlp = spacy.load(SPACY_MODEL)
    
    # texto = "Los perros corren rápidamente."
    # doc = nlp(texto)
    # lemmas = [token.lemma_ for token in doc]
    # print("Texto lematizado:", " ".join(lemmas))
    return nlp 

def lematizar_texto(texto, nlp):
    # Procesar el texto con SpaCy
    doc = nlp(texto)
    # Lematizar cada palabra del texto
    lemas = [token.lemma_ for token in doc]
    return ' '.join(lemas)

def main():
    height = 500
    st.title("Lematizador de Texto en Español con Modelo Remoto")
    
    # Cargar el modelo de SpaCy
    nlp = cargar_modelo()
    
    # Subir archivo de texto
    # uploaded_file = st.file_uploader("Sube un archivo de texto", type="txt")
    uploaded_file = ReadTextFile('diag-sample.txt')

    if uploaded_file is not None:
        # Leer el contenido del archivo
        # texto = uploaded_file.read().decode("utf-8")
        texto = uploaded_file
        st.subheader("Texto cargado")
        st.text_area("Texto original", texto, height=height)
        
        # Lematizar el texto
        texto_lema = lematizar_texto(texto, nlp)
        st.subheader("Texto lematizado")
        st.text_area("Texto lematizado", texto_lema, height=height)
    
    # Opción para ingresar texto manualmente
    else:
        texto_input = st.text_area("Ingresa el texto que deseas lematizar", "")
        
        if st.button("Lematizar"):
            if texto_input:
                # Lematizar el texto ingresado manualmente
                texto_lema_input = lematizar_texto(texto_input, nlp)
                st.subheader("Texto lematizado")
                st.text_area("Texto lematizado", texto_lema_input, height=height)
            else:
                st.warning("Por favor ingresa algún texto para lematizar.")
            
if __name__ == "__main__":
    main()

