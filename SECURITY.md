# Security Policy

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

Security notes:

- BYOT API keys are entered through a password-style field.
- The app does not intentionally save, print, or commit API keys.
- Reflections are not stored by the app.
- In BYOT mode, reflections are sent to the configured online AI provider.
- In local Ollama mode, reflections are sent to the configured local Ollama server.
- Users should only connect to AI endpoints they trust.

## Environment Files

`.env.example` is safe to commit because it contains placeholder values only.

Local `.env` files must stay private. They are intended for local developer notes, deployment tooling, or future configuration and should not contain production secrets in version control.

## Safety Scope

The assistant is intended to generate short supportive affirmations only. It should not be treated as medical, mental health, legal, crisis, political, or religious advice.
