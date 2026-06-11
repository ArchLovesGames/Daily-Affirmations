import random
import json
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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
        "reflection_heading": "Reflect with AI",
        "reflection_intro": "Write a short thought, then receive a personal affirmation.",
        "reflection_label": "How are you feeling today?",
        "reflection_placeholder": "I feel nervous about my project demo.",
        "assistant_mode": "Assistant mode",
        "byot_mode": "BYOT online assistant",
        "ollama_mode": "Local Ollama assistant",
        "api_key_label": "API key",
        "api_key_help": "Your key is used only for this request.",
        "api_url_label": "API URL",
        "online_model_label": "Online model",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama model",
        "generate_button": "Create personal affirmation",
        "empty_reflection": "Please write a short reflection first.",
        "missing_key": "Please enter your API key for BYOT mode.",
        "assistant_error": "The assistant could not respond yet. Please check the settings and try again.",
    },
    "हिन्दी": {
        "code": "hi",
        "title": "दैनिक सकारात्मक वाक्य ✨",
        "subtitle": "एक छोटा सा स्मरण कि आप ठीक कर रहे हैं।",
        "selector": "अपनी भाषा चुनें",
        "image_warning": "चित्र नहीं मिला। कृपया assets/thumbs_up.jpeg जांचें।",
        "missing_data": "इस भाषा के लिए सकारात्मक वाक्य अभी उपलब्ध नहीं हैं।",
        "empty_data": "इस भाषा के लिए अभी कोई सकारात्मक वाक्य नहीं मिला।",
        "reflection_heading": "AI के साथ मन की बात",
        "reflection_intro": "एक छोटा विचार लिखें और अपने लिए एक सकारात्मक वाक्य पाएं।",
        "reflection_label": "आज आप कैसा महसूस कर रहे हैं?",
        "reflection_placeholder": "मुझे अपने प्रोजेक्ट डेमो को लेकर घबराहट हो रही है।",
        "assistant_mode": "सहायक मोड",
        "byot_mode": "BYOT ऑनलाइन सहायक",
        "ollama_mode": "स्थानीय Ollama सहायक",
        "api_key_label": "API कुंजी",
        "api_key_help": "आपकी कुंजी केवल इस अनुरोध के लिए उपयोग होगी।",
        "api_url_label": "API URL",
        "online_model_label": "ऑनलाइन मॉडल",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama मॉडल",
        "generate_button": "व्यक्तिगत सकारात्मक वाक्य बनाएं",
        "empty_reflection": "कृपया पहले एक छोटा विचार लिखें।",
        "missing_key": "कृपया BYOT मोड के लिए अपनी API कुंजी डालें।",
        "assistant_error": "सहायक अभी उत्तर नहीं दे पाया। कृपया सेटिंग जांचकर फिर कोशिश करें।",
    },
    "తెలుగు": {
        "code": "te",
        "title": "రోజువారీ ధైర్య వాక్యాలు ✨",
        "subtitle": "మీరు బాగానే ముందుకు సాగుతున్నారని ఒక చిన్న గుర్తు.",
        "selector": "మీ భాషను ఎంచుకోండి",
        "image_warning": "చిత్రం దొరకలేదు. దయచేసి assets/thumbs_up.jpeg చూడండి.",
        "missing_data": "ఈ భాషకు ధైర్య వాక్యాలు ఇంకా అందుబాటులో లేవు.",
        "empty_data": "ఈ భాషకు ఇంకా ధైర్య వాక్యాలు లేవు.",
        "reflection_heading": "AI తో ఆలోచన పంచుకోండి",
        "reflection_intro": "ఒక చిన్న ఆలోచన రాసి, మీకోసం ఒక వ్యక్తిగత ధైర్య వాక్యం పొందండి.",
        "reflection_label": "ఈ రోజు మీకు ఎలా అనిపిస్తోంది?",
        "reflection_placeholder": "నా ప్రాజెక్ట్ డెమో గురించి నాకు కొంచెం ఆందోళనగా ఉంది.",
        "assistant_mode": "సహాయక మోడ్",
        "byot_mode": "BYOT ఆన్లైన్ సహాయకుడు",
        "ollama_mode": "లోకల్ Ollama సహాయకుడు",
        "api_key_label": "API కీ",
        "api_key_help": "మీ కీ ఈ అభ్యర్థనకే ఉపయోగించబడుతుంది.",
        "api_url_label": "API URL",
        "online_model_label": "ఆన్లైన్ మోడల్",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama మోడల్",
        "generate_button": "వ్యక్తిగత ధైర్య వాక్యం తయారు చేయండి",
        "empty_reflection": "దయచేసి ముందుగా ఒక చిన్న ఆలోచన రాయండి.",
        "missing_key": "దయచేసి BYOT మోడ్ కోసం మీ API కీ ఇవ్వండి.",
        "assistant_error": "సహాయకుడు ఇప్పుడే స్పందించలేకపోయాడు. సెట్టింగ్స్ చూసి మళ్లీ ప్రయత్నించండి.",
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


def build_reflection_prompt(reflection, selected_language_name, selected_language_code):
    return (
        "You are a gentle daily reflection assistant for a Daily Affirmations app. "
        "Read the user's short reflection and write one brief, personal affirmation. "
        "Use the same language as the user's reflection when it is clear. "
        f"If the reflection language is unclear, use the selected app language: "
        f"{selected_language_name} ({selected_language_code}). "
        "Keep the response to one or two short sentences. "
        "Do not give medical, legal, political, or religious advice. "
        "Do not diagnose the user. Keep it warm, practical, and safe.\n\n"
        f"User reflection: {reflection}"
    )


def request_online_affirmation(api_url, api_key, model, prompt):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You write short, safe, personalized affirmations.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 120,
    }

    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"].strip()


def request_ollama_affirmation(ollama_url, model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 120,
        },
    }

    request = Request(
        ollama_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data.get("response", "").strip()


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

st.markdown("---")

st.markdown(
    f"<h2 style='text-align: center;'>{language['reflection_heading']}</h2>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align: center; font-size: 16px;'>{language['reflection_intro']}</p>",
    unsafe_allow_html=True
)

reflection = st.text_area(
    language["reflection_label"],
    placeholder=language["reflection_placeholder"],
    height=110,
)

assistant_mode = st.radio(
    language["assistant_mode"],
    [language["byot_mode"], language["ollama_mode"]],
    horizontal=True,
)

if assistant_mode == language["byot_mode"]:
    api_key = st.text_input(
        language["api_key_label"],
        type="password",
        help=language["api_key_help"],
    )
    api_url = st.text_input(
        language["api_url_label"],
        value="https://api.openai.com/v1/chat/completions",
    )
    model = st.text_input(language["online_model_label"], value="gpt-4o-mini")
else:
    ollama_url = st.text_input(
        language["ollama_url_label"],
        value="http://localhost:11434/api/generate",
    )
    ollama_model = st.text_input(language["ollama_model_label"], value="llama3.2")

if st.button(language["generate_button"]):
    reflection_text = reflection.strip()

    if not reflection_text:
        st.warning(language["empty_reflection"])
    elif assistant_mode == language["byot_mode"] and not api_key.strip():
        st.warning(language["missing_key"])
    else:
        prompt = build_reflection_prompt(
            reflection_text,
            language_name,
            language["code"],
        )

        try:
            with st.spinner(language["reflection_heading"]):
                if assistant_mode == language["byot_mode"]:
                    personal_affirmation = request_online_affirmation(
                        api_url.strip(),
                        api_key.strip(),
                        model.strip(),
                        prompt,
                    )
                else:
                    personal_affirmation = request_ollama_affirmation(
                        ollama_url.strip(),
                        ollama_model.strip(),
                        prompt,
                    )

            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    color: #222222;
                    font-size: 22px;
                    padding: 24px;
                    margin-top: 18px;
                    border-radius: 16px;
                    background-color: #eef7f1;
                    line-height: 1.5;
                ">
                    {escape(personal_affirmation)}
                </div>
                """,
                unsafe_allow_html=True,
            )
        except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError):
            st.error(language["assistant_error"])
