
Daily Affirmations Agent Instructions

Role: You are a Streamlit Python developer asked to add localisation features to 
a base app called Daily Affirmations, which currently supports only English.

You are required to first compile affirmations in 3 different languages: Telugu, Hindi and English. 
To avoid serious copyright infridgement, you are NOT allowed to use licensed sources to extract the data.
Once the data has been compiled, edit the app.py file to integrate the language change feature, ensuring language change changes the homepage language and affirmation.

Note that for the data collection, it is not mandatory to find 200 quotes per language if resources cannot be found. However, copyright cannot be infrindged at any cost. 
If license is unsure, leave it.

Skills have been available to explain each workflow required with detailed specifications.

NEW INSTRUCTION

You are an AI Assistant website integration developer who has been given base application to which you 
have been asked to integrate a reflectful AI assistant where
a user can put down their daily reflection after looking at the preset 
affirmation message and the AI can give them a personalised affirmation.

NO EDITS should be made to the original functionality. Only app.py can be edited for 
this functionality, however extra files may be added if required.

The user should have a small box prompting them to reflect on their mood. 
The AI then takes their response, sees the language they typed in as well as language selected, and responds in 
that language with a small affirmation personalised to that thought below.
It should be easy and accessible to users. 

There are two modes through which a user can use the AI assistant.
The first mode is BYOT (Bring your own tokens), Where they can use
an online ai assistant and use their own tokes. The second is local
AI assistant using Ollama integration which users can connect with their
local agent to use.

If any keys are required, you are allowed to edit .env.example to accomodate for the same. You
may also halt processes if you require the human developer to provide any info.

Skills have been made available to explain the workflow. Refer to the reflective-ai-assistant skill for the same.