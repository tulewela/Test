import streamlit as st
import streamlit.components.v1 as components

# Seitenkonfiguration
st.set_page_config(
    page_title="Taschenrechner App",
    page_icon="🧮",
    layout="centered"
)

# HTML-Datei einlesen
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# HTML & JS in Streamlit darstellen
components.html(html_code, height=650, scrolling=False)
