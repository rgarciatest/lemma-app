import streamlit as st
import pandas as pd
import spacy
import pickle
import requests
from io import BytesIO
import os
import json
import random

def ReadTextFile(path_text):
    test_tmp = []
    for line in open(path_text): 
        if line!='\n':
            test_tmp.append(line)
    text = ''.join(test_tmp)
    return text

CONFIG = {"DB" : None,}

@st.cache_resource
def InitFirebase():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db

    # Leer la variable de entorno
    firebase_credentials_json = os.getenv('FIREBASE_CREDENTIALS')
    if not firebase_credentials_json:
        raise ValueError("La variable de entorno 'FIREBASE_CREDENTIALS' no está configurada.")
    else:
        if not firebase_admin._apps:
            # cred = credentials.Certificate('firebase-adminsdk.json')
            firebase_credentials = json.loads(firebase_credentials_json)
            cred = credentials.Certificate(firebase_credentials)
            default_app = firebase_admin.initialize_app(cred, {"databaseURL": "https://fbtesting-intl-default-rtdb.firebaseio.com",})
        else: firebase_admin.get_app()
        CONFIG["DB"] = db

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

    InitFirebase()
    if st.button("GET Firebase"):
        host = 1
        trial = 45
        ref = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').child(f'trial_{trial:03d}').get()
        st.subheader("FB")
        st.write(ref)

    # if st.button("SEND Firebase"):
    #     host = 1
    #     trial = random.randint(1,100)
    #     FIREBASEDATA = { "id": 1, "var1": random.randint(1,100), "var2": random.randint(1,100), "trial": trial }
    #     ref = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').child(f'trial_{trial:03d}').update(FIREBASEDATA)
    #     # ref = CONFIG["DB"].reference('Test').child(f'host_{subj:02d}').child(f'trial_{trial:03d}').get()
    #     ref = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').get()
    #     st.subheader("FB")
    #     st.write(ref)

    st.markdown('---')
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

