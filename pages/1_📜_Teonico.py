import streamlit as st
import pandas as pd
import numpy as np
import unicodedata

import constants
import labels


# Normalize string by removing accents
def normalize_string(s):
    return (
        "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )
        .strip()
        .lower()
    )


# Parse the definitions and examples
def parse_definitions_examples(definition_str, example_str):
    definitions = [d.strip() for d in definition_str.split(", 2.")]
    examples = [e.strip() for e in example_str.split(", 2.")]
    return definitions, examples


def generate_search_key(teonico: str, plural: str, verbs: str) -> str:
    if not plural and not verbs:
        return teonico
    return f"{teonico} | {plural}{verbs}"


with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


file_path = "data/teonicodicc.xlsx"

st.markdown(
    "<h1><a href='/' target='_self' class='invisible-link'>Diccionario Teónico</a></h1>",
    unsafe_allow_html=True,
)

df = pd.read_excel(file_path).dropna(how="all", axis=1)
if df is None:
    st.error("Teonico excel file not loaded correctly")
    st.stop()

verb_cols = [f"v{i}{j}" for i in range(1, 5) for j in range(1, 4)]
df_extra = df[verb_cols].values.tolist()
df["verbs_extra"] = [", ".join(v) if not pd.isna(v[0]) else None for v in df_extra]
df["search_key"] = df.fillna("").apply(
    lambda row: generate_search_key(row["teonico"], row["plural"], row["verbs_extra"]),
    axis=1,
)

word = st.selectbox(
    labels.teo_dropdown_label,
    sorted(df["search_key"]),
    index=None,
    placeholder=labels.dropdown_placeholder,
    format_func=normalize_string,
)

if word:
    word_row = (
        df[
            df["search_key"].astype(str).apply(normalize_string)
            == normalize_string(word)
        ]
        .iloc[0]
        .replace({np.nan: None})
    )

    word_header = f"<h2 style='color:{constants.color_word_complex};'> {word_row["teonico"]} </h2>"
    st.markdown(word_header, unsafe_allow_html=True)

    if word_row["etimologia"]:
        st.write(f":{constants.color_etimology}[{word_row["etimologia"]}]")

    word_def = f"1. **{word_row["cat1"]}** {word_row["def1"]}"
    if word_row["def2"]:
        word_def += f"\n1. **{word_row["cat2"]}** {word_row["def2"]}"
    st.markdown(word_def)

    if word_row["cat1"] in constants.categories_plural and word_row["plural"]:
        plural = f"**Plural:** {word_row["plural"]}"
        st.write(plural)

    if word_row["cat1"] in constants.categories_verb:
        current_verb = word_row[verb_cols]
        verb_table = current_verb.fillna("-").values.reshape(4, 3)
        verb_table = pd.DataFrame(
            verb_table,
            columns=["Presente", "Pretérito Perfecto", "Futuro"],
            index=["1ª Pers. Sing.", "2ª Pers. Sing.", "3ª Pers. Sing.", "Plural"],
        )
        st.table(verb_table)
