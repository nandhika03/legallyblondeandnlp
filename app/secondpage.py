# secondpage.py
import streamlit as st
import re
from collections import Counter
import base64

def run_bow():
    # Load background (optional: reuse same image if desired)
    def get_img_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    image_64 = get_img_base64("C://Users//Nandhika//Desktop//LegallyBlonde//data//bg_elle.png")
    
    #st.set_page_config(layout="wide")
    
    # Inject style
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .result-box {{
        background-color: #fff0f5;
        color: black;
        padding: 12px;
        border-radius: 10px;
        font-size: 15px;
        box-shadow: 0 0 6px rgba(255,182,193,0.3);
        margin-bottom: 20px;
        white-space: pre-wrap;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Page title
    st.markdown(
        "<h1 style='color: hotpink; text-align: center;'>Bag of Words – Elle Woods Scene</h1>",
        unsafe_allow_html=True
    )
    
    # Paragraph input
    paragraph = st.text_area(
        "Enter Paragraph for Bag of Words:", 
        """A Delta Gamma/Sigma Chi barbecue in full swing. Beautiful college students drink beer and mingle,
        trying to figure out who they're going to sleep with next. The main wall of the living room has been 
        designated as a "Model Wall" of Delta Gamma girls -- ELLE smiles at us from a Hawaiian Tropic ad and
        a Miss June USC calendar photo. A cover of an Italian Vogue shows a blonde sexpot MARGOT; a USC 
        cheerleader poster displays a hard-bodied non-blonde SERENA in a pom-pom pose.
        Serena walks up, fending off an admirer.""",
        label_visibility="collapsed"
    )
    
    # Process text
    words = re.findall(r'\b\w+\b', paragraph.lower())
    bow = Counter(words)
    
    # Slider for top N words
    top_n = st.slider("Number of words to display", min_value=5, max_value=50, value=10)
    
    # Display results
    bow_display = "\n".join([f"{word}: {count}" for word, count in bow.most_common(top_n)])
    st.markdown(f"<div class='result-box'>{bow_display}</div>", unsafe_allow_html=True)