import pandas as pd
import streamlit as st
import Preprocessor
import plotly.express as px
import plotly.graph_objects as go

df = Preprocessor.load_data()

filter_df = df

selected_crimes = Preprocessor.multiselect_main(
    "Crime Types", Preprocessor.df_crime_type
)

st.markdown(
    "<h2 id='crime-trend-year'>Crime Trends Over the Years</h2>", unsafe_allow_html=True
)
if selected_crimes:
    filtered_data = (
        filter_df.groupby(["Year", "STATE/UT"])[selected_crimes].sum().reset_index()
    )
    for crime in selected_crimes:
        fig = px.line(
            filtered_data,
            x="Year",
            y=crime,
            color="STATE/UT",
            title=f"Trend of {crime} over the Years",
            markers=True,
        )
        Preprocessor.update_chart_layout(
            fig, title=f"Trend of {crime} over the Years", x="Year", y=f"{crime}"
        )
else:
    st.write("Please select at least one valid crime type to visualize.")


st.markdown("<h2 id='crime-type-plots'>Crime Type Plots</h2>", unsafe_allow_html=True)

if selected_crimes:
    for crime in selected_crimes:
        # Sorting states by crime values
        sorted_data = filter_df.sort_values(by=crime, ascending=False)
        fig1 = px.bar(
            sorted_data,
            x="STATE/UT",
            y=crime,
            color="STATE/UT",
            title=f"{crime} by State",
            labels={"STATE/UT": "State/UT", crime: "Count"},
        )

        fig1.update_layout(xaxis={"categoryorder": "total descending"})
        Preprocessor.update_chart_layout(
            fig1, title=f"{crime} by State", x="STATE/UT", y=f"{crime}"
        )
else:
    st.write("Please select at least one valid crime type to visualize.")