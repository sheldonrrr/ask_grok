
# Ask AI Plugin User Manual v0.5
Latest updated: December 22, 2025, Ask AI Plugin v1.3.7

ToC of this tutorial:
- Explain: Why & What is API Keys
- Free API Key Options
- Installation
- First Time Setup an AI Service
- How to Use
- Keyboard Shortcuts
- Random Questions
- Other Features
- Configuration
- Troubleshooting
- Privacy
- Tips
- Getting Help

Note: This plugin was renamed from Ask Grok to Ask AI Plugin because it now supports multiple AI providers, not just Grok.

## Explain: Why & What is API Keys

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

Option 2: Google Gemini
- Free tier: 15 requests per minute
- Get key at: https://aistudio.google.com/

Option 3: OpenRouter
- Free models: there are some free models available at: https://openrouter.ai/models?q=free
- Get key at: https://openrouter.ai/settings/keys

Option 4: Ollama (Local, No Internet)
- Cost: Free forever
- Privacy: Runs on your computer, nothing sent online
- Setup: Download from https://ollama.com/ and install
- Run in terminal: ollama pull llama3.2
- Select Ollama in plugin, no API key needed

## Installation

Method 1 (Recommended):
1. Open calibre
2. Go to Preferences -> Plugins -> Get new plugins
3. Search for "Ask AI Plugin" (Author: Sheldon)
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
2. Select Configuration
3. Find Nvidia AI section
4. Paste your API key
5. Base URL is already filled in
6. Click Load Model List button
7. Select a model from dropdown

Done!

## How to Use

1. Select a book or multiple books in calibre
2. Open Ask dialog:
   - Click Ask AI Plugin button in toolbar, or
   - Use the global shortcut (default: F3)
3. Type your question
4. Click Send (or use Ctrl+Enter / Cmd+Enter)

The plugin automatically includes book metadata. You don't need to type title or author.

### Perplexity (Sonar) for Research

Perplexity is useful when you want answers with sources.

When Perplexity returns citations/search results, the plugin appends a plain-text "Citations" / "Search Results" section (with full URLs) at the end of the answer, so you can copy/paste the links.

## Keyboard Shortcuts

This plugin supports full shortcut customization via calibre.

How to customize:
1. Open calibre
2. Go to Preferences -> Shortcuts
3. Search for "Ask AI"
4. Edit the shortcuts you want

Common shortcuts (defaults):
- Ask AI: Ask (global): F3
- Ask AI: Open Configuration: F2
- Ask AI: Send (in dialog): Ctrl+Enter (Cmd+Enter on macOS)
- Ask AI: Random Question (in dialog): Ctrl+R (Cmd+R on macOS)

Note: If you customized shortcuts in calibre, your custom settings take precedence.

## Random Questions

1. Click Random Question button (or Ctrl+R / Cmd+R)
2. AI suggests a question

Customize prompts in Configuration -> Edit Random Question Prompts

## Other Features

- Parallel AI Comparison: Set Parallel AI Panels to 2 in Configuration, then compare responses from different AIs side-by-side
- History: Auto-saved conversations, click History button to view past Q&A
- PDF Export: Click Export PDF to save conversations, set default folder in Configuration -> Export Settings

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
- Prompts if you customize them

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

## Getting Help

GitHub: https://github.com/sheldonrrr/ask_grok
calibre Forum: https://www.mobileread.com/forums/showthread.php?p=4547077
Email: sheldonrrr@gmail.com

