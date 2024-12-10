import streamlit as st
import pandas as pd
# import spacy
import pickle
import requests
from io import BytesIO
import os
import json
import random

CONFIG = {"DB" : None,}

def InitFirebase():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db

    firebase_credentials_json = os.getenv('FIREBASE_CREDENTIALS')
    firebase_credentials = json.loads(firebase_credentials_json)
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        default_app = firebase_admin.initialize_app(cred, {"databaseURL": "https://fbtesting-intl-default-rtdb.firebaseio.com",})
    else: firebase_admin.get_app()
    CONFIG["DB"] = db

def main():
    height = 500
    st.title("Lematizador de Texto")
    InitFirebase()
    if st.button("GET Firebase"):
        host = 1
        trial = 45
        ref = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').child(f'trial_{trial:03d}').get()
        st.subheader("FB")
        st.write(ref)

    st.markdown('---')
    st.subheader("Texto cargado")

if __name__ == "__main__":
    main()

