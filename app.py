import streamlit as st
import random

st.title("✨Daily affirmations✨")

st.image("assets/thumbs_up.jpeg", width=250)

with open("data/affirmations.txt", r) as file:
    affirmations = file.readlines()

affirmations = [line.strip() for line in affirmations if line.strip()]

affirmation = random.choice(affirmations)

st.success(affirmation)
