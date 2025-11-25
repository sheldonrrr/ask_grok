# Ask AI Plugin User Manual

Plugin version: 1.3.3
Tutorial version: 0.3
Last updated: November 25, 2025

This manual covers:
- Installation
- Free API key options
- Basic usage
- Common problems and solutions

Note: This plugin was renamed from Ask Grok to Ask AI Plugin because it now supports multiple AI providers, not just Grok.

## Important: About API Keys

Many users are confused why their ChatGPT Plus or Gemini subscription doesn't work with this plugin.

Here's why: AI companies separate their services into two types:
- Consumer subscriptions: For using their website or app directly
- API keys: For developers and tools like this plugin

These are separate services with separate billing. Your ChatGPT Plus subscription won't work here.

Good news: You don't need to pay. Free options are available below.

## Free API Key Options

Option 1: Nvidia (Recommended)
- Cost: Free
- Limit: 40 requests per minute
- Setup: Visit https://build.nvidia.com/ and sign up
- Get your API key and paste it in the plugin's Nvidia AI configuration

Option 2: Ollama (Local, No Internet)
- Cost: Free forever
- Privacy: Runs on your computer, nothing sent online
- Setup: Download from https://ollama.com/ and install
- Run in terminal: ollama pull llama3.2
- Select Ollama in plugin, no API key needed

Option 3: Google Gemini
- Free tier: 15 requests per minute
- Get key at: https://aistudio.google.com/

## Installation

Method 1 (Recommended):
1. Open calibre
2. Go to Preferences -> Plugins -> Get new plugins
3. Search for "Ask AI"(Author: Sheldon)
4. Click Install
5. Restart calibre

Method 2 (Manual):
1. Download from https://www.mobileread.com/forums/showthread.php?p=4547077
2. Go to Preferences -> Plugins -> Load Plugin from file
3. Select the .zip file
4. Restart calibre

## First Time Setup an AI Service

Example: Setting up Nvidia AI (free)

1. Click Ask AI Plugin menu in calibre toolbar
2. Select Configure
3. Find Nvidia AI section
4. Paste your API key
5. Base URL is already filled in
6. Click Load Model List button
7. Select a model from dropdown
8. Saved appear(Now automatically selected)

Done!

## How to Use

1. Select a book or multiple books in calibre
2. Click Ask AI button in toolbar
3. Type your question
4. Click Send (or Ctrl+Enter)

The plugin automatically includes book metadata. You don't need to type title or author.

## Random Questions

1. Click Random Question button
2. AI suggests a question

Customize prompts in Configure -> Edit Random Question Prompts

## Other Features

- **Parallel AI Comparison**: Set Parallel AI Panels to 2 in Configure, then compare responses from different AIs side-by-side
- **History**: Auto-saved conversations, click History button to view past Q&A
- **PDF Export**: Click Export PDF to save conversations, set default folder in Configure -> Export Settings

## Configuration

General Settings:
- Language Change
- Dialog Size: Adjust window size
- Parallel AI Panels: Set to 2 for side-by-side comparison

AI Provider Settings:
- API Key: Your authentication key
- Base URL: Usually pre-filled
- Model: Select from dropdown or enter custom
- Enable Streaming: Get responses word-by-word

Template Settings:
- Customize prompts for single book, multiple books, or random questions

Export Settings:
- Set default PDF save location

## Keyboard Shortcuts

- Open Ask Dialog: F3
- Open Config: F2
- Send Question: Ctrl+Enter (Cmd+Enter on Mac)
- Random Question: Ctrl+R (Cmd+R on Mac)
- Close Dialog: Esc

## Troubleshooting

Request Failed:
- Check internet connection
- Verify API key is correct
- Try different AI provider

API Key Invalid:
- Copy entire key without spaces
- Check key hasn't expired
- For Grok: use key from console.x.ai, not x.com

Ollama Not Working:
- Make sure Ollama is installed and running
- Pull a model: ollama pull llama3.2
- Check models: ollama list
- Confirm service running: ollama serve

## Privacy

What is sent to AI:
- Book metadata (title, author, publisher, date, language)
- Your questions

NOT sent:
- Your calibre tags, comments, or reviews
- Reading progress
- Personal data

API Key Storage:
- Stored locally on your computer
- Never sent to third parties
- Location: calibre config folder/plugins/ask_ai_plugin.json

For maximum privacy: Use Ollama (runs locally, nothing sent online).

## Tips

1. First ask: "Is this book in your training data?" If AI says no, it can't help much.
2. Use parallel panels to compare different AIs.
3. Be specific in questions for better answers.

## Recent Updates

v1.3.3 (November 2025):
- Better PDF export with book titles
- Fixed language switching bugs
- Improved parallel AI display

v1.3.2 (November 2025):
- Added OpenAI, Anthropic, Nvidia support
- Parallel AI comparison
- PDF export
- Multiple books support
- Renamed to Ask AI Plugin

## Getting Help

GitHub: https://github.com/sheldonrrr/ask_grok
calibre Forum: https://www.mobileread.com/forums/showthread.php?p=4547077
Email: sheldonrrr@gmail.com

## FAQ

Q: Why doesn't my ChatGPT Plus work?
A: Subscriptions and API keys are separate services. Use free options like Nvidia or Ollama.

Q: What's a token?
A: About 4 characters. A typical Q&A uses 500-2000 tokens.

Q: Can I ask about book content?
A: Plugin only sends metadata. AI answers from its training data.

Q: Is my data shared?
A: Only book metadata is sent. Your library and reading history stay private.

Q: Why is Ollama slower?
A: Runs on your computer. Cloud AIs use powerful servers. Trade-off: Ollama is free and private.

---

Help improve it:
- Give me feedbacks on Reddit: https://www.reddit.com/r/AskGrokPlugin/