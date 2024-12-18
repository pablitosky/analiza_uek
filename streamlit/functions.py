# Funkcje
import os
import pandas as pd
from classes import Database, Minio
import streamlit as st
from ydata_profiling import ProfileReport

db_choice = os.getenv('DATABASE', 'file')
db = Database if db_choice == 'file' else Minio()

def validate_name(name):
    if name in Database.list_datasets():
        return False
    return True


def read_file(file):
    """
    Reads a file and returns its contents as a pandas DataFrame.

    Parameters:
    file (file-like object): The file to be read. The file name should have an extension 
                             indicating the file type (e.g., 'csv', 'xlsx', 'pkl', 'parquet').

    Returns:
    pandas.DataFrame: The contents of the file as a DataFrame.

    Raises:
    ValueError: If the file type is not supported.
    """
    ext = file.name.split(".")[-1]
    if ext == "csv":
        df = pd.read_csv(file)
    elif ext == "xlsx":
        df = pd.read_excel(file)
    elif ext == "pkl":
        df = pd.read_pickle(file)
    elif ext == "parquet":
        df = pd.read_parquet(file)
    else:
        raise ValueError("File type not supported")

    return df


@st.fragment
def profile_report(df:pd.DataFrame, name:str):
    """
    Generates a profile report for the given DataFrame and displays it in a Streamlit app.

    Parameters:
    df (pd.DataFrame): The DataFrame to generate the profile report for.
    name (str): The name of the file or dataset being analyzed.

    Returns:
    None
    """
    profile = ProfileReport(
        df,
        minimal=False,
        title=f"Analiza danych z pliku {name}",
        explorative=True,
    )
    st.session_state.report_html = profile.to_html()
    st.subheader("Raport analityczny")
    with st.expander("Podgląd raportu", expanded=True):
        st.components.v1.html(st.session_state.report_html, height=800, scrolling=True)


@st.fragment
def download_report(name):
    """
    Generates a download button in a Streamlit app to download a report.

    Args:
        name (str): The name of the report file, including the extension.

    Returns:
        None
    """
    htname = name.split(".")[0]
    st.download_button(
        "Pobierz raport",
        st.session_state.report_html,
        f"{htname}.html",
        "text/html",
        on_click=None,
    )
