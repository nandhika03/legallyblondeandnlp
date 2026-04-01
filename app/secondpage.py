# secondpage.py

import streamlit as st
import re
from collections import Counter
import base64
import nltk

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize tools
wordlem = WordNetLemmatizer()
ps = PorterStemmer()


def run_bow():
    # ------------------ Background Image ------------------
    def get_img_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    image_64 = get_img_base64(
        "C://Users//Nandhika//Desktop//LegallyBlonde//data//bg_lb.jpg"
    )

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

    # ------------------ Title ------------------
    st.markdown(
        "<h1 style='color: hotpink; text-align: center;'>A deeper shade of pre-processing</h1>",
        unsafe_allow_html=True
    )

    # ------------------ Text Input ------------------
    paragraph = st.text_area(
        "Enter Paragraph:",
        """A Delta Gamma/Sigma Chi barbecue in full swing. Beautiful college students drink beer and mingle,
trying to figure out who they're going to sleep with next. The main wall of the living room has been 
designated as a "Model Wall" of Delta Gamma girls -- ELLE smiles at us from a Hawaiian Tropic ad and
a Miss June USC calendar photo. A cover of an Italian Vogue shows a blonde sexpot MARGOT; a USC 
cheerleader poster displays a hard-bodied non-blonde SERENA in a pom-pom pose.
Serena walks up, fending off an admirer.""",
        label_visibility="collapsed"
    )

    # ------------------ Slider ------------------
    top_n = st.slider("Number of words to display", 5, 50, 10)

    # ------------------ Preprocessing Function ------------------
    def preprocess_text(text):
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = set(stopwords.words('english'))
        processed = []
        for word in words:
            if word not in stop_words:
                word = wordlem.lemmatize(word)
                word = ps.stem(word)
                processed.append(word)
        return processed

    processed_words = preprocess_text(paragraph)

    # ------------------ Buttons ------------------
    col1, col2 = st.columns(2)
    with col1:
        bow_btn = st.button("BOW")
    with col2:
        tfidf_btn = st.button("TF-IDF")

    # ------------------ BOW ------------------
    if bow_btn:
        bow = Counter(processed_words)
        bow_display = "\n".join(
            [f"{word}: {count}" for word, count in bow.most_common(top_n)]
        )
        st.markdown(
            f"<div class='result-box'>{bow_display}</div>",
            unsafe_allow_html=True
        )

    # ------------------ TF-IDF per sentence ------------------
    if tfidf_btn:
        # Split paragraph into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]', paragraph) if s.strip()]
        # Preprocess each sentence individually
        processed_sentences = [" ".join(preprocess_text(s)) for s in sentences]

        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(processed_sentences)
        features = vectorizer.get_feature_names_out()

        st.subheader("TF-IDF Scores per Sentence")
        for i, sent_vec in enumerate(X.toarray()):
            top_words = sorted(
                zip(features, sent_vec), key=lambda x: x[1], reverse=True
            )[:top_n]
            sent_display = "\n".join(
                f"{word}: {round(score,4)}" for word, score in top_words if score > 0
            )
            st.markdown(f"<div class='result-box'><b>Sentence {i+1}:</b>\n{sent_display}</div>",
                        unsafe_allow_html=True)