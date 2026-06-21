# Daily Affirmations

Daily Affirmations is a Streamlit app that shows a positive affirmation in the selected language. Version 1.1.0 supports English, Hindi, and Telugu and adds an optional reflective AI assistant that can turn a user's daily reflection into a short personalized affirmation.

The preset affirmation feature works without an AI key, internet connection, database, or user account. AI features are optional.

## Deployed App

The Streamlit deployment is available here:

https://daily-affirmations-archisha.streamlit.app/

## Features

- Random preset affirmations in English, Hindi, and Telugu
- 60 project-created affirmations per language
- Localized homepage text for the selected language
- Simple Streamlit interface with a centered affirmation card
- Optional reflection box for mood or daily thoughts
- BYOT online AI mode, where users enter their own API key at runtime
- OpenAI-compatible chat completions support, including Groq-style endpoints
- Local Ollama AI mode for local assistant use
- Optional Sarvam translation support for enhanced Hindi and Telugu AI responses
- Native-script fallback for Hindi and Telugu when enhanced translation is not configured
- Graceful fallback if the AI assistant is unavailable

## Requirements

- Python 3.10 or newer
- Streamlit, installed from `requirements.txt`
- Optional: Ollama for local AI assistant mode
- Optional: an online AI provider API key for BYOT mode
- Optional: Sarvam API key for enhanced Hindi and Telugu AI translation

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

## Developer Checks

Install local hook tooling:

```bash
pip install -r requirements-dev.txt
git config core.hooksPath .githooks
```

Run the same checks manually:

```bash
python scripts/local_checks.py --stage pre-commit
python scripts/local_checks.py --stage pre-push
```

Pre-commit checks cover formatting, linting, Python compilation, unit tests,
secret scanning, and affirmation data compliance. Pre-push checks add type
checking, dead code checking, security scanning, and package audits.

## AI Reflection Assistant

The AI assistant is optional. The normal daily affirmation still works if the AI service is not configured.

After reading the preset affirmation, users can write a short reflection in the text box. The assistant considers both the selected app language and the language typed by the user, then returns one or two short supportive sentences in the most suitable supported language.

Supported languages:

- English
- Hindi
- Telugu

### BYOT Online Assistant

BYOT means "Bring Your Own Tokens." In this mode, the user provides their own online AI provider key in the app.

1. Select `BYOT online assistant`.
2. Enter an API key in the password-style key field.
3. Confirm the API URL. The app default is:

```text
https://api.groq.com/openai/v1/chat/completions
```

4. Confirm the model name. The app default is:

```text
llama-3.3-70b-versatile
```

5. Write a reflection and click the generate button.

Any OpenAI-compatible chat completions endpoint can be used if the provider accepts the same `Authorization: Bearer <key>` header and chat completions response shape.

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

3. Start Ollama. On desktop installs, opening the Ollama app usually starts the local server. On CLI-only installs, run:

```bash
ollama serve
```

Do not run both the desktop app and `ollama serve` on the same port.

4. Confirm Ollama is reachable:

```bash
curl http://localhost:11434/api/tags
```

The app uses Ollama's `POST /api/generate` endpoint and appends `/api/generate` itself, so the Ollama URL field should contain only the base URL:

```text
http://localhost:11434
```

5. Start the Streamlit app:

```bash
streamlit run app.py
```

6. Select `Local Ollama assistant`, keep the Ollama URL as `http://localhost:11434`, and use the model name you pulled, such as `llama3.2`.

If Ollama is not running or the selected model is unavailable, the app shows a friendly error and keeps the preset affirmation feature available.

When the app is deployed on the web, `localhost` points to the deployment server, not the user's computer. For demos that need to connect a deployed app to a local Ollama process, the in-app help explains how to use a temporary Cloudflare Tunnel URL. Do not share that tunnel URL publicly.

### Sarvam Translation

For Hindi and Telugu AI responses, the app can use Sarvam Translate around the English assistant step. The flow is:

1. Sarvam translates the user's Hindi or Telugu reflection to English.
2. The selected AI provider or local Ollama model generates the personalized affirmation in English.
3. Sarvam translates that English affirmation back to the selected language.

Sarvam keys can be provided in one of these ways:

- In the runtime password field shown for Hindi and Telugu
- As `SARVAM_API_KEY` in the process environment
- As `SARVAM_API_KEY` in Streamlit secrets

If no Sarvam key is configured, the assistant still works. It asks the selected model to respond directly in Hindi or Telugu and applies a small native-script fallback for common Latin words.

## Environment Example

The app accepts BYOT and Ollama settings through the Streamlit UI at runtime. `.env.example` is included as a safe reference for local developers and deployment configuration. The only environment/secret value read directly by the current app is `SARVAM_API_KEY`.

Do not put real keys in `.env.example`, and do not commit local `.env` files.

Example local setup:

```bash
cp .env.example .env
```

Then fill `.env` only on your own machine if you use it for local notes, deployment tooling, or future configuration. Streamlit does not automatically load `.env` files; use shell exports, deployment settings, or Streamlit secrets for values the app should read.

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
- OpenAI-compatible chat completions support for BYOT mode through Python standard-library HTTP requests
- Sarvam Translate API support for optional Hindi and Telugu translation
- Spec Kit documentation for task organization

## Privacy and Safety

- Reflections are not stored by this app.
- BYOT API keys are entered at runtime and are not saved.
- Local Ollama mode can run without sending reflections to an online provider.
- Hindi and Telugu enhanced translation sends reflection text and generated affirmation text to Sarvam when a Sarvam key is configured.
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
