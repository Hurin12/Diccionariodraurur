import streamlit as st

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Diccionario Teónico",
    page_icon=":scroll:",  # This is an emoji shortcode. Could be a URL too.,
    layout="wide",
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown("<p class='pre-header'>Accede al diccionario de teónico</p>", unsafe_allow_html=True)
st.markdown("<h1><a href='/Teonico' target='_self' class='invisible-link'>Diccionario Teónico</a></h1>", unsafe_allow_html=True)

st.markdown("<p class='pre-header'>Página de ventas del libro</p>", unsafe_allow_html=True)
st.markdown("<h1><a href='/Teonico' target='_self' class='invisible-link'>Adquiere un ejemplar</a></h1>", unsafe_allow_html=True)
