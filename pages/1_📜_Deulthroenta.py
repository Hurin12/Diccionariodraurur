import streamlit as st
import pandas as pd
import unicodedata

import labels


# Normalize string by removing accents
def normalize_string(s):
    return (
        "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )
        .lower()
        .strip()
    )


# Load the Excel file
def load_data(file_path):
    try:
        # Read the Excel file, specifying the sheet and row to start
        df = pd.read_excel(file_path, sheet_name="Diccionario", header=None, skiprows=7)
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None


# Parse the definitions and examples
def parse_definitions_examples(definition_str, example_str):
    definitions = [d.strip() for d in definition_str.split(", 2.")]
    examples = [e.strip() for e in example_str.split(", 2.")]
    return definitions, examples


# Function to get word details
def get_word_details(word, df):
    # Normalize the input word
    normalized_word = normalize_string(word)

    # Ensure the word is treated as a string
    word = str(word).strip().lower()

    # Check for nouns
    noun_data = df[df.iloc[:, 1].astype(str).apply(normalize_string) == normalized_word]

    if not noun_data.empty:
        row = noun_data.iloc[0]
        noun_details = {
            "category": "Noun",
            "short_translation": str(row[2]) if pd.notna(row[2]) else "N/A",
            "gender": str(row[3]) if pd.notna(row[3]) else "N/A",
            "etymology": str(row[4]) if pd.notna(row[4]) else "N/A",
            "definitions": [],
            "examples": [],
        }

        definitions, examples = parse_definitions_examples(str(row[5]), str(row[6]))
        noun_details["definitions"].extend(definitions)
        noun_details["examples"].extend(examples)
        return noun_details

    # Check for verbs
    verb_data = df[df.iloc[:, 7].astype(str).str.strip().str.lower() == word]

    if not verb_data.empty:
        row = verb_data.iloc[0]
        verb_details = {
            "category": "Verb",
            "short_translation": str(row[9]) if pd.notna(row[9]) else "N/A",
            "etymology": str(row[10]) if pd.notna(row[10]) else "N/A",
            "definitions": [],
            "examples": [],
        }

        definitions, examples = parse_definitions_examples(str(row[11]), str(row[12]))
        verb_details["definitions"].extend(definitions)
        verb_details["examples"].extend(examples)
        return verb_details

    return None


# Streamlit UI
st.title("Diccionario Draur")

df = load_data("Diccionario dr.xlsm")
noun_list = df.iloc[:, 1].dropna().tolist()
verb_list = df.iloc[:, 7].dropna().tolist()
words_list = noun_list + verb_list


if df is not None:  # Proceed only if the dataframe was loaded successfully
    # Input field for the word
    word = st.selectbox(
        labels.dropdown_label,
        sorted(words_list),
        index=None,
        placeholder=labels.dropdown_placeholder,
    )

    if word:
        details = get_word_details(word, df)

        if details:
            st.subheader(f"{details['category']} Details")
            st.write(f"**Short Translation (Spanish):** {details['short_translation']}")

            if details["category"] == "Noun":
                st.write(f"**Gender:** {details['gender']}")

            st.write(f"**Etimologia:** {details['etymology']}")

            st.write("**Definiciones:**")
            for definition in details["definitions"]:
                st.write(f"- {definition}")

            st.write("**Ejemplos:**")
            for example in details["examples"]:
                st.write(f"- {example}")
        else:
            st.error("Sorry, the word is not found in the dictionary.")
