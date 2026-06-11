# Daily Affirmations

Daily Affirmations is a simple Streamlit app that shows a positive affirmation in the selected language. Version 1.1.0 adds English, Hindi, and Telugu language options plus an optional AI reflection assistant that can create a short personalized affirmation from the user's daily reflection.

The preset affirmation feature works without an AI key, internet connection, database, or user account.

## Deployed App

The Streamlit deployment is available here:

https://daily-affirmations-archisha.streamlit.app/

## Features

- Random preset affirmations in English, Hindi, and Telugu
- Localized homepage text for the selected language
- Simple Streamlit interface with a centered affirmation card
- Optional reflection box for mood or daily thoughts
- BYOT online AI mode, where users enter their own API key at runtime
- Local Ollama AI mode for offline/local assistant use
- Graceful fallback if the AI assistant is unavailable

## Requirements

- Python 3.10 or newer
- Streamlit
- Optional: Ollama for local AI assistant mode
- Optional: an online AI provider API key for BYOT mode

## Run Locally

1. Clone the repository:

```bash
git clone https://github.com/ArchLovesGames/Daily-Affirmations.git
cd Daily-Affirmations
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run app.py
```

5. Open the local URL shown in the terminal. Streamlit usually uses:

```text
http://localhost:8501
```

If the `streamlit` command is not available, run:

```bash
python3 -m streamlit run app.py
```

## AI Reflection Assistant

The AI assistant is optional. The normal daily affirmation still works if the AI service is not configured.

After reading the preset affirmation, users can write a short reflection in the text box. The assistant considers both the selected app language and the language typed by the user, then returns a short personalized affirmation in the most suitable supported language.

Supported languages:

- English
- Hindi
- Telugu

### BYOT Online Assistant

BYOT means "Bring Your Own Tokens." In this mode, the user provides their own online AI provider key in the app.

1. Select `BYOT online assistant`.
2. Enter an API key in the password-style key field.
3. Confirm the API URL. The default is:

```text
https://api.openai.com/v1/chat/completions
```

4. Confirm the model name. The default is:

```text
gpt-4o-mini
```

5. Write a reflection and click the generate button.

The API key is used only for the current request and is not saved by the app.

### Local Ollama Assistant

Use this mode to run the assistant through a local Ollama model.

1. Install Ollama from:

```text
https://ollama.com/
```

2. Pull a model, for example:

```bash
ollama pull llama3.2
```

3. Make sure Ollama is running locally. The app expects this default endpoint:

```text
http://localhost:11434
```

4. Start the Streamlit app:

```bash
streamlit run app.py
```

5. Select `Local Ollama assistant`, keep the Ollama URL as `http://localhost:11434`, and use the model name you pulled, such as `llama3.2`.

If Ollama is not running or the selected model is unavailable, the app shows a friendly error and keeps the preset affirmation feature available.

## Environment Example

The app currently accepts AI settings through the Streamlit UI at runtime. `.env.example` is included as a safe reference for local developers and deployment configuration. Do not put real keys in `.env.example`, and do not commit local `.env` files.

Example local setup:

```bash
cp .env.example .env
```

Then fill `.env` only on your own machine if you use it for local notes, deployment tooling, or future configuration.

## Project Structure

```text
Daily-Affirmations/
├── app.py
├── data/
│   ├── affirmations_en.txt
│   ├── affirmations_hi.txt
│   └── affirmations_te.txt
├── assets/
│   └── thumbs_up.jpeg
├── .env.example
├── README.md
├── USER_MANUAL.md
├── SECURITY.md
├── CHANGELOG.md
└── requirements.txt
```

## Tech Stack

- Streamlit for the app UI
- Plain text files for preset affirmation data
- Ollama API support for local AI mode
- OpenAI-compatible chat completions support for BYOT mode
- Spec Kit documentation for task organization

## Privacy and Safety

- Reflections are not stored by this app.
- BYOT API keys are entered at runtime and are not saved.
- Local Ollama mode can run without sending reflections to an online provider.
- The AI response is intended for short supportive affirmations, not medical, legal, crisis, political, or religious advice.

## Authors

- [@ArchLovesGames](https://www.github.com/ArchLovesGames)

## Acknowledgements

- [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
- [Awesome README](https://github.com/matiassingers/awesome-readme)
- [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
- Thanks to the Swecha team for the hackathon task

## Contributing

Contributions are welcome. See `CONTRIBUTING.md` for ways to get started and follow the project's `CODE_OF_CONDUCT.md`.

## Support and Feedback

For support or feedback, email archisha.singh@gmail.com.
