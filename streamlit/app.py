import streamlit as st
import pandas as pd
import functions as f
import os
from functions import db, db_choice
import plotly.express as px
import streamlit.components.v1 as components


st.set_page_config(layout="wide")
st.subheader("""Analiza i projektowanie obiektowe""")
st.session_state["df"] = pd.DataFrame()

data_tab, analysis_tab, visual_tab, auto_tab = st.tabs(
    ["Dane", "Analiza", "Wizualizacja", "Automatyzacja"]
)

with data_tab:
    st.write(f"### Zarządzanie danymi w bazie `{db_choice}`")
    data = st.file_uploader(
        "Załaduj nowy zbiór danych", type=["csv", "xlsx", "pkl", "parquet"]
    )
    if data:
        st.write("Data preview:")
        df = f.read_file(data)
        st.dataframe(df.head(10))
        default_name = str(data.name).split(".")[0]
        name = st.text_input("Dataset name", value=default_name)
        add_button = st.button("Dodaj do bazy")
        if add_button:
            if db.validate_name(name):
                db.add_to_database(df, name)
                st.success("Dodano do bazy")
            else:
                st.warning(
                    "Zbiór danych istnieje, zmień nazwę."
                )

    # List all datasets
    with st.expander("Dostępne zbiory danych:", expanded=True):
        dataset_names = db.list_datasets()
        
        for ix, name in enumerate(dataset_names):
            c1, c2, c3, _ = st.columns([2, 1, 1, 4])
            c1.write(f"*{ix+1}*. **{name}**")
            with c2.popover("Pobierz"):
                dataset = db.load_dataset(name)
                st.download_button(
                    label="CSV",
                    data=dataset.df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{name}.csv",
                    mime="text/csv",
                )

            with c3.popover("Usuń"):
                st.write(f"Czy chcesz usunąć plik?")
                if st.button("Tak", key=str(ix) + "remove"):
                    success = db.remove_dataset(name)
                    if success:
                        st.toast("Plik usunięty")
                    else:
                        st.toast("Wystąpił błąd podczas usuwania pliku")
                    st.rerun()

with analysis_tab:
    st.write(f"### Analiza i filtrowanie danych")
    dataset_names = db.list_datasets()
    if len(dataset_names) == 0:
        st.warning("Brak dostępnych zbiorów danych")
        st.stop()
    dataset_name = st.selectbox("Select dataset", dataset_names)

    # ładowanie datasetu
    dataset = db.load_dataset(dataset_name)
    st.session_state.df = dataset.df
    # dynamic df
    df = dataset.df.copy()
    c1, c2 = st.columns(2)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    with st.expander("Dataset preview", expanded=True):
        query = st.text_input("Filter", key="filter")
        if query is not None and query != "":
            df = df.query(query)
            st.text(f"Query: {query}")
            st.write("Filtered rows: ", df.shape[0])
        st.dataframe(df)

        def set_session_dataframe(df):
            st.session_state.df = df
            st.session_state.dfname = dataset_name
            st.toast("Zbiór danych ustawiony w sesji")

        st.button("Ustaw zbiór danych w sesji", on_click=set_session_dataframe, args=(df,))

    with st.expander("Dataset info", expanded=False):
        df_desc = df.describe()
        df_types = df.dtypes.to_frame().T.rename(index={0: "dtype"})
        # transpose df_types and concat df_desc with df_types
        df_info = pd.concat([df_desc, df_types])
        st.dataframe(df_info)

with visual_tab:
    st.write("### Dynamiczne Wizualizacje")
    if "dfname" not in st.session_state:
        st.warning("Ustaw zbiór w sesji w zakładce Analiza")
        st.stop()
    else:
        st.write(f"Zbiór danych: `{st.session_state.dfname}`")
    c1, c2 = st.columns([1, 4])
    with c1:

        st.write("")
        chart_config = {
            "scatter": dict(func=px.scatter, single_col=["x", "y", "color"]),
            "scatter_matrix": dict(
                func=px.scatter_matrix, single_col=["color"], multi_col=["dimensions"]
            ),
            "bar": dict(
                func=px.bar,
                single_col=["x", "y", "color"],
                kwargs={"barmode": ["group", "stack", "overlay"]},
            ),
            "pie": dict(func=px.pie, single_col=["values", "names"]),
            "line": dict(func=px.line, single_col=["x", "y", "color"]),
            "area": dict(func=px.area, single_col=["x", "y", "color"]),
            "histogram": dict(
                func=px.histogram,
                single_col=["x", "y", "color"],
                kwargs={"histfunc": ["count", "sum", "avg"]},
            ),
        }

        chart_name = st.selectbox("Wybierz Typ Wykresu", list(chart_config.keys()))
        color = st.selectbox(
            "Color", ["default", "viridis", "greens", "rainbow", "sunsetdark"]
        )

        chart = chart_config.get(chart_name)
        conf = {}
        with st.form("Dynamic Visuals"):
            cols = list(df.columns)
            for ix, col in enumerate(chart["single_col"]):
                conf[col] = st.selectbox(col, cols, index=min(ix, len(cols)))

            for ix, col in enumerate(chart.get("multi_col") or []):
                conf[col] = st.multiselect(col, cols)

            for key, vals in (chart.get("kwargs") or {}).items():
                if type(vals) == list:
                    conf[key] = st.selectbox(key, vals)
                else:
                    conf[key] = vals
            st.form_submit_button("Apply")

        color_discrete = {
            "viridis": px.colors.sequential.Viridis,
            "greens": px.colors.sequential.Greens,
            "geyser": px.colors.sequential.Plasma,
            "rainbow": px.colors.sequential.Rainbow,
            "sunsetdark": px.colors.sequential.Sunsetdark,
            "default": None,
        }
        # color_discrete_sequence=color_discrete[color]
    with c2:
        fig = chart["func"](
            df,
            **conf,
        )
        fig.update_layout(height=600)

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


with auto_tab:
    st.markdown("### Automatyczna analiza eksploracyjna")
    if "dfname" not in st.session_state:
        st.warning("Wybierz zbiór danych w zakładce Analiza")
        st.stop()
    else:
        st.write(f"Zbiór danych: `{st.session_state.dfname}`")

    if st.button("Generuj Raport"):
        with st.spinner("Generowanie raportu..."):
            f.profile_report(df, name)
            f.download_report(dataset.name)
