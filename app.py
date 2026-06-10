import streamlit as st
import random

st.title("<h1 style='text-align: center;'>Daily Affirmations ✨</h1>", unsafe_allow_html=True)

image_path = Path("assets/thumbs_up.jpg")

if image_path.exists():
    st.image(str(image_path), width=750, height=400)
else:
    st.warning("Image not found.")

with open("data/affirmations.txt", "r") as file:
    affirmations = file.readlines()

affirmations = [line.strip() for line in affirmations if line.strip()]

affirmation = random.choice(affirmations)

st.success(affirmation)

st.markdown(
    f"""
    <div style="
        text-align: center;
        font-size: 28px;
        padding: 30px;
        margin-top: 20px;
        border-radius: 20px;
        background-color: #f5f5f5;
    ">
        {affirmation}
    </div>
    """,
    unsafe_allow_html=True
)