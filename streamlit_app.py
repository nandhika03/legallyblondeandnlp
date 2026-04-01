import streamlit as st
from app.app_home import run_home
from app.secondpage import run_bow

# Page config must be first command
st.set_page_config(page_title="Legally NLP", layout="wide")

# Page selection
page = st.selectbox("Choose Page", ["Home", "Bag of Words"])

if page == "Home":
    run_home()
else:
    run_bow()