import random
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Daily Affirmations",
    page_icon="✨",
    layout="centered"
)

st.markdown(
    "<h1 style='text-align: center;'>Daily Affirmations ✨</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size: 18px;'>A small reminder that you are doing okay.</p>",
    unsafe_allow_html=True
)

image_path = Path("assets/thumbs_up.jpeg")

if image_path.exists():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(str(image_path), use_container_width=True)
else:
    st.warning("Image not found. Please check assets/thumbs_up.jpg")

affirmations_path = Path("data/affirmations.txt")

with open(affirmations_path, "r") as file:
    affirmations = file.readlines()

cleaned_affirmations = []

for line in affirmations:
    cleaned_line = line.strip()

    if cleaned_line:
        cleaned_affirmations.append(cleaned_line)

affirmation = random.choice(cleaned_affirmations)

st.markdown(
    f"""
    <div style="
        text-align: center;
        font-size: 28px;
        padding: 30px;
        margin-top: 25px;
        border-radius: 20px;
        background-color: #f5f5f5;
        line-height: 1.4;
    ">
        {affirmation}
    </div>
    """,
    unsafe_allow_html=True
)