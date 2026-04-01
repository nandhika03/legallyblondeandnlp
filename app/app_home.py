# app_home.py
import base64
import streamlit as st
import nltk
import spacy
import re
from collections import Counter
from nltk import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer

# Wrap the whole page in a function
def run_home():

    # NLTK downloads (can skip if already downloaded)
    nltk.download("stopwords")
    nltk.download("wordnet")

    # Load SpaCy
    nlp = spacy.load("en_core_web_sm")

    # Load background
    def get_img_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    image_64 = get_img_base64("C://Users//Nandhika//Desktop//LegallyBlonde//data//bg_elle.png")

    # Page setup
    #st.set_page_config(layout="wide")

    # Inject full custom style
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    div[data-baseweb="base-input"] > textarea {{
        min-height: 70px !important;
        max-height: 100px !important;
        background-color: #ffe6f0 !important;
        color: black !important;
        font-size: 16px !important;
        border: 1px solid #ff99cc !important;
        border-radius: 10px !important;
        padding: 8px !important;
        box-shadow: 0 0 8px rgba(255, 105, 180, 0.3);
    }}

    div.stButton > button:first-child {{
        background-color: #DE3163 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
    }}

    div.stButton > button:first-child:hover {{
        background-color: #c2214f !important;
        transform: scale(1.02);
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

    # Title and intro
    st.markdown(
        "<h1 style='color: hotpink; text-align: center;'>Legally NLP </h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color: white; font-size: 20px; text-align: center;'>A visualization of the emotional wizardry of Elle Woods ✨</p>",
        unsafe_allow_html=True
    )

    # Centered input
    buff1, col, buff2 = st.columns([1, 2, 1])
    with col:
        st.markdown("<p style='color: #FF6679; text-align: center; font-size: 18px; font-weight: bold;'>Enter a quote from the Pink Slayer 💅</p>", unsafe_allow_html=True)
        sample_text = st.text_area(label="", value="I love Elle Woods!")

    # NLP Analysis
    if st.button("Analyze"):

        # Tokenization
        st.markdown("<h3 style='color:#E30B5C;'>1. Tokenized Words:</h3>", unsafe_allow_html=True)
        tokenizer = TreebankWordTokenizer()
        tokens = tokenizer.tokenize(sample_text)
        st.markdown(f"<div class='result-box'>{tokens}</div>", unsafe_allow_html=True)

        # Stopwords
        st.markdown("<h3 style='color:#E30B5C;'>2. Stopword Removal:</h3>", unsafe_allow_html=True)
        stop_words = set(stopwords.words("english"))
        no_stop = [w for w in tokens if w.lower() not in stop_words]
        st.markdown(f"<div class='result-box'>{no_stop}</div>", unsafe_allow_html=True)

        # Stemming
        st.markdown("<h3 style='color:#E30B5C;'>3. Snowball Stemming:</h3>", unsafe_allow_html=True)
        stemmer = SnowballStemmer("english")
        stems = [stemmer.stem(w) for w in no_stop]
        st.markdown(f"<div class='result-box'>{stems}</div>", unsafe_allow_html=True)

        # Lemmatization
        st.markdown("<h3 style='color:#E30B5C;'>4. Lemmatization:</h3>", unsafe_allow_html=True)
        lem = WordNetLemmatizer()
        lemmas = [lem.lemmatize(w) for w in no_stop]
        st.markdown(f"<div class='result-box'>{lemmas}</div>", unsafe_allow_html=True)

        # POS tagging
        st.markdown("<h3 style='color:#E30B5C;'>5. Parts of Speech (POS) Tagging:</h3>", unsafe_allow_html=True)
        doc = nlp(" ".join(no_stop))
        pos = [(token.text, token.pos_) for token in doc]
        st.markdown(f"<div class='result-box'>{pos}</div>", unsafe_allow_html=True)

        # Named Entity Recognition
        st.markdown("<h3 style='color:#E30B5C;'>6. Named Entity Recognition (NER):</h3>", unsafe_allow_html=True)
        doc2 = nlp(sample_text)
        ner = [(ent.text, ent.label_) for ent in doc2.ents]
        st.markdown(f"<div class='result-box'>{ner}</div>", unsafe_allow_html=True)

        # One-hot encoding
        st.markdown("<h3 style='color:#E30B5C;'>7. One-Hot Encoding (First 5 Words):</h3>", unsafe_allow_html=True)
        vocab = list(set(no_stop))
        one_hot = {word: [1 if word == v else 0 for v in vocab] for word in vocab}
        encoded = "\n".join([f"{word}: {one_hot[word]}" for word in vocab[:5]])
        st.markdown(f"<div class='result-box'>{encoded}</div>", unsafe_allow_html=True)