import streamlit as st
import pandas as pd

st.write("Welcome to page text")
df = pd.read_excel("data/Diccionario dr.xlsm", sheet_name="Texts")
df = df.dropna(how="all", axis=1).dropna(how="all", axis=0).reset_index(drop=True)
df.columns=["spa", "dra", "spa_lit"]
# st.write(df.head())
show_literal = st.toggle("Show literal")
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Espanol")
    st.write("\n\n".join(df["spa"].dropna().values))

with col2:
    st.header("Draurir")
    st.write("\n\n".join(df["dra"].dropna().values))

with col3:
    if show_literal:
        st.header("Literal")
        st.write("\n\n".join(df["spa_lit"].dropna().values))
    else:
        st.tabs(["Notes", "Vocab", "Media"])