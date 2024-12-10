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
    # url = "https://drive.google.com/uc?id=1zspq3faEXDqRQZzpIn0mxRil_40FczwA&export=download"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     archivo_pkl = BytesIO(response.content)
    #     nlp = pickle.load(archivo_pkl)
    #     print(nlp)
    # else:
    #     print("Error al descargar el archivo. Código de estado:", response.status_code)



    # SPACY_MODEL = 'es_core_news_sm'
    # SPACY_MODEL = 'es_core_news_lg'
    # with open(f"spacy_es/{SPACY_MODEL}.pkl", "rb") as f:
    #     nlp = pickle.load(f)

    nlp = spacy.load(SPACY_MODEL)
    
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
    
    opciones = ["es_core_news_sm", "en_core_web_sm", "es_core_news_lg"]

    # # Creando el multiselect
    # seleccionadas = st.multiselect(
    #     "Selecciona una o varias opciones:",
    #     opciones,
    #     default=["es_core_news_sm"]  # Opción seleccionada por defecto
    # )

    # Creando el selectbox
    SPACY_MODEL = st.selectbox(
        "Selecciona una opción:",
        opciones,
        index=0  # Índice de la opción seleccionada por defecto (opcional)
    )

    # Mostrando la opción seleccionada
    st.write("Has seleccionado:", SPACY_MODEL)


    # SPACY_MODEL = 'es_core_news_sm'
    # SPACY_MODEL = 'es_core_news_lg'
    # Cargar el modelo de SpaCy
    nlp = cargar_modelo(SPACY_MODEL)
    
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

