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
    # trial = 45
    trial = st.number_input("Get trial", value=45)
    st.write("The current number is ", trial)
    trial = int(trial)
    if st.button("GET Firebase"):
        host = 1
        ref_get = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').child(f'trial_{trial:03d}').get()
        st.subheader("FB")
        st.write(ref_get)

    st.markdown('---')
    with st.container():
        # trial_in = random.randint(1,100)
        trial_in = st.number_input("Update trial", value=45)
        trial_in = int(trial_in)
        st.write("The current number is ", trial_in)
        if st.button("SEND Firebase"):
            host = 1
            FIREBASEDATA = { "id": 1, "var1": random.randint(1,100), "var2": random.randint(1,100), "trial": trial_in }
            ref_up = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').child(f'trial_{trial_in:03d}').update(FIREBASEDATA)
            # ref = CONFIG["DB"].reference('Test').child(f'host_{subj:02d}').child(f'trial_{trial_in:03d}').get()
            # ref = CONFIG["DB"].reference('Test').child(f'host_{host:02d}').get()
            # st.subheader("FB")
            # st.write(ref)

    st.markdown('---')

if __name__ == "__main__":
    main()

