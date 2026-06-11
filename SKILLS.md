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


