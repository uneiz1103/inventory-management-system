import streamlit as st
import pandas as pd

from db_functions import *

# sidebar
st.sidebar.title("Inventory Management Dashboard")
option = st.sidebar.radio("Select an option", ["Basic Information", "Operational Tasks"])

# main space
st.title("SONA Inventory and Supply Chain Dashboard")
db = connect_to_db()
cursor = db.cursor(dictionary=True)

# -------------------------- BASIC INFORMATION PAGE --------------------------
if option == "Basic Information":
    st.header("Basic Metrics")

# get basic information from DB
    basic_info = get_basic_info(cursor)

    cols = st.columns(3)
    keys = list(basic_info.keys())

    for i in range(3):
        cols[i].metric(label=keys[i], value=basic_info[keys[i]])

    cols = st.columns(3)
    for i in range(3, 6):
        cols[i - 3].metric(label=keys[i], value=basic_info[keys[i]])

    st.divider()

    # fetch and display detailed tables
    tables = get_additional_tables(cursor)
    for labels, data in tables.items():
        st.header(labels)
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.divider()

elif option == "Operational Tasks":
    st.header("Operational Tasks")
    selected_task = st.selectbox("Choose a Task", ["Add New Product", "Product History", "Place Reorder", "Receive Reorder"])























# ----------------------------- product History -----------------------------
