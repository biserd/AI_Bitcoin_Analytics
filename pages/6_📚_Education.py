
import streamlit as st
from components.education import display_education_section

st.set_page_config(page_title="Education", page_icon="📚", layout="wide")

st.title("Educational Resources")
st.markdown("Learn about Bitcoin ETFs, On-Chain Metrics, and how to use this dashboard effectively")

# Display education content
display_education_section()
