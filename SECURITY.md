# Security Policy

## Supported Version

The current documented release is `1.1.0`.

## Reporting Security Issues

This is a beginner-friendly Streamlit project. It does not use accounts, payments, a database, or server-side storage for reflections.

If you find a security issue, please report it through the repository issue tracker.

## Sensitive Data

Do not commit:

- API keys
- Passwords
- Personal tokens
- `.env` files
- Streamlit secrets
- Provider credentials
- Private reflection logs

Only placeholders should be committed in `.env.example`.

## AI Reflection Assistant Security

The AI reflection assistant has two modes:

- BYOT online assistant: the user enters their own API key at runtime.
- Local Ollama assistant: the app connects to a local Ollama endpoint, usually `http://localhost:11434`.
- Optional Sarvam translation: Hindi and Telugu assistant responses can use Sarvam translation when a Sarvam key is supplied.

Security notes:

- BYOT API keys are entered through a password-style field.
- The app does not intentionally save, print, or commit API keys.
- Reflections are not stored by the app.
- In BYOT mode, reflections are sent to the configured online AI provider.
- In local Ollama mode, reflections are sent to the configured local Ollama server.
- If Sarvam translation is enabled, reflections and generated affirmations are sent to Sarvam for translation.
- Users should only connect to AI endpoints they trust.
- Temporary tunnel URLs for local Ollama demos should be treated as sensitive and should not be shared publicly.

## Secret Handling

The app reads `SARVAM_API_KEY` from the runtime password field, the process environment, or Streamlit secrets. BYOT provider keys are currently entered in the UI at runtime and are not read from `.env.example`.

Recommended practices:

- Use Streamlit secrets or deployment environment variables for hosted deployments.
- Use local shell environment variables for local testing.
- Do not commit `.env`, `.streamlit/secrets.toml`, API keys, tunnel URLs, or provider tokens.
- Rotate any key that was pasted into a public issue, committed file, screenshot, or shared terminal log.

## Environment Files

`.env.example` is safe to commit because it contains placeholder values only.

Local `.env` files must stay private. They are intended for local developer notes, deployment tooling, or future configuration and should not contain production secrets in version control.

Streamlit does not automatically load `.env` files. If a value must be available to the app, provide it through the shell, deployment configuration, or Streamlit secrets.

## Safety Scope

The assistant is intended to generate short supportive affirmations only. It should not be treated as medical, mental health, legal, crisis, political, or religious advice.

If a reflection sounds serious or unsafe, the prompt directs the model to respond gently and suggest reaching out to a trusted person or local support. This is a safety prompt, not a professional support system.
