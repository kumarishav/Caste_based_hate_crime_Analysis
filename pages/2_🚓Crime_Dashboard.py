import pandas as pd
import streamlit as st
import Preprocessor
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout="centered")

# =========================
# 1. Load Images
# =========================
team_logo = Image.open("group_logo.jpg")  # Load team logo

# Load the data
df = Preprocessor.load_data()

# Standardize state names
df = Preprocessor.standardize_state_names(df)

# Sidebar filters
st.sidebar.title("Filters")
selected_year = Preprocessor.multiselect("Select Year", df["Year"].unique())
selected_state = Preprocessor.multiselect("Select State", df["STATE/UT"].unique())

# Apply global filter
filter_df = df[(df["Year"].isin(selected_year)) & (df["STATE/UT"].isin(selected_state))]

# Dashboard title
st.title("Hate Crime Analysis 🚨")
st.markdown("---")

# Display KPIs
# creating columns for Induccators or KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Crimes", value=int(filter_df["Total Crimes"].sum()))
with col2:
    st.metric(label="Murder", value=int(filter_df["Murder"].sum()))
with col3:
    st.metric(label="Assault on women", value=int(filter_df["Assault on women"].sum()))
with col4:
    st.metric(
        label="Kidnapping and Abduction",
        value=int(filter_df["Kidnapping and Abduction"].sum()),
    )


col5, col6, col7 = st.columns(3)
with col5:
    st.metric(label="Robbery", value=int(filter_df["Robbery"].sum()))
with col6:
    st.metric(label="Arson", value=int(filter_df["Arson"].sum()))
with col7:
    st.metric(label="Hurt", value=int(filter_df["Hurt"].sum()))

col8, col9, col10 = st.columns(3)
with col8:
    st.metric(
        label="Prevention of atrocities (POA) Act",
        value=int(filter_df["Prevention of atrocities (POA) Act"].sum()),
    )
with col9:
    st.metric(
        label="Protection of Civil Rights (PCR) Act",
        value=int(filter_df["Protection of Civil Rights (PCR) Act"].sum()),
    )
with col10:
    st.metric(
        label="Other Crimes Against SCs",
        value=int(filter_df["Other Crimes Against SCs"].sum()),
    )

st.markdown("---")

# Multiselect for crime types
selected_crimes = Preprocessor.multiselect_main(
    "Crime Types", Preprocessor.df_crime_type
)

# Plot using selected crime types
if selected_crimes:
    st.markdown(
        "<h2 id='crime-patterns'>Crime Patterns in India</h2>", unsafe_allow_html=True
    )
    filter_data = filter_df.groupby(["STATE/UT"])[selected_crimes].sum().reset_index()

    melted_data = pd.melt(
        filter_data,
        id_vars=["STATE/UT"],
        value_vars=selected_crimes,
        var_name="Crime Type",
        value_name="Count",
    )
    Preprocessor.plot_with_plotly(melted_data)
else:
    st.write("Please select at least one crime type to visualize.")

# Bar chart for selected crime types
if selected_crimes:
    crime_data = filter_df[selected_crimes].sum().reset_index()
    crime_data.columns = ["Crime Type", "Count"]

    fig_bar = px.bar(
        crime_data,
        x="Crime Type",
        y="Count",
        color="Crime Type",
        title="Crime Distribution by Type",
        labels={"Count": "Total Cases"},
    )
    Preprocessor.update_chart_layout(
        fig_bar, title="Crime Distribution by Type", x="Crime Type", y="Count"
    )

# Top 5 States with Highest Crimes
st.markdown(
    "<h2 id='top5-states'>Top 5 States with Highest Crimes</h2>", unsafe_allow_html=True
)
state_totals = (
    filter_df.groupby("STATE/UT")["Total Crimes"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig1 = px.scatter(
    state_totals,
    x="STATE/UT",
    y="Total Crimes",
    size="Total Crimes",
    color="STATE/UT",
    title="Top 5 States by Total Crimes",
    size_max=100,
)
Preprocessor.update_chart_layout(
    fig1, title="Top 5 States by Total Crimes", x="State/UT", y="Total Crimes"
)

# Crime Trends Over the Years
st.markdown(
    "<h2 id='crime-trend-year'>Crime Trends Over the Years</h2>", unsafe_allow_html=True
)
selected_crime_trend = st.sidebar.selectbox(
    "Select a Single Crime Type", Preprocessor.df_crime_type
)

if selected_crime_trend:

    filtered_data = (
        filter_df.groupby(["Year", "STATE/UT"])[selected_crime_trend]
        .sum()
        .reset_index()
    )
    fig = px.line(
        filtered_data,
        x="Year",
        y=selected_crime_trend,
        color="STATE/UT",
        title=f"Trend of {selected_crime_trend} over the Years",
        markers=True,
    )
    Preprocessor.update_chart_layout(
        fig,
        title=f"Trend of {selected_crime_trend} over the Years",
        x="Year",
        y=f"{selected_crime_trend}",
    )
else:
    st.write("Please select a valid crime type to visualize.")




# Crime Type Plots (Bar Plot for each crime type)
st.markdown("<h2 id='crime-type-plots'>Crime Type Plots</h2>", unsafe_allow_html=True)

if selected_crime_trend:

    sorted_data = filter_df.sort_values(by=selected_crime_trend, ascending=False)
    fig1 = px.bar(
            sorted_data,
            x="STATE/UT",
            y=selected_crime_trend,
            color="STATE/UT",
            title=f"{selected_crime_trend} by State",
            labels={"STATE/UT": "State/UT", selected_crime_trend: "Count"},
        )

    fig1.update_layout(xaxis={"categoryorder": "total descending"})
    Preprocessor.update_chart_layout(
            fig1, title=f"{selected_crime_trend} by State", x="STATE/UT", y=f"{selected_crime_trend}"
        )
else:
    st.write("Please select at least one valid crime type to visualize.")


# 3D Pie Chart using Plotly
if selected_crimes:
    fig_3d_pie = go.Figure(
        go.Pie(
            values=filter_df[selected_crimes[0]],
            labels=filter_df["STATE/UT"],
            hole=0.3,
            pull=[0.1] * len(filter_df),
        )
    )
    fig_3d_pie.update_traces(marker=dict(line=dict(color="#000000", width=2)))
    fig_3d_pie.update_layout(
        title_text=f"{selected_crimes[0]} Distribution by State",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig_3d_pie.update_layout(
        title={
            "text": f"<b>{selected_crimes[0]} Distribution by State</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, color="#FFD700", family="Georgia"),
        },
        plot_bgcolor="#2C2C2C",  # Dark grey background
        paper_bgcolor="#1F1F1F",  # Dark chart background
        font=dict(color="#FFD700", family="Georgia"),
        hoverlabel=dict(bgcolor="#FFD700", font_size=14, font_family="Verdana"),
    )
    st.plotly_chart(fig_3d_pie, use_container_width=True)

# District-Level Insights
st.markdown(
    "<h2 id='district-insights'>District-Level Insights</h2>", unsafe_allow_html=True
)
selected_state = st.selectbox("Select State", filter_df["STATE/UT"].unique())
district_data = filter_df[filter_df["STATE/UT"] == selected_state]

# Boxplot
if not district_data.empty:
    fig7 = px.box(
        district_data,
        x="DISTRICT",
        y="Total Crimes",
        color="DISTRICT",
        title=f"Crime Distribution in {selected_state} Districts",
    )
    Preprocessor.update_chart_layout(
        fig7,
        title=f"Crime Distribution in {selected_state} Districts",
        x="DISTRICT",
        y="Total Crimes",
    )

    if selected_crimes:
        fig = px.line(
            district_data,
            x="Year",
            y=selected_crimes[0],
            color="DISTRICT",
            title=f"{selected_crimes[0]} Trend in {selected_state}",
            markers=True,
        )
        Preprocessor.update_chart_layout(
            fig,
            title=f"{selected_crimes[0]} Trend in {selected_state}",
            x="Year",
            y=f"{selected_crimes[0]}",
        )

# Footer
st.markdown("---")
Preprocessor.footer(team_logo)
