import random
from html import escape
from pathlib import Path

import streamlit as st


LANGUAGES = {
    "English": {
        "code": "en",
        "title": "Daily Affirmations ✨",
        "subtitle": "A small reminder that you are doing okay.",
        "selector": "Choose your language",
        "image_warning": "Image not found. Please check assets/thumbs_up.jpeg",
        "missing_data": "Affirmations are not available for this language yet.",
        "empty_data": "No affirmations found for this language yet.",
    },
    "हिन्दी": {
        "code": "hi",
        "title": "दैनिक सकारात्मक वाक्य ✨",
        "subtitle": "एक छोटा सा स्मरण कि आप ठीक कर रहे हैं।",
        "selector": "अपनी भाषा चुनें",
        "image_warning": "चित्र नहीं मिला। कृपया assets/thumbs_up.jpeg जांचें।",
        "missing_data": "इस भाषा के लिए सकारात्मक वाक्य अभी उपलब्ध नहीं हैं।",
        "empty_data": "इस भाषा के लिए अभी कोई सकारात्मक वाक्य नहीं मिला।",
    },
    "తెలుగు": {
        "code": "te",
        "title": "రోజువారీ ధైర్య వాక్యాలు ✨",
        "subtitle": "మీరు బాగానే ముందుకు సాగుతున్నారని ఒక చిన్న గుర్తు.",
        "selector": "మీ భాషను ఎంచుకోండి",
        "image_warning": "చిత్రం దొరకలేదు. దయచేసి assets/thumbs_up.jpeg చూడండి.",
        "missing_data": "ఈ భాషకు ధైర్య వాక్యాలు ఇంకా అందుబాటులో లేవు.",
        "empty_data": "ఈ భాషకు ఇంకా ధైర్య వాక్యాలు లేవు.",
    },
}


def load_affirmations(language_code):
    affirmations_path = Path(f"data/affirmations_{language_code}.txt")

    if not affirmations_path.exists():
        return None

    with open(affirmations_path, "r", encoding="utf-8") as file:
        affirmations = file.readlines()

    cleaned_affirmations = []

    for line in affirmations:
        cleaned_line = line.strip()

        if cleaned_line:
            cleaned_affirmations.append(cleaned_line)

    return cleaned_affirmations


st.set_page_config(
    page_title="Daily Affirmations",
    page_icon="✨",
    layout="centered"
)

language_name = st.selectbox(
    "Language / भाषा / భాష",
    list(LANGUAGES.keys())
)

language = LANGUAGES[language_name]

st.markdown(
    f"<h1 style='text-align: center;'>{language['title']}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align: center; font-size: 18px;'>{language['subtitle']}</p>",
    unsafe_allow_html=True
)

image_path = Path("assets/thumbs_up.jpeg")

if image_path.exists():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(str(image_path), use_container_width=True)
else:
    st.warning(language["image_warning"])

affirmations = load_affirmations(language["code"])

if affirmations is None:
    st.warning(language["missing_data"])
elif not affirmations:
    st.warning(language["empty_data"])
else:
    affirmation = random.choice(affirmations)

    st.markdown(
        f"""
        <div style="
            text-align: center;
            color: #222222;
            font-size: 28px;
            padding: 30px;
            margin-top: 25px;
            border-radius: 20px;
            background-color: #f5f5f5;
            line-height: 1.4;
        ">
            {escape(affirmation)}
        </div>
        """,
        unsafe_allow_html=True
    )
