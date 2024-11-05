import streamlit as st
import pandas as pd
import functions as f
    
st.set_page_config(layout="wide")
st.subheader("""Analiza i projektowanie obiektowe""")

data_tab, analysis_tab, visual_tab, auto_tab = st.tabs(["Dane", "Analiza", "Wizualizacja", "Automatyzacja"])

with data_tab:
    data = st.file_uploader("Upload new dataset", type=["csv", 'xlsx'])
    if data:
        st.write("Data preview:")
        df = pd.read_csv(data)
        st.dataframe(df)
        name = st.text_input("Dataset name", value=data.name)
        st.button("Add to database")