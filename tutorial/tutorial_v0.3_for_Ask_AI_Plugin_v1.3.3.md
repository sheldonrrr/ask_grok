# Ask AI Plugin User Manual v0.3

*Ask AI Plugin Version: 1.3.3, Updated: November 24, 2025*

**Note:** This version represents a major upgrade from Ask Grok (v1.2.x). The plugin has been renamed to Ask AI Plugin to reflect its support for 10+ AI providers.

---

## What's New in v1.3.x

### Major Changes

**Plugin Renamed: Ask Grok -> Ask AI Plugin**
- Originally supported only few AI providers.
- Now supports 8+ AI providers (OpenAI, Anthropic, Gemini, Grok, DeepSeek, Nvidia, OpenRouter, Ollama, and more)

**New AI Providers:**
- OpenAI
- Anthropic
- Nvidia AI (Free tier available)
- OpenRouter
- Ollama

**New Features:**
- Dynamic model list loading from AI providers
- Parallel AI requests (compare up to 4 AIs side-by-side)
- Multiple books support (ask about several books at once)
- PDF export (export Q&A and history)
- AI switcher in response panel
- Enhanced history system

---

## Getting Started

### Understanding API Keys

**What is an API Key?**

An API Key is a unique identifier that allows applications like this plugin to access AI services programmatically. Think of it as a password that lets the plugin talk to AI providers on your behalf.

**Important: Subscriptions vs API Keys**

Many users get confused about this. Here's the key difference:

- **Consumer Subscription (toC)**: When you pay for ChatGPT Plus, Gemini Advanced, or SuperGrok, you're buying access to use their website or mobile app directly.

- **API Key (toB)**: This is for developers and tools like this plugin. It's a separate service with different pricing, usually pay-per-use based on how many words (tokens) you send and receive. But anyone can buy their own API key from the provider's website.

**Why are they separate?**
- Subscriptions are for casual personal use with simple limits
- API Keys are for building apps and integrations, which have higher technical demands
- Companies charge separately because the infrastructure costs are different

**Examples:**
- **Grok (x.AI)**: Your SuperGrok subscription works on x.com, but you need API credits from console.x.ai for this plugin
- **Google Gemini**: Your Gemini Advanced subscription works in the app, but you need an API key from Google AI Studio for this plugin

**The Good News: Free Options Exist!**

You don't need to pay for API access. See the "Free API Options" section below.

---

### Free API Options

**1. Nvidia NIM (Recommended for Beginners)**

Nvidia offers FREE API access with generous limits:

- **Cost**: Completely free (limited time offer)
- **Limit**: 40 requests per minute (plenty for personal use)
- **Models**: llama-3.3-70b, deepseek-r1, qwen2.5-coder-32b, and more
- **How to get it**:
  1. Visit https://build.nvidia.com/
  2. Sign up with email and phone verification
  3. Click "Get API Key" button
  4. Copy the key (looks like: `nvapi-xxxxx...`)
  5. Paste it in the plugin's Nvidia AI configuration

**2. Ollama (100% Free, No Internet Required)**

Run AI models completely free on your own computer:

- **Cost**: Free forever
- **Privacy**: Everything runs locally, no data sent to internet
- **How to set up**:
  1. Download Ollama from https://ollama.com/
  2. Install it on your computer
  3. Open terminal/command prompt
  4. Run: `ollama pull llama3.2` (or any model you want)
  5. In the plugin, select "Ollama" and use default settings
  6. No API key needed!

**Popular Ollama Models:**
- `llama3.2`
- `mistral` 
- `deepseek-r1` 

**3. Free Tiers from Other Providers**

- **OpenRouter**: Free tier available for some models
- **Google Gemini**: Free tier with 15 requests/minute (get key at https://aistudio.google.com/)

---

### Installation

**Method 1: Install from calibre Plugin Index (Recommended)**

1. In calibre, select "Preferences" -> "Plugins" -> "Get new plugins"
2. Search for "Ask AI" in the search box
3. Select the plugin and click "Install"
4. Restart calibre

**Method 2: Manual Installation**

1. Download the latest version from `https://www.mobileread.com/forums/showthread.php?p=4547077#post4547077`
2. In calibre, select "Preferences" -> "Plugins" -> "Load Plugin from file"
3. Select the downloaded .zip file
4. Restart calibre

---

### Configuring Your First AI

Let's set up Nvidia AI (free option) as an example:

1. Click the "Ask AI Plugin" dropdown menu in calibre toolbar
2. Select "Configure"
3. Find the "Nvidia AI" section
4. Paste your API Key (from https://build.nvidia.com/)
5. The Base URL should already be: `https://integrate.api.nvidia.com/v1`(there is already a default value)
6. Click "Load Model List" button to see available models
7. Select a model (e.g., `meta/llama-3.3-70b-instruct`)(there is already a default value)
8. Click "Save"

You'll see a "Save successful" message. You're ready to use the plugin!

---

## Core Features

### Basic Q&A

**How to ask questions about a book:**

1. Select a book in your calibre library
2. Click the "Ask AI Plugin" button in the toolbar
3. Select your preferred AI from the dropdown
4. Type your question in the input box
5. Click "Send" (or press Cmd/Ctrl + Enter)
6. Wait for the AI's response

**The plugin automatically includes:**
- Book title
- Author name
- Publisher
- Publication date
- Language

You don't need to copy-paste book information!

**Example questions:**
- "What are the main themes in this book?"
- "Is this book suitable for teenagers?"
- "Summarize the plot in 3 sentences"
- "What writing style does the author use?"

---

### Random Question Generator

Not sure what to ask? Let AI suggest questions:

1. Click the "Random Question" button
2. AI will generate relevant questions about the book
3. Click any suggested question to use it
4. Or edit the suggestion and send

**Customize suggestions:**
- Go to Configure -> "Edit Random Question Prompts"
- Modify the prompt template to get different types of questions
- Supports all languages

---

### Multiple Books Support

Ask questions about several books at once:

1. Select multiple books in calibre (Ctrl/Cmd + Click)
2. Click "Ask AI"
3. Ask comparative questions

**Example questions:**
- "Compare the writing styles of these authors"
- "What common themes appear across these books?"
- "Which book should I read first?"
- "How are these books related?"

**Note:** The plugin uses a special template for multi-book queries that you can customize in settings.

---

### Parallel AI Requests

Compare responses from multiple AI providers simultaneously:

**Setup:**
1. Go to Configure
2. Find "Parallel AI Panels" setting
3. Choose 2 panels
4. Set the AI 1 and AI 2 to different AIs
5. Auto save will works.

**Usage:**
1. Open Ask dialog
2. You'll see parallel AI panels (based on your setting)
3. Each panel has its own AI selector
4. Type your question once
5. Click "Send" - all AIs respond at the same time
6. Compare their answers side-by-side

**Tip:** This is great for:
- Comparing free vs paid AI quality
- Getting multiple perspectives
- Fact-checking responses
- Finding the best AI for your needs

---

### AI Switcher

Switch AI providers without closing the dialog:

1. After getting a response, use the dropdown at the top of the response panel
2. Select a different AI
3. Ask another question - it uses the new AI
4. Each response remembers which AI generated it

This makes it easy to try different AIs for the same book without reopening the dialog.

---

### Dynamic Model List Loading

No more typing model names manually:

**How to use:**
1. Go to Configure
2. Select any AI provider
3. Enter your API Key (except Ollama)
4. Click "Load Model List" button
5. Wait a few seconds
6. Select from the dropdown of available models

**Supported providers:**
- OpenAI, Anthropic, Gemini, Grok, DeepSeek, Nvidia, OpenRouter, Custom API

**Fallback:** If you want to use a model not in the list, check "Use custom model name" and type it manually.

---

### History System

All your conversations are saved automatically:

**View history:**
1. Click "History" button in the Ask dialog
2. Browse previous questions and answers
3. Click any history item to view it
4. Use "Clear current book history" to delete

**Features:**
- Organized by book
- Shows which AI was used
- Includes timestamps
- Supports multi-book conversations
- Export to PDF

---

### PDF Export

Save your Q&A sessions as PDF files:

**Export current Q&A:**
1. After getting a response, click "Export PDF" button
2. Choose save location
3. PDF includes book metadata, question, answer, and AI info

**Export all history:**
1. Click "History" button
2. Click "Export All History to PDF"
3. Saves all conversations for the current book(s)

**PDF features:**
- Professional formatting
- Markdown rendering (bold, italic, code blocks, lists)
- Book metadata included
- AI provider and timestamp
- Automatic page breaks

**Configure default export folder:**
- Go to Configure -> Export Settings
- Enable "Use default export folder"
- Browse and select your preferred folder
- All exports will go there automatically

---

## Configuration Options

### General Settings

- **Language**: Choose your preferred interface language (15 languages supported)
- **Dialog Size**: Adjust the default width and height of the Ask dialog
- **Parallel AI Panels**: Set how many AI panels to show (2)

### AI Provider Settings

For each AI provider:
- **API Key**: Your authentication key
- **Base URL**: API endpoint (usually pre-filled)
- **Model**: Select from loaded list or enter custom name
- **Enable Streaming**: Get responses word-by-word as they're generated

### Template Settings

- **Single Book Template**: Customize the prompt format for one book
- **Multi-Book Template**: Customize the prompt format for multiple books
- **Random Question Prompts**: Customize question suggestions

### Export Settings

- **Use Default Export Folder**: Enable to always save PDFs to the same location
- **Default Export Folder**: Choose your preferred save location

---

## Keyboard Shortcuts

- Ask Dialogue: F3
- Config Dialogue: F2
- **Send**: Ctrl/Cmd+Enter
- **Random Question**: Ctrl/Cmd+R
- **Close Dialog**: Esc

---

## Supported Languages

The plugin interface is available in 15 languages:

- Danish (da)
- German (de)
- English (en)
- Spanish (es)
- Finnish (fi)
- French (fr)
- Japanese (ja)
- Dutch (nl)
- Norwegian (no)
- Portuguese (pt)
- Russian (ru)
- Swedish (sv)
- Simplified Chinese (zh)
- Traditional Chinese (zht)
- Cantonese (yue)

Change language in Configure -> Language dropdown.

---

## Troubleshooting

### Common Issues

**"Request Failed" Error**

1. Check your internet connection
2. Verify your API key is correct
3. Make sure you have API credits (for paid services)
4. Try a different AI provider
5. Check the provider's status page

**"API Key Invalid" Error**

- Double-check you copied the entire key
- Make sure there are no extra spaces
- Verify the key hasn't expired
- For Grok, ensure you're using the key from console.x.ai, not x.com

**Ollama Not Working**

1. Make sure Ollama is installed and running
2. Check that you've pulled at least one model: `ollama pull deepseek-r1:1.5b`
3. Try running `ollama list` in terminal to see available models
4. Confirm `ollama serve` is running
5. Confirm `ollama run model-name` is running

**Streaming Responses Stop Mid-Sentence**

- This can happen with network issues
- Try disabling streaming in Configure
- Check your internet stability
- Some providers have rate limits

---

## Privacy and Data Handling

### What Data is Sent

The plugin sends to AI providers:
- Book metadata: title, author, publisher, publication date, language
- Your questions

The plugin does NOT send:
- Your personal calibre tags
- Book comments or reviews
- Your reading progress
- Any other personal data

### API Key Storage

- Your API keys are stored locally in a JSON file on your computer
- Keys are never sent to any third-party servers (except the AI provider you're using)
- The file location: `[calibre config folder]/plugins/ask_ai_plugin.json`

### AI Provider Privacy Policies

Each AI provider has different policies about data usage:

- **Ollama**: 100% local, nothing sent to internet
- **Others**: Review each provider's privacy policy

**Recommendation**: For sensitive books, use Ollama (local AI) for complete privacy.

---

## Tips and Best Practices

### Getting Better Responses

1. **Ask Training Data**: Ask AI if this book in AI's training data, if not, just reply no. 
2. **Compare AIs**: Use parallel panels to see which AI gives better answers for your needs

---

## Recent Updates

### v1.3.3 (November 20, 2025)
- Improved PDF filename format with book titles
- Real-time export folder configuration
- Export success feedback tooltips
- Enhanced PDF layout with cleaner separators
- Fixed language switching in export configuration
- Fixed parallel AI display issues

### v1.3.2 (November 17, 2025)
- Added OpenAI, Anthropic, Nvidia AI support
- Dynamic model list loading
- AI switcher in response panel
- PDF export features
- Multiple books support
- Parallel AI requests (1-4 panels)
- Plugin renamed to Ask AI Plugin
- Enhanced history system
- UI/UX improvements

---

## Getting Help

### Resources

- **GitHub Repository**: https://github.com/sheldonrrr/ask_grok
- **Issue Tracker**: Report bugs on GitHub Issues
- **calibre Forum**: https://www.mobileread.com/forums/showthread.php?p=4547077#post4547077

### Contact

- **Email**: sheldonrrr@gmail.com
- **iMessage**: sheldonrrr@gmail.com

---

## Frequently Asked Questions

**Q: Why do I need an API key if I already pay for ChatGPT Plus?**

A: Consumer subscriptions (ChatGPT Plus, Gemini Advanced, etc.) are separate from API access. The plugin needs API keys to work. See "Understanding API Keys" section above.

**Q: Are there any completely free options?**

A: Yes! Nvidia offers free API access (40 requests/minute), and Ollama is 100% free and runs locally on your computer.

**Q: Can I use this plugin offline?**

A: Yes, if you use Ollama. All other providers require internet connection.

**Q: How much does API access cost?**

A: It varies:
- Nvidia: FREE
- Ollama: FREE
- Others: Depends on the provider

**Q: What's a "token"?**

A: Roughly 4 characters or 0.75 words. A typical question and answer might use 500-2000 tokens. Most providers give you free credits to start.

**Q: Can I use multiple API keys from the same provider?**

A: No, but you can switch keys in the configuration anytime.

**Q: Can I ask questions about book content?**

A: The plugin sends only metadata, not the actual book text. The AI answers based on its training data about the book. For specific passages, you'd need to copy-paste them into your question.

**Q: Is my reading data shared with AI companies?**

A: Only the book metadata you query about is sent. Your full library, reading history, and personal notes stay private.

**Q: Can I customize the AI's personality or tone?**

A: Yes, edit the template in Configure to add instructions like "Answer in a friendly tone" or "Be concise".

**Q: Why is Ollama slower than cloud AIs?**

A: Ollama runs on your computer's hardware. Cloud AIs use powerful servers. But Ollama is free and private!

**Q: Can I use this for academic research?**

A: Yes, but remember AI responses should be verified. Always cite original sources, not AI summaries.

---

**Thank you for using Ask AI Plugin!**

If you find this plugin helpful, please:
- Star the GitHub repository
- Leave a review on calibre Plugin Index
- Share with fellow book lovers
- Report bugs to help improve it

Happy reading! 
