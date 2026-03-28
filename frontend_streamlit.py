import streamlit as st
import pandas as pd
from backend.app.service.process_statement import process_file
from backend.app.utils.excel_format import create_excel

st.title("Monthly Statement Generator")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_option = st.selectbox(
            "Select Month Range",
            [
                "Current Month",
                "Last 2 Months",
                "Last 3 Months",
                "Last 4 Months",
                "Last 5 Months",
                "All Months"
            ]
        )

    with col2:
        sub_option = st.radio(
            "Select Data",
            ["Amt Only", "Amt with Receipt No"]
        )

    df = pd.read_excel(uploaded_file, header=[0, 1])
    df = df.fillna("")
    name_col = df.columns[1]
    person_list = df[name_col].dropna().unique().tolist()

    with col3:
        selected_person = st.selectbox("Select Person", person_list)

    if st.button("Generate Statement"):

        result = process_file(
            uploaded_file,
            selected_person,
            selected_option,
            sub_option
        )

        final_df = pd.DataFrame(result)

        st.subheader("Building Point Data")
        st.dataframe(final_df)

        excel_file = create_excel(final_df, selected_person)

        st.download_button(
            label="Download File",
            data=excel_file,
            file_name="person_statement.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )