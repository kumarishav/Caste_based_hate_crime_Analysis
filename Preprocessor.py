import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px

def load_data():
    return pd.read_csv("crime_by_district_rt_1.csv")


df_crime_type = ['Murder', 'Assault on women', 'Kidnapping and Abduction', 'Dacoity',  
                'Robbery', 'Arson', 'Hurt', 'Prevention of atrocities (POA) Act', 
                'Protection of Civil Rights (PCR) Act', 'Other Crimes Against SCs']

# standardize the state names
def standardize_state_names(df, state_column='STATE/UT'):
    df[state_column] = df[state_column].str.strip()  # Remove leading/trailing spaces
    df[state_column] = df[state_column].str.capitalize()  # Convert to Capitalize
    df[state_column] = df[state_column].str.replace('&', 'AND')  # Replace '&' with 'AND'
    df[state_column] = df[state_column].str.replace(' ut', '')  # Remove 'UT'
    df[state_column] = df[state_column].replace({
        "AANDn islands":"A AND n islands",
        "DANDn haveli":'D AND n haveli' 
    })
    return df

# multiselect function
def multiselect(title, options_list):
    select_all = st.sidebar.checkbox(f"Select all {title}", value=True, key=title)
    
    if select_all:
        selected_options = options_list
    else:
        selected_options = st.sidebar.multiselect(title, options_list)
    return selected_options

# multiselect function on main
def multiselect_main(title, options_list):
    select_all = st.sidebar.checkbox(f"Select All {title}")

    # If 'select_all' is checked, return all options
    if select_all:
        return options_list

    # Otherwise, use a multiselect widget to choose options
    selected_options = st.sidebar.multiselect(title, options_list, default=options_list[:3])
    return selected_options

    # select = st.write(f"{title}", value=True, key=title)
    # if select:
    #     selected_options = options_list
    # else:
    #     selected_options = st.sidebar.multiselect(title, options_list,default=df_crime_type[0:3])
    # return selected_options

def plot_with_plotly(data):
    fig = px.line(data_frame=data, x='Crime Type', y='Count', color='STATE/UT',markers=True)

    fig.update_layout(
        title={
            'text': '<b>Crime Trends by Type</b>',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='#FFD700', family='Georgia')
        },
        xaxis_title='<b>Crime Type</b>',
        yaxis_title='<b>Count</b>',
        plot_bgcolor='#2C2C2C',  # Dark grey background
        paper_bgcolor='#1F1F1F',  # Dark chart background
        font=dict(color='#FFD700', family='Georgia'),
        hoverlabel=dict(bgcolor="#FFD700", font_size=14, font_family="Verdana")
    )
    
    st.plotly_chart(fig)
# Type 1
def update_chart_layout(fig, title, x, y):
    fig.update_layout(
        title={
            'text': f"<b>{title}</b>",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='#FFD700', family='Georgia')
        },
        xaxis_title=f'<b>{x}</b>',
        yaxis_title=f'<b>{y}</b>',
        plot_bgcolor='#2C2C2C',
        paper_bgcolor='#1F1F1F',
        font=dict(color='#FFD700', family='Georgia'),
        hoverlabel=dict(
            bgcolor="#B3CDE0", 
            font=dict(
                color="#F5F5DC",       # Beige
                size=14,                # Font size
                family="Verdana"        # Font family
            ),
            bordercolor="#D3D3D3"
        )
    )
    st.plotly_chart(fig)


def footer(team_logo):
    st.markdown("### Team Data Detective")

# Create two columns: one for the logo, one for the team members
    col1, col2, col3 = st.columns([1,1, 3])  # Adjust column ratios 

# Column 1: Display the team logo
    with col1:
        st.image(team_logo, width=130)  # Adjust width for the logo
    with col2:
        st.markdown("")

# Column 2: Display the team members with LinkedIn links
    with col3:
        st.markdown("""
        -  [**Mohit**](https://www.linkedin.com/in/mohitag026)
        -  [**Lipika**](https://www.linkedin.com/in/k-lipika-reddy-a086262ba)
        -  [**Rishav**](https://www.linkedin.com/in/rk-rishav)
        -  [**Krushna**](https://www.linkedin.com/in/krushna-chandra-nayak-b18a55176)
        """)

