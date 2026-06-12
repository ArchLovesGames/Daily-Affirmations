# User Manual

## Daily Affirmations

Daily Affirmations is a Streamlit app that displays a random positive affirmation. Version 1.1.0 supports English, Hindi, and Telugu, and includes an optional AI reflection assistant for personalized affirmations.

## How to Use the Preset Affirmation

1. Open the app.
2. Choose a language from the language selector.
3. Read the homepage text and affirmation in the selected language.
4. Refresh the page to see another random affirmation.

## Language Options

The app currently supports:

- English
- Hindi
- Telugu

Changing the language updates the page text and the preset affirmation source.

Each language currently has 60 preset affirmations.

## How to Use the AI Reflection Assistant

The AI assistant appears below the preset affirmation. It is optional, so the main affirmation feature works even if no AI service is connected.

1. Write a short reflection in the text box, such as how you feel today or what is on your mind.
2. Choose an assistant mode.
3. Enter the required connection details for that mode.
4. Click the generate button.
5. Read the personalized affirmation shown below the button.

The assistant considers both the selected app language and the language used in the reflection. It usually responds in the selected language unless the reflection is clearly written in another supported language.

## BYOT Online Assistant Mode

Use BYOT mode when you want to connect an online AI provider with your own token.

1. Select `BYOT online assistant`.
2. Enter your API key in the password field.
3. Keep or edit the API URL. The default is `https://api.groq.com/openai/v1/chat/completions`.
4. Keep or edit the model name. The default is `llama-3.3-70b-versatile`.
5. Generate the personalized affirmation.

The key is only used for the request and is not saved by the app.

The online provider must support OpenAI-compatible chat completions. Sarvam Chat Completion can also be used with API URL `https://api.sarvam.ai/v1/chat/completions` and model `sarvam-30b`.

## Local Ollama Assistant Mode

Use local mode when you want the assistant to run through Ollama on your machine.

1. Install Ollama.
2. Pull a model, for example:

```bash
ollama pull llama3.2
```

3. Confirm Ollama is running at:

```text
http://localhost:11434
```

4. Select `Local Ollama assistant` in the app.
5. Enter the model name, such as `llama3.2`.
6. Generate the personalized affirmation.

If Ollama is not running or the model is not available, the app shows an error message and the normal affirmation feature remains usable.

If the app is deployed online and you want it to reach Ollama running on your own computer, use the Cloudflare Tunnel instructions shown inside the app. The tunnel URL is temporary and should not be shared publicly.

## Hindi and Telugu Translation

When Hindi or Telugu is selected, the app shows an optional Sarvam API key field for enhanced translation.

Use this field if you want Sarvam to:

- Translate the user's reflection to English for the AI model
- Translate the generated affirmation back to the selected language

If you do not enter a Sarvam key, the assistant still tries to respond directly in the selected language. The app also applies a small fallback that rewrites common Latin words into Hindi or Telugu script.

Developers can also provide `SARVAM_API_KEY` through the process environment or Streamlit secrets.

## What the AI Assistant Is For

The assistant is designed to create short, positive, personalized affirmations. It is not a replacement for professional support and should not be used for medical, legal, crisis, political, or religious advice.

If your reflection is urgent, unsafe, or about immediate harm, contact a trusted person or local emergency support instead of relying on the app.

## Files Used

- `app.py` contains the app code.
- `data/affirmations_en.txt` contains English affirmations.
- `data/affirmations_hi.txt` contains Hindi affirmations.
- `data/affirmations_te.txt` contains Telugu affirmations.
- `assets/thumbs_up.jpeg` contains the frontend image.
- `.env.example` contains safe placeholder examples for optional AI configuration.
