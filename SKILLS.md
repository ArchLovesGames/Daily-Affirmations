---
name: affirmation-curation
description: Create, clean, expand, and validate affirmation datasets in English, Hindi and Telugu for the Daily Affirmations app.
---

# Affirmation Curation Skill

## Purpose

Maintain high-quality affirmation text files for the app in the data folder.
Seperate files for each of the three languages, English, Hindi, and Telugu

## Responsibilities

- Create affirmation datasets toward 200 affirmations for each language.
- Remove duplicates.
- Keep one affirmation per line.
- Keep affirmations short, positive, and readable.
- Avoid copyrighted or unclear-license content. If sources are not available and affirmations are less than 200, assume the dataset compilation is complete and move on.
- Avoid medical, political, hateful, or religiously sensitive claims.

## Files
Delete the original data/affirmations.txt file
Then create and work with:

- `data/affirmations_en.txt`
- `data/affirmations_hi.txt`
- `data/affirmations_te.txt`

## Rules

- Do not copy random internet content unless license allows reuse.
- Prefer project-created or openly licensed content.
- Keep affirmations positive and sfw for all.
- Do not break any license rules to meet the 200 limit. If 200 cannot be reached, assume completed task and move on.

## Validation Checklist

- [ ] One affirmation per line
- [ ] No duplicates
- [ ] No blank lines
- [ ] No unsafe content
- [ ] Files are UTF-8 compatible

---

name: streamlit-ui-development
description: Add the intended translation and localisation support to the base application
---


# Streamlit UI Development

## Purpose

A simple base application for the daily affirmations has been created that only supports English.
Using the new dataset with affirmations for all 3 languages, create a feature where language change can be supported from English to Hindi or Telugu.

## Responsibilities

- Keep the content centered.
- Keep the affirmation card readable.
- Make the image display cleanly.
- Keep the layout simple.
- Have the change language button visible.
- Add support for the language of the homepage to be translated to native languages when change language is selected.
- Avoid unnecessary frameworks.
- Preserve beginner-level Python code.

## UI Rules

- Use Streamlit built-in components where possible.
- Use small amounts of HTML/CSS only when needed.
- Do not overcomplicate the app.
- Ensure language change means the entire page is translated, not just affirmations.
- Ensure text is readable in both light and dark mode.
- Avoid shrinking the preset image or using low-contrast text.

## Existing UI Elements

- Centered title
- Subtitle
- Thumbs-up image
- Affirmation card
- Language selector


---
name: reflective-ai-assistant
description: Add a reflective AI assistant to Daily Affirmations using BYOT or local Ollama without changing the base affirmation functionality.
---

# Reflective AI Assistant Skill

## Purpose

Add an optional AI-powered reflection assistant to the Daily Affirmations app.

The assistant allows users to write a short daily reflection after seeing a preset affirmation. The AI then responds with a small personalized affirmation in the appropriate language.

## Core Rule

Do not change or remove the original affirmation functionality.

Only extend the app by adding the reflective AI assistant below the existing affirmation experience.

## Allowed Files

Primary file to edit:

- `app.py`

Extra files may be added only if required.

Allowed supporting file:

- `.env.example`

## User Experience

After the preset affirmation is displayed, show a small reflection box.

The user should be able to type how they feel or what they are thinking.

Example:

```text
I feel nervous about my project demo.

The AI should respond with a short personalized affirmation.

Example:

You have prepared step by step. Trust your effort and take one small action at a time.
```

Language Behavior

The AI should consider:

The language selected in the app.
The language typed by the user.

The response should be in the most suitable language.

Supported languages:

English
Hindi
Telugu

If the selected language and typed language differ, prefer the selected app language unless the user clearly writes in another language.

AI Modes

The app must support two AI modes.

BYOT: Bring Your Own Tokens
Users can enter their own API key/token.

Rules:

Token must be entered at runtime.
Use password-style input.
Do not save the token.
Do not print the token.
Do not commit the token.
Do not require the token for the base app to work.
Local AI: Ollama

Users can connect to a local Ollama instance.

Default local endpoint:

http://localhost:11434

Rules:

The app should fail gracefully if Ollama is not running.
The base app must continue working.
Do not require internet for Ollama mode.
Reflection Prompt Rules

The AI response must be:

Short
Positive
Personalized
Supportive
Non-medical
Non-diagnostic
Easy to understand
Suitable for students and young adults
Safety Rules

Do not generate:

Medical advice
Mental health diagnosis
Crisis counseling
Political persuasion
Religious persuasion
Hateful content
Long therapy-style responses

If the user writes something serious or unsafe, respond gently and suggest reaching out to a trusted person or local support.

UI Requirements

Add a small assistant section below the affirmation.

Suggested labels:

“Reflect for a moment”
“How are you feeling today?”
“Generate personalized affirmation”

The UI should be simple and accessible.

Fallback Behavior

If AI is off, unavailable, or fails:

Do not crash the app.
Show a friendly message.
Keep the normal affirmation feature working.

Example fallback:

AI reflection is unavailable right now, but your daily affirmation is still here for you.
Environment Variables

If needed, update .env.example with placeholders only.

Example:

# Optional BYOT token for online AI provider
AI_API_KEY=

# Optional Ollama endpoint
OLLAMA_BASE_URL=http://localhost:11434

Never add real keys.

Out of Scope
Login system
Database
Saving reflections
Saving API keys
Chat history
Voice input
User tracking

Then commit:

```bash
git add skills/reflective-ai-assistant/skill.md
git commit -m "Add reflective AI assistant skill"
git push origin main
git push github main
```