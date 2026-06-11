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
        "api_key_help_title": "How to add an API key",
        "api_key_steps": [
            "Choose BYOT online assistant.",
            "Create or copy an API key from your AI provider account.",
            "Paste the key into the password field. It is used only for this request and is not saved.",
            "Keep the default API URL for OpenAI-compatible providers, or paste your provider's chat completions endpoint.",
            "Set the model name that your provider supports, then generate your affirmation.",
        ],
        "api_url_label": "API URL",
        "online_model_label": "Online model",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama model",
        "ollama_help_text": "New to Ollama?",
        "ollama_setup_title": "Quick Ollama setup",
        "ollama_setup_steps": [
            "Install Ollama from `https://ollama.com/`.",
            "Pull a model in your terminal: `ollama pull llama3.2`.",
            "Start Ollama by opening the app or running `ollama serve`.",
            "Use `http://localhost:11434` in this app unless you configured a different host.",
            "Set the model to `llama3.2`, write your reflection, and generate.",
        ],
        "ollama_url_help_title": "If localhost does not match your Ollama URL",
        "ollama_url_steps": [
            "Check the configured host in a terminal: `echo $OLLAMA_HOST` on macOS/Linux or `$env:OLLAMA_HOST` in Windows PowerShell.",
            "If Ollama shows a custom host, paste it here as a full URL, for example `http://192.168.1.20:11434`.",
            "Test the URL with `/api/tags`, for example `curl http://localhost:11434/api/tags`.",
            "Pull the model on that same configured host: `OLLAMA_HOST=http://your-host:11434 ollama pull llama3.2`.",
            "Use the same URL and model name in this app.",
        ],
        "generate_button": "Create personal affirmation",
        "empty_reflection": "Please write a short reflection first.",
        "missing_key": "Please enter your API key for BYOT mode.",
        "assistant_error": "AI reflection is unavailable right now, but your daily affirmation is still here for you.",
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
        "api_key_help_title": "API कुंजी कैसे जोड़ें",
        "api_key_steps": [
            "BYOT ऑनलाइन सहायक चुनें।",
            "अपने AI सेवा खाते से API कुंजी बनाएं या कॉपी करें।",
            "कुंजी को पासवर्ड वाले बॉक्स में डालें। यह केवल इसी अनुरोध के लिए उपयोग होगी और सहेजी नहीं जाएगी।",
            "OpenAI-संगत सेवाओं के लिए डिफॉल्ट API URL रखें, या अपनी सेवा का chat completions endpoint डालें।",
            "अपनी सेवा द्वारा समर्थित मॉडल नाम लिखें, फिर अपना सकारात्मक वाक्य बनाएं।",
        ],
        "api_url_label": "API URL",
        "online_model_label": "ऑनलाइन मॉडल",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama मॉडल",
        "ollama_help_text": "Ollama पहली बार इस्तेमाल कर रहे हैं?",
        "ollama_setup_title": "त्वरित Ollama सेटअप",
        "ollama_setup_steps": [
            "`https://ollama.com/` से Ollama इंस्टॉल करें।",
            "टर्मिनल में मॉडल खींचें: `ollama pull llama3.2`।",
            "Ollama ऐप खोलें या `ollama serve` चलाकर Ollama शुरू करें।",
            "अगर आपने अलग होस्ट कॉन्फिगर नहीं किया है, तो इस ऐप में `http://localhost:11434` इस्तेमाल करें।",
            "मॉडल में `llama3.2` लिखें, अपना विचार लिखें, और सकारात्मक वाक्य बनाएं।",
        ],
        "ollama_url_help_title": "अगर localhost आपके Ollama URL से match नहीं करता",
        "ollama_url_steps": [
            "टर्मिनल में कॉन्फिगर किया गया होस्ट देखें: macOS/Linux पर `echo $OLLAMA_HOST` या Windows PowerShell में `$env:OLLAMA_HOST`।",
            "अगर Ollama अलग होस्ट दिखाता है, तो पूरा URL यहां डालें, जैसे `http://192.168.1.20:11434`।",
            "URL को `/api/tags` से जांचें, जैसे `curl http://localhost:11434/api/tags`।",
            "मॉडल उसी कॉन्फिगर किए गए होस्ट पर खींचें: `OLLAMA_HOST=http://your-host:11434 ollama pull llama3.2`।",
            "इस ऐप में वही URL और मॉडल नाम इस्तेमाल करें।",
        ],
        "generate_button": "व्यक्तिगत सकारात्मक वाक्य बनाएं",
        "empty_reflection": "कृपया पहले एक छोटा विचार लिखें।",
        "missing_key": "कृपया BYOT मोड के लिए अपनी API कुंजी डालें।",
        "assistant_error": "AI मनन अभी उपलब्ध नहीं है, लेकिन आपका दैनिक सकारात्मक वाक्य अभी भी आपके साथ है।",
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
        "api_key_help_title": "API కీని ఎలా జోడించాలి",
        "api_key_steps": [
            "BYOT ఆన్లైన్ సహాయకుడిని ఎంచుకోండి.",
            "మీ AI సేవ ఖాతా నుండి API కీని సృష్టించండి లేదా కాపీ చేయండి.",
            "ఆ కీని పాస్‌వర్డ్ పెట్టెలో అతికించండి. ఇది ఈ అభ్యర్థనకే వాడబడుతుంది, భద్రపరచబడదు.",
            "OpenAI-సరిపోలే సేవలకు డిఫాల్ట్ API URL ఉంచండి, లేదా మీ సేవ యొక్క chat completions endpoint ఇవ్వండి.",
            "మీ సేవలో అందుబాటులో ఉన్న మోడల్ పేరును రాయండి, తర్వాత మీ ధైర్య వాక్యాన్ని తయారు చేయండి.",
        ],
        "api_url_label": "API URL",
        "online_model_label": "ఆన్లైన్ మోడల్",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama మోడల్",
        "ollama_help_text": "Ollama కొత్తగా వాడుతున్నారా?",
        "ollama_setup_title": "త్వరిత Ollama సెటప్",
        "ollama_setup_steps": [
            "`https://ollama.com/` నుండి Ollama ఇన్‌స్టాల్ చేయండి.",
            "టెర్మినల్‌లో మోడల్‌ను పొందండి: `ollama pull llama3.2`.",
            "Ollama యాప్ తెరవండి లేదా `ollama serve` నడిపి Ollama ప్రారంభించండి.",
            "మీరు వేరే హోస్ట్ అమర్చకపోతే, ఈ యాప్‌లో `http://localhost:11434` వాడండి.",
            "మోడల్‌గా `llama3.2` ఇవ్వండి, మీ ఆలోచన రాయండి, తర్వాత ధైర్య వాక్యాన్ని తయారు చేయండి.",
        ],
        "ollama_url_help_title": "localhost మీ Ollama URL తో match కాకపోతే",
        "ollama_url_steps": [
            "టెర్మినల్‌లో అమర్చిన హోస్ట్‌ను చూడండి: macOS/Linux లో `echo $OLLAMA_HOST`, Windows PowerShell లో `$env:OLLAMA_HOST`.",
            "Ollama వేరే హోస్ట్ చూపిస్తే, పూర్తి URL ను ఇక్కడ ఇవ్వండి, ఉదాహరణకు `http://192.168.1.20:11434`.",
            "URL ను `/api/tags` తో పరీక్షించండి, ఉదాహరణకు `curl http://localhost:11434/api/tags`.",
            "మోడల్‌ను అదే అమర్చిన హోస్ట్‌పై పొందండి: `OLLAMA_HOST=http://your-host:11434 ollama pull llama3.2`.",
            "ఈ యాప్‌లో అదే URL మరియు మోడల్ పేరును వాడండి.",
        ],
        "generate_button": "వ్యక్తిగత ధైర్య వాక్యం తయారు చేయండి",
        "empty_reflection": "దయచేసి ముందుగా ఒక చిన్న ఆలోచన రాయండి.",
        "missing_key": "దయచేసి BYOT మోడ్ కోసం మీ API కీ ఇవ్వండి.",
        "assistant_error": "AI ఆలోచన సహాయం ప్రస్తుతం అందుబాటులో లేదు, కానీ మీ రోజువారీ ధైర్య వాక్యం మీకోసం ఉంది.",
    },
}


def show_help_popup(title, steps):
    if hasattr(st, "popover"):
        popup = st.popover(title)
    else:
        popup = st.expander(title)

    with popup:
        for step in steps:
            st.markdown(f"- {step}")


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
        f"Prefer the selected app language: {selected_language_name} "
        f"({selected_language_code}). "
        "Only switch to the user's typed language if the user is clearly writing "
        "in a different supported language. "
        "Keep the response to one or two short sentences. "
        "Do not give medical, legal, political, or religious advice. "
        "Do not diagnose the user. "
        "If the reflection sounds serious or unsafe, respond gently and suggest "
        "reaching out to a trusted person or local support. "
        "Keep it warm, practical, and safe.\n\n"
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


def request_ollama_affirmation(ollama_base_url, model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 120,
        },
    }

    ollama_url = ollama_base_url.rstrip("/") + "/api/generate"

    request = Request(
        ollama_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    response_text = data.get("response", "").strip()

    if not response_text:
        raise ValueError("Ollama returned an empty response")

    return response_text


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
    show_help_popup(language["api_key_help_title"], language["api_key_steps"])
else:
    ollama_url = st.text_input(
        language["ollama_url_label"],
        value="http://localhost:11434",
    )
    ollama_model = st.text_input(language["ollama_model_label"], value="llama3.2")
    show_help_popup(language["ollama_url_help_title"], language["ollama_url_steps"])
    show_help_popup(language["ollama_setup_title"], language["ollama_setup_steps"])

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
        except (
            HTTPError,
            URLError,
            TimeoutError,
            KeyError,
            ValueError,
            json.JSONDecodeError,
        ):
            st.error(language["assistant_error"])
