from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Diccionario Draurur",
    page_icon=":sailboat:",  # This is an emoji shortcode. Could be a URL too.,
    layout="wide",
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
