import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Crime Dashboard",
    page_icon="🚔",
    layout="wide"
)

st.sidebar.success("Select a page above")

team_logo = Image.open("group_logo.jpg")  # Load team logo


# Fixed font size for the title
font_size_title = 60  # You can change this value to adjust the size

# Use the fixed font size in the HTML
st.markdown(
    f"<h1 style='text-align: center; color: #ffffff; font-size: {font_size_title}px;'>Welcome to the Hate Crime Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("")

# Fixed font size for the subtitle
font_size_subtitle = 38  # You can adjust this size as needed

# Use the fixed font size in the HTML for the subtitle
st.markdown(
    f"<h3 style='text-align: center; color: #b0bec5; font-size: {font_size_subtitle}px;'>Your comprehensive platform for understanding hate crime patterns.</h3>",
    unsafe_allow_html=True
)

st.write("")
st.write("")
st.write("")
# Add a logo to the dashboard
col1, col2 = st.columns([1, 1.5])

with col1:
    st.write("")
    st.write("")
    # Adjust the path to your team logo image
    st.image(team_logo, width=250)


with col2:
    st.write("")
    st.write("")
    st.write("")


    # Define the font sizes for the question and answers
    font_size_question = 40  # Larger size for the question
    font_size_answers = 29    # Smaller size for the answers

    # Display the formatted text with sizes applied
    st.markdown(
        f"""
        <h4 style='color: #b0bec5; font-size: {font_size_question}px;'>What insights can you expect?</h4>
        <ol>
            <li style='color: #e0e0e0; font-size: {font_size_answers}px;'>Trends in Hate Crimes Over Time</li>
            <li style='color: #e0e0e0; font-size: {font_size_answers}px;'>Regional Analysis of Crime Incidences</li>
            <li style='color: #e0e0e0; font-size: {font_size_answers}px;'>Impact of Legislation on Crime Reduction</li>
        </ol>
        """, 
        unsafe_allow_html=True
    )