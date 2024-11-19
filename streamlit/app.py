import streamlit as st
import pandas as pd
import functions as f
import os
from classes import Database

st.set_page_config(layout="wide")
st.subheader("""Analiza i projektowanie obiektowe""")

data_tab, analysis_tab, visual_tab, auto_tab = st.tabs(
    ["Dane", "Analiza", "Wizualizacja", "Automatyzacja"]
)

with data_tab:
    data = st.file_uploader("Upload new dataset", type=["csv", "xlsx"])
    if data:
        st.write("Data preview:")
        df = pd.read_csv(data)
        st.dataframe(df.head(10))
        default_name = str(data.name).split(".")[0]
        name = st.text_input("Dataset name", value=default_name)
        add_button = st.button("Add to database")
        if add_button:
            if f.validate_name(name):
                Database.add_to_database(df, name)
                st.success("Dataset added to database")
            else:
                st.warning(
                    "Dataset with this name already exists, please change the name."
                )

    # List all datasets
    with st.expander("Available datasets:", expanded=False):
        dataset_names = Database.list_datasets()
        for name in dataset_names:
            st.write(f"*{name}*")

with analysis_tab:
    dataset_names = Database.list_datasets()
    dataset_name = st.selectbox("Select dataset", dataset_names)

    # ładowanie datasetu
    dataset = Database.load_dataset(dataset_name)
    # dynamic df
    df = dataset.df.copy()
    c1, c2 = st.columns(2)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    with st.expander("Dataset preview", expanded=False):
        query = st.text_input("Filter", key="filter")
        if query is not None and query != "":
            df = df.query(query)
            st.text(f"Query: {query}")
            st.write("Filtered rows: ", df.shape[0])
        st.dataframe(df)

    with st.expander("Dataset info", expanded=False):
        st.dataframe(df.describe())
        st.dataframe(df.dtypes)
