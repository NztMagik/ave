# streamlit_app.py

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Load secrets from secrets.toml
spreadsheet_url = st.secrets["connections.gsheets"]["spreadsheet"]
private_key = st.secrets["connections.gsheets"]["private_key"]
client_email = st.secrets["connections.gsheets"]["client_email"]
project_id = st.secrets["connections.gsheets"]["project_id"]

# Create a connection object.
conn = GSheetsConnection(
    private_key=private_key,
    client_email=client_email,
    project_id=project_id,
    spreadsheet_url=spreadsheet_url
)
#conn = st.connection("gsheets", type=GSheetsConnection)

# Initialize session state
if 'df2' not in st.session_state:
    st.session_state.df2 = conn.read(worksheet="Cotiza")

# Inputs
id = st.text_input('id')
nombre = st.text_input('nombre')
producto = st.text_input('producto')
precio = st.text_input('precio')
fecha = st.date_input('fecha')

# Lista para almacenar los nuevos datos
nuevos_datos = []

# Validar datos
if not id or not nombre or not producto or not precio or not fecha:
    st.error("Por favor, complete todos los campos")
else:
    subir_datos = pd.DataFrame({
        'OrderID': [id],
        'CustomerName': [nombre],
        'ProductList': [producto],
        'TotalPrice': [precio],
        'OrderDate': [fecha]
    })

    # Boton para mandar datos
    if st.button("mandar"):
        nuevos_datos.append(subir_datos)

        try:
            # Concatenar los nuevos datos con df2
            st.session_state.df2 = pd.concat([st.session_state.df2] + nuevos_datos, ignore_index=True)
            conn.update(worksheet="Cotiza", data=st.session_state.df2)
            st.success("Worksheet Updated ")
        except Exception as e:
            st.error("Error al subir datos: " + str(e))