import random
import json
import os
import re
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
            "Sarvam Chat Completion is also supported as an online provider. Use API URL `https://api.sarvam.ai/v1/chat/completions` and model `sarvam-30b`.",
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
        "cloudflare_help_title": "Using local Ollama with the web app",
        "cloudflare_steps": [
            "To connect Ollama running on your computer to this web app, start Ollama: `ollama serve`.",
            "Open a second terminal and install Cloudflare Tunnel if needed: `brew install cloudflared`.",
            "Run: `cloudflared tunnel --url http://localhost:11434 --http-host-header=\"localhost:11434\"`.",
            "Copy the generated URL ending in `.trycloudflare.com`.",
            "Paste that full URL into the Ollama URL field and keep the terminal open.",
            "This URL is temporary and changes whenever the tunnel restarts. Use it only for testing or demos. Do not share the URL publicly.",
        ],
        "generate_button": "Create personal affirmation",
        "empty_reflection": "Please write a short reflection first.",
        "missing_key": "Please enter your API key for BYOT mode.",
        "missing_sarvam_key": "Please enter your Sarvam API key for Sarvam Chat Completion.",
        "translation_caption": "Local-language reflections use Sarvam AI translation when enhanced translation is configured.",
        "ollama_translation_caption": "Ollama generates the affirmation locally. Hindi and Telugu translation use the online Sarvam API when enabled; English mode remains fully local.",
        "sarvam_key_label": "Sarvam API key",
        "sarvam_key_help": "Optional for Hindi or Telugu translation. Required when the BYOT API URL is Sarvam Chat Completion.",
        "sarvam_key_warning": "Enhanced local-language translation is unavailable because SARVAM_API_KEY is not configured. Falling back to direct AI generation.",
        "sarvam_failure_warning": "Enhanced translation is unavailable right now. Showing the AI response without translation.",
        "assistant_error": "AI reflection is unavailable right now, but your daily affirmation is still here for you.",
    },
    "हिन्दी": {
        "code": "hi",
        "title": "रोज़ाना Affirmations ✨",
        "subtitle": "एक छोटी सी याद दिलाना कि आप ठीक कर रहे हैं।",
        "selector": "अपनी भाषा चुनिए",
        "image_warning": "Image नहीं मिली। ज़रा assets/thumbs_up.jpeg देख लीजिए",
        "missing_data": "इस language के लिए अभी Affirmations नहीं हैं।",
        "empty_data": "अभी तक इस language के लिए कोई affirmations नहीं मिले हैं।",
        "reflection_heading": "AI के साथ सोचिए",
        "reflection_intro": "एक छोटा सा विचार लिखिए, फिर आपको एक personal affirmation मिलेगा।",
        "reflection_label": "आज आप कैसा महसूस कर रहे हैं?",
        "reflection_placeholder": "मुझे अपने project demo को लेकर घबराहट हो रही है।",
        "assistant_mode": "Assistant mode",
        "byot_mode": "BYOT online assistant",
        "ollama_mode": "Local Ollama assistant",
        "api_key_label": "API key",
        "api_key_help": "आपकी key सिर्फ़ इसी request के लिए इस्तेमाल होगी।",
        "api_key_help_title": "API key कैसे लगाएँ",
        "api_key_steps": [
            "BYOT online assistant चुनिए।",
            "अपने AI provider account से API key बनाइए या copy कीजिए।",
            "Password field में key डाल दीजिए। यह सिर्फ़ इसी request के लिए है और save नहीं किया जाएगा।",
            "OpenAI-compatible providers के लिए default API URL रखें, या अपने provider का chat completions endpoint paste कर दीजिए।",
            "Sarvam Chat Completion online भी support करता है। API URL `https://api.sarvam.ai/v1/chat/completions` और model `sarvam-30b` इस्तेमाल कीजिए।",
            "अपने provider के support वाले model का नाम set कीजिए, फिर अपना affirmation generate कीजिए।",
        ],
        "api_url_label": "API URL",
        "online_model_label": "Online model",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama model",
        "ollama_help_text": "क्या आप Ollama में नए हैं?",
        "ollama_setup_title": "Quick Ollama setup कीजिए",
        "ollama_setup_steps": [
            "`https://ollama.com/` से Ollama install कीजिए।",
            "अपने terminal में model `ollama pull llama3.2` निकाल लीजिए।",
            "आप app खोलकर या `ollama serve` run करके Ollama शुरू कर सकते हैं।",
            "इस app में `http://localhost:11434` इस्तेमाल कीजिए, जब तक कि आपने कोई दूसरा host ना set किया हो।",
            "model को `llama3.2` पर set कीजिए, अपना reflection लिखिए, और generate कीजिए।",
        ],
        "ollama_url_help_title": "अगर localhost आपके Ollama URL से match नहीं करता है",
        "ollama_url_steps": [
            "किसी terminal में configured host check कीजिए: `echo $OLLAMA_HOST` on macOS/Linux या `$env:OLLAMA_HOST` in Windows PowerShell.",
            "अगर Ollama कोई custom host दिखाता है, तो उसे यहाँ पूरी तरह से URL की तरह, जैसे `http://192.168.1.20:11434`, paste कर दीजिए।",
            "ज़रा URL को `/api/tags` के साथ test कीजिए, जैसे कि `curl http://localhost:11434/api/tags`.",
            "उसी configured host: `OLLAMA_HOST=http://your-host:11434 ollama pull llama3.2` पर model को खींच लीजिए।",
            "इस app में वही URL और model name इस्तेमाल कीजिए।",
        ],
        "cloudflare_help_title": "web app के साथ local Ollama इस्तेमाल कर रहे हैं",
        "cloudflare_steps": [
            "अपने computer पर चलने वाले Ollama को इस web app से connect करने के लिए, Ollama: `ollama serve` से शुरू कीजिए।",
            "दूसरा terminal खोलिए और ज़रूरत पड़ने पर Cloudflare Tunnel install कर लीजिए: `brew install cloudflared`.",
            "चलाएँ: `cloudflared tunnel --url http://localhost:11434 --http-host-header=\"localhost:11434\"`.",
            "`.trycloudflare.com` में ख़त्म होने वाला URL copy कर लीजिए।",
            "उस full URL को Ollama URL field में paste कर दीजिए और terminal खुला रखिए।",
            "यह URL temporary है और tunnel restart होने पर बदल जाएगा। इसे सिर्फ़ testing या demo के लिए इस्तेमाल कीजिए। URL को public में share मत कीजिए।",
        ],
        "generate_button": "अपने लिए एक affirmation बनाइए",
        "empty_reflection": "पहले एक छोटा सा reflection लिखिए।",
        "missing_key": "ज़रा BYOT mode के लिए अपनी API key डालिए।",
        "missing_sarvam_key": "Sarvam Chat Completion के लिए अपनी Sarvam API key डालिए।",
        "translation_caption": "जब enhanced translation चालू होता है, तो Local-language reflections में Sarvam AI translation इस्तेमाल होता है।",
        "ollama_translation_caption": "Ollama locally affirmation generate करता है। जब online Sarvam API चालू होता है, तो Hindi और Telugu translation के लिए इसका इस्तेमाल होता है; English mode पूरी तरह से local ही रहता है।",
        "sarvam_key_label": "Sarvam API key",
        "sarvam_key_help": "Hindi या Telugu translation के लिए optional. BYOT API URL Sarvam Chat Completion हो तो यह required है।",
        "sarvam_key_warning": "SARVAM_API_KEY configure नहीं किया गया है, इसलिए enhanced local-language translation नहीं हो सकता। वापस direct AI generation पर आ रही हूँ।",
        "sarvam_failure_warning": "अभी Enhanced Translation नहीं चल रहा है। बिना translation के AI response दिखा रहा हूँ।",
        "assistant_error": "AI reflection अभी available नहीं है, लेकिन आपकी daily affirmation आपके लिए अभी भी मौजूद है।",
    },
    "తెలుగు": {
        "code": "te",
        "title": "రోజువారీ ధృవీకరణలు ✨",
        "subtitle": "మీరు బాగానే ఉన్నారని గుర్తు చేస్తున్నాను.",
        "selector": "మీ language ఎంచుకోండి",
        "image_warning": "Image దొరకలేదు. assets/thumbs_up.jpeg చూడండి",
        "missing_data": "ఈ language-కి ఇంకా affirmations లేవు.",
        "empty_data": "ఈ language-కి ఇంకా affirmations దొరకలేదు.",
        "reflection_heading": "AI-తో reflect చేయండి",
        "reflection_intro": "ఒక చిన్న ఆలోచనాత్మకమైన మాట రాయండి, తర్వాత మీకు ఒక personal affirmation వస్తుంది.",
        "reflection_label": "ఈరోజు మీరు ఎలా ఉన్నారు?",
        "reflection_placeholder": "నా project demo గురించి నాకు చాలా భయంగా ఉంది.",
        "assistant_mode": "Assistant mode",
        "byot_mode": "BYOT online assistant",
        "ollama_mode": "Local Ollama assistant",
        "api_key_label": "API key",
        "api_key_help": "ఈ request కోసం మాత్రమే మీ key వాడతారు.",
        "api_key_help_title": "API key ఎలా add చేయాలో చెప్పండి",
        "api_key_steps": [
            "BYOT online assistant-ని ఎంచుకోండి.",
            "మీ AI provider account నుండి API key-ని create చేయండి లేదా copy చేయండి.",
            "Password field-లో key paste చేయండి. ఇది ఈ request-కి మాత్రమే వాడతారు. save చేయరు.",
            "OpenAI-compatible providers కోసం default API URL-నే ఉంచండి లేదా మీ provider chat completions endpoint paste చేయండి.",
            "Sarvam Chat Completion online provider-గా కూడా support చేస్తుంది. API URL `https://api.sarvam.ai/v1/chat/completions` మరియు model `sarvam-30b` వాడండి.",
            "మీ provider support చేసే model name set చేసి, మీ affirmation generate చేయండి.",
        ],
        "api_url_label": "API URL",
        "online_model_label": "Online model",
        "ollama_url_label": "Ollama URL",
        "ollama_model_label": "Ollama model",
        "ollama_help_text": "Ollama-కి కొత్తరా?",
        "ollama_setup_title": "Quick Ollama setup చేసుకోండి",
        "ollama_setup_steps": [
            "`https://ollama.com/` నుంచి Ollama install చేయండి.",
            "మీ terminal-లో `ollama pull llama3.2` అనే model-ని pull చేయండి.",
            "Ollama app open చేయండి లేదా `ollama serve` run చేయండి.",
            "మీరు వేరే host configure చేయకపోతే ఈ app-లో `http://localhost:11434` వాడండి.",
            "`llama3.2`-కి model set చేసి, మీ reflection రాసి, generate చేయండి.",
        ],
        "ollama_url_help_title": "localhost మీ Ollama URL-తో match కాకపోతే",
        "ollama_url_steps": [
            "Configured host-ని terminal-లో check చేయండి: `echo $OLLAMA_HOST` on macOS/Linux లేదా Windows PowerShell-లో `$env:OLLAMA_HOST`.",
            "Ollama custom host చూపిస్తే, దాన్ని ఇక్కడ full URL లాగా paste చేయండి. ఉదాహరణకి `http://192.168.1.20:11434`.",
            "ఉదాహరణకి `curl http://localhost:11434/api/tags` లాంటి `/api/tags`-తో URL test చేయండి.",
            "అదే configured host: `OLLAMA_HOST=http://your-host:11434 ollama pull llama3.2` పైన model-ని pull చేయండి.",
            "ఈ app-లో URL, model name అలాగే వాడండి.",
        ],
        "cloudflare_help_title": "web app-తో local Ollama-ని వాడటం",
        "cloudflare_steps": [
            "మీ computer-లో run అవుతున్న Ollama-ని ఈ web app-కి connect చేయడానికి, Ollama: `ollama serve` start చేయండి.",
            "అవసరమైతే రెండవ terminal open చేసి Cloudflare Tunnel install చేయండి: `brew install cloudflared`.",
            "Run: `cloudflared tunnel --url http://localhost:11434 --http-host-header=\"localhost:11434\"`.",
            "`.trycloudflare.com`-తో అంతమయ్యే URL-ని copy చేయండి.",
            "ఆ full URL-ని Ollama URL field-లో paste చేసి, terminal open-లో ఉంచండి.",
            "ఈ URL temporary-ది. Tunnel restart అయినప్పుడల్లా మారుతుంది. దీన్ని testing-కి, demos-కి మాత్రమే వాడండి. URL-ని public-గా share చేయకండి.",
        ],
        "generate_button": "మీ గురించి మీకు నచ్చినవి చెప్పుకోండి",
        "empty_reflection": "ముందుగా ఒక చిన్న reflection రాయండి.",
        "missing_key": "BYOT mode-కి మీ API key enter చేయండి.",
        "missing_sarvam_key": "Sarvam Chat Completion కోసం మీ Sarvam API key enter చేయండి.",
        "translation_caption": "Enhanced translation configure చేసినప్పుడు, Local-language reflections-లో Sarvam AI translation వాడతారు.",
        "ollama_translation_caption": "Ollama affirmation-ని local-గా generate చేస్తుంది. Hindi, Telugu translation-కి online Sarvam API enable చేస్తే వాడతారు. English mode మాత్రం పూర్తిగా local-లోనే ఉంటుంది.",
        "sarvam_key_label": "Sarvam API key",
        "sarvam_key_help": "Hindi లేదా Telugu translation కోసం optional. BYOT API URL Sarvam Chat Completion అయితే ఇది required.",
        "sarvam_key_warning": "SARVAM_API_KEY configure కాలేదు కాబట్టి enhanced local-language translation లేదు. direct AI generation-కి తిరిగి వెళ్తున్నాను.",
        "sarvam_failure_warning": "ఇప్పుడు Enhanced Translation లేదు. Translation లేకుండా AI response చూపిస్తున్నాను.",
        "assistant_error": "AI reflection ఇప్పుడు available లేదు. కానీ మీ daily affirmation మాత్రం ఇంకా ఉంది.",
    },
}


SARVAM_LANGUAGE_CODES = {
    "English": "en-IN",
    "हिन्दी": "hi-IN",
    "తెలుగు": "te-IN",
}

SARVAM_CHAT_API_URL = "https://api.sarvam.ai/v1/chat/completions"
DEFAULT_ONLINE_API_URL = "https://api.groq.com/openai/v1/chat/completions"


SCRIPT_FALLBACKS = {
    "हिन्दी": {
        "script": "Devanagari",
        "examples": "project -> प्रोजेक्ट, demo -> डेमो",
    },
    "తెలుగు": {
        "script": "Telugu",
        "examples": "project -> ప్రాజెక్ట్, demo -> డెమో",
    },
}

COMMON_TRANSLITERATIONS = {
    "हिन्दी": {
        "ai": "एआई",
        "api": "एपीआई",
        "byot": "बीवाईओटी",
        "demo": "डेमो",
        "email": "ईमेल",
        "local": "लोकल",
        "model": "मॉडल",
        "ollama": "ओलामा",
        "online": "ऑनलाइन",
        "project": "प्रोजेक्ट",
        "token": "टोकन",
        "tokens": "टोकन",
        "work": "वर्क",
    },
    "తెలుగు": {
        "ai": "ఏఐ",
        "api": "ఏపీఐ",
        "byot": "బీవైఓటీ",
        "demo": "డెమో",
        "email": "ఈమెయిల్",
        "local": "లోకల్",
        "model": "మోడల్",
        "ollama": "ఒల్లామా",
        "online": "ఆన్‌లైన్",
        "project": "ప్రాజెక్ట్",
        "token": "టోకెన్",
        "tokens": "టోకెన్లు",
        "work": "వర్క్",
    },
}

LETTER_TRANSLITERATIONS = {
    "हिन्दी": {
        "a": "ए",
        "b": "बी",
        "c": "सी",
        "d": "डी",
        "e": "ई",
        "f": "एफ",
        "g": "जी",
        "h": "एच",
        "i": "आई",
        "j": "जे",
        "k": "के",
        "l": "एल",
        "m": "एम",
        "n": "एन",
        "o": "ओ",
        "p": "पी",
        "q": "क्यू",
        "r": "आर",
        "s": "एस",
        "t": "टी",
        "u": "यू",
        "v": "वी",
        "w": "डब्ल्यू",
        "x": "एक्स",
        "y": "वाई",
        "z": "ज़ेड",
    },
    "తెలుగు": {
        "a": "ఏ",
        "b": "బీ",
        "c": "సీ",
        "d": "డీ",
        "e": "ఈ",
        "f": "ఎఫ్",
        "g": "జీ",
        "h": "హెచ్",
        "i": "ఐ",
        "j": "జే",
        "k": "కే",
        "l": "ఎల్",
        "m": "ఎమ్",
        "n": "ఎన్",
        "o": "ఓ",
        "p": "పీ",
        "q": "క్యూ",
        "r": "ఆర్",
        "s": "ఎస్",
        "t": "టీ",
        "u": "యూ",
        "v": "వీ",
        "w": "డబ్ల్యూ",
        "x": "ఎక్స్",
        "y": "వై",
        "z": "జెడ్",
    },
}

PHONETIC_TRANSLITERATIONS = {
    "हिन्दी": {
        "vowels": {
            "a": ("अ", ""),
            "e": ("ए", "े"),
            "i": ("इ", "ि"),
            "o": ("ओ", "ो"),
            "u": ("उ", "ु"),
        },
        "vowel_groups": {
            "aa": ("आ", "ा"),
            "ai": ("ऐ", "ै"),
            "au": ("औ", "ौ"),
            "ee": ("ई", "ी"),
            "oo": ("ऊ", "ू"),
            "ou": ("आउ", "ाउ"),
        },
        "consonants": {
            "bh": "भ",
            "ch": "च",
            "dh": "ध",
            "gh": "घ",
            "kh": "ख",
            "ph": "फ",
            "sh": "श",
            "th": "थ",
            "wh": "व",
            "b": "ब",
            "c": "क",
            "d": "ड",
            "f": "फ",
            "g": "ग",
            "h": "ह",
            "j": "ज",
            "k": "क",
            "l": "ल",
            "m": "म",
            "n": "न",
            "p": "प",
            "q": "क",
            "r": "र",
            "s": "स",
            "t": "ट",
            "v": "व",
            "w": "व",
            "x": "क्स",
            "y": "य",
            "z": "ज़",
        },
        "virama": "्",
    },
    "తెలుగు": {
        "vowels": {
            "a": ("అ", ""),
            "e": ("ఎ", "ె"),
            "i": ("ఇ", "ి"),
            "o": ("ఒ", "ొ"),
            "u": ("ఉ", "ు"),
        },
        "vowel_groups": {
            "aa": ("ఆ", "ా"),
            "ai": ("ఐ", "ై"),
            "au": ("ఔ", "ౌ"),
            "ee": ("ఈ", "ీ"),
            "oo": ("ఊ", "ూ"),
            "ou": ("ఔ", "ౌ"),
        },
        "consonants": {
            "bh": "భ",
            "ch": "చ",
            "dh": "ధ",
            "gh": "ఘ",
            "kh": "ఖ",
            "ph": "ఫ",
            "sh": "ష",
            "th": "థ",
            "wh": "వ",
            "b": "బ",
            "c": "క",
            "d": "డ",
            "f": "ఫ",
            "g": "గ",
            "h": "హ",
            "j": "జ",
            "k": "క",
            "l": "ల",
            "m": "మ",
            "n": "న",
            "p": "ప",
            "q": "క",
            "r": "ర",
            "s": "స",
            "t": "ట",
            "v": "వ",
            "w": "వ",
            "x": "క్స్",
            "y": "య",
            "z": "జ",
        },
        "virama": "్",
    },
}


def transliterate_latin_word(word, language_name):
    lower_word = word.lower()
    common_words = COMMON_TRANSLITERATIONS.get(language_name, {})

    if lower_word in common_words:
        return common_words[lower_word]

    if word.isupper() and len(word) <= 4:
        return transliterate_latin_letters(word, language_name)

    return transliterate_latin_phonetically(lower_word, language_name)


def transliterate_latin_letters(word, language_name):
    letters = LETTER_TRANSLITERATIONS.get(language_name, {})

    if not letters:
        return word

    return "".join(letters.get(character.lower(), character) for character in word)


def transliterate_latin_phonetically(word, language_name):
    rules = PHONETIC_TRANSLITERATIONS.get(language_name)

    if not rules:
        return word

    if len(word) > 3 and word.endswith("e"):
        word = word[:-1]

    pieces = []
    index = 0
    vowels = rules["vowels"]
    vowel_groups = rules["vowel_groups"]
    consonants = rules["consonants"]
    virama = rules["virama"]

    while index < len(word):
        vowel_group = next(
            (group for group in sorted(vowel_groups, key=len, reverse=True)
             if word.startswith(group, index)),
            None,
        )

        if vowel_group:
            pieces.append(vowel_groups[vowel_group][0])
            index += len(vowel_group)
            continue

        character = word[index]

        if character in vowels:
            pieces.append(vowels[character][0])
            index += 1
            continue

        consonant = next(
            (group for group in sorted(consonants, key=len, reverse=True)
             if word.startswith(group, index)),
            None,
        )

        if not consonant:
            pieces.append(character)
            index += 1
            continue

        native_consonant = consonants[consonant]
        next_index = index + len(consonant)
        next_vowel_group = next(
            (group for group in sorted(vowel_groups, key=len, reverse=True)
             if word.startswith(group, next_index)),
            None,
        )

        if next_vowel_group:
            pieces.append(native_consonant + vowel_groups[next_vowel_group][1])
            index = next_index + len(next_vowel_group)
            continue

        if next_index < len(word) and word[next_index] in vowels:
            pieces.append(native_consonant + vowels[word[next_index]][1])
            index = next_index + 1
            continue

        pieces.append(native_consonant + virama)
        index = next_index

    return "".join(pieces)


def apply_native_script_fallback(text, language_name):
    if language_name not in SCRIPT_FALLBACKS:
        return text

    return re.sub(
        r"\b[A-Za-z][A-Za-z0-9+-]*\b",
        lambda match: transliterate_latin_word(match.group(0), language_name),
        text,
    )


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


def get_sarvam_api_key(runtime_api_key=""):
    api_key = runtime_api_key.strip()

    if api_key:
        return api_key

    api_key = os.environ.get("SARVAM_API_KEY", "").strip()

    if api_key:
        return api_key

    try:
        return st.secrets.get("SARVAM_API_KEY", "").strip()
    except Exception:
        return ""


def is_sarvam_chat_api(api_url):
    normalized_api_url = api_url.strip().rstrip("/").lower()
    return (
        normalized_api_url == SARVAM_CHAT_API_URL
        or "api.sarvam.ai" in normalized_api_url
    )


def translate_with_sarvam(
    text,
    target_language_code,
    source_language_code="auto",
    api_key="",
):
    api_key = get_sarvam_api_key(api_key)

    if not api_key:
        raise ValueError("SARVAM_API_KEY is not configured")

    payload = {
        "input": text,
        "source_language_code": source_language_code,
        "target_language_code": target_language_code,
        "model": "mayura:v1",
        "mode": "classic-colloquial",
    }

    request = Request(
        "https://api.sarvam.ai/translate",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "api-subscription-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 DailyAffirmationsApp/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ValueError(f"Sarvam translation failed with status {error.code}") from error
    except URLError as error:
        raise ValueError("Could not reach Sarvam translation service") from error
    except TimeoutError as error:
        raise ValueError("Sarvam translation timed out") from error
    except json.JSONDecodeError as error:
        raise ValueError("Sarvam translation returned an invalid response") from error

    translated_text = data.get("translated_text", "").strip()

    if not translated_text:
        raise ValueError("Sarvam translation returned a blank response")

    return translated_text


def build_reflection_prompt(
    reflection,
    response_language_name="English",
):
    language_instruction = (
        "Answer in clear, natural English before any optional translation."
    )

    if response_language_name != "English":
        script_fallback = SCRIPT_FALLBACKS[response_language_name]
        language_instruction = (
            f"Respond in {response_language_name} because enhanced translation "
            "is unavailable. If an English word has no natural translation, "
            f"write it in {script_fallback['script']} script instead of Latin "
            f"letters. Examples: {script_fallback['examples']}."
        )

    return (
        "You are a friendly daily reflection assistant inside a Daily "
        "Affirmations app. "
        f"{language_instruction} "
        "Keep your response grounded, simple, and brief. "

        "First decide whether the user's message contains an actual "
        "reflection, emotion, concern, or personal thought. "

        "If it does, write one warm and practical personalized affirmation "
        "based only on what the user actually said. "
        "Avoid flowery, theatrical, or overly poetic language. "
        "Do not invent emotions, struggles, or hidden meanings. "
        "Do not write the word 'Affirmation:' before the response. "

        "If the message is only a greeting, a casual question, random text, "
        "or does not contain enough information, politely ask the user to "
        "share how they are feeling today. "
        "Do not generate an affirmation in that case. "

        "Keep the response to one or two short sentences. "
        "Do not give medical, legal, political, or religious advice. "
        "Do not diagnose the user. "
        "If the reflection sounds serious or unsafe, respond gently and "
        "suggest reaching out to a trusted person or local support. "

        "\n\n"
        f"User message: {reflection}"
    )


def generate_personal_affirmation(
    assistant_mode,
    language_name,
    language,
    reflection_text,
    api_url=None,
    api_key=None,
    model=None,
    ollama_url=None,
    ollama_model=None,
    sarvam_api_key="",
):
    def request_ai(prompt):
        if assistant_mode == language["byot_mode"]:
            return request_online_affirmation(
                api_url.strip(),
                api_key.strip(),
                model.strip(),
                prompt,
                sarvam_api_key=sarvam_api_key,
            )

        return request_ollama_affirmation(
            ollama_url.strip(),
            ollama_model.strip(),
            prompt,
        )

    if language_name == "English":
        prompt = build_reflection_prompt(reflection_text)
        return request_ai(prompt)

    sarvam_api_key = get_sarvam_api_key(sarvam_api_key)

    if not sarvam_api_key:
        st.warning(language["sarvam_key_warning"])
        prompt = build_reflection_prompt(reflection_text, language_name)
        return apply_native_script_fallback(request_ai(prompt), language_name)

    target_language_code = SARVAM_LANGUAGE_CODES[language_name]

    try:
        english_reflection = translate_with_sarvam(
            reflection_text,
            "en-IN",
            source_language_code="auto",
            api_key=sarvam_api_key,
        )
    except ValueError:
        st.warning(language["sarvam_failure_warning"])
        prompt = build_reflection_prompt(reflection_text, language_name)
        return apply_native_script_fallback(request_ai(prompt), language_name)

    prompt = build_reflection_prompt(english_reflection)
    english_affirmation = request_ai(prompt)

    try:
        translated_affirmation = translate_with_sarvam(
            english_affirmation,
            target_language_code,
            source_language_code="en-IN",
            api_key=sarvam_api_key,
        )
        return apply_native_script_fallback(translated_affirmation, language_name)
    except ValueError:
        st.warning(language["sarvam_failure_warning"])
        return apply_native_script_fallback(english_affirmation, language_name)


def request_online_affirmation(api_url, api_key, model, prompt, sarvam_api_key=""):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You write short, safe, personalized affirmations.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 120,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 DailyAffirmationsApp/1.0",
    }

    if is_sarvam_chat_api(api_url):
        headers["api-subscription-key"] = get_sarvam_api_key(sarvam_api_key)
    else:
        headers["Authorization"] = f"Bearer {api_key.strip()}"

    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
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
            "temperature": 0.3,
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

api_key = ""
api_url = DEFAULT_ONLINE_API_URL
model = ""
ollama_url = ""
ollama_model = ""
sarvam_api_key = ""

if assistant_mode == language["byot_mode"]:
    api_url = st.text_input(
        language["api_url_label"],
        value=DEFAULT_ONLINE_API_URL,
    )
    model = st.text_input(language["online_model_label"], value="llama-3.3-70b-versatile")

    if is_sarvam_chat_api(api_url):
        sarvam_api_key = st.text_input(
            language["sarvam_key_label"],
            type="password",
            help=language["sarvam_key_help"],
        )
    else:
        api_key = st.text_input(
            language["api_key_label"],
            type="password",
            help=language["api_key_help"],
        )
        sarvam_api_key = st.text_input(
            language["sarvam_key_label"],
            type="password",
            help=language["sarvam_key_help"],
        )

    if language_name != "English":
        st.caption(language["translation_caption"])

    show_help_popup(language["api_key_help_title"], language["api_key_steps"])
else:
    if language_name != "English":
        sarvam_api_key = st.text_input(
            language["sarvam_key_label"],
            type="password",
            help=language["sarvam_key_help"],
        )
        st.caption(language["ollama_translation_caption"])

    ollama_url = st.text_input(
        language["ollama_url_label"],
        value="http://localhost:11434",
    )
    ollama_model = st.text_input(language["ollama_model_label"], value="llama3.2")
    show_help_popup(language["ollama_url_help_title"], language["ollama_url_steps"])
    show_help_popup(language["ollama_setup_title"], language["ollama_setup_steps"])
    show_help_popup(language["cloudflare_help_title"], language["cloudflare_steps"])

if st.button(language["generate_button"]):
    reflection_text = reflection.strip()

    if not reflection_text:
        st.warning(language["empty_reflection"])
    elif (
        assistant_mode == language["byot_mode"]
        and is_sarvam_chat_api(api_url)
        and not get_sarvam_api_key(sarvam_api_key)
    ):
        st.warning(language["missing_sarvam_key"])
    elif (
        assistant_mode == language["byot_mode"]
        and not is_sarvam_chat_api(api_url)
        and not api_key.strip()
    ):
        st.warning(language["missing_key"])
    else:
        try:
            with st.spinner(language["reflection_heading"]):
                personal_affirmation = generate_personal_affirmation(
                    assistant_mode,
                    language_name,
                    language,
                    reflection_text,
                    api_url=api_url if assistant_mode == language["byot_mode"] else None,
                    api_key=api_key if assistant_mode == language["byot_mode"] else None,
                    model=model if assistant_mode == language["byot_mode"] else None,
                    ollama_url=ollama_url if assistant_mode == language["ollama_mode"] else None,
                    ollama_model=ollama_model if assistant_mode == language["ollama_mode"] else None,
                    sarvam_api_key=sarvam_api_key,
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
        except HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            st.error(f"Online AI request failed ({error.code}): {error_body}")
        except URLError as error:
            st.error(f"Could not reach the AI service: {error.reason}")
        except TimeoutError:
            st.error("The AI request timed out. Please try again.")
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            st.error(f"The AI service returned an unexpected response: {error}")
