
# Ask AI Plugin User Manual v0.9
Latest updated: Jul 1, 2026, Ask AI Plugin v1.4.7

ToC of this tutorial:
- Explain: Why & What is API Keys
- Free API Key Options
- Installation
- First Time Setup an AI Service
- How to Use
- AI Search
- Keyboard Shortcuts
- Random Questions
- Prompts
- Other Features
- Configuration
- Custom Prompt Length (New)
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

**Default Option: Nvidia AI Free (No Setup Required)**
- Cost: Completely FREE
- Setup: None! Works immediately after plugin installation
- Limit: Shared free tier (may be less stable during peak times)
- Note: This is a free service maintained by the plugin developer. For better stability and higher limits, consider the options below.

Option 1: Nvidia (Recommended for Stability)
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
3. Search for "Ask AI" (Author: Sheldon)
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
   - Use the global shortcut (default: Ctrl+K)
3. Type your question
4. Click Send (or use Ctrl+Enter / Cmd+Enter)

The plugin automatically includes book metadata. You don't need to type title or author.

### Perplexity (Sonar) for Research

Perplexity is useful when you want answers with sources.

When Perplexity returns citations/search results, the plugin appends a plain-text "Citations" / "Search Results" section (with full URLs) at the end of the answer, so you can copy/paste the links.

## AI Search

AI Search lets you search your entire library using natural language, without selecting any books first.

### How to Use AI Search

**Open AI Search**:
- Click "AI Search" in the plugin menu, or
- Use the shortcut Ctrl+Shift+L, or
- Simply open the Ask dialog without selecting any books

**Ask questions about your library**:
- "Do you have any books about Python programming?"
- "Show me books by Isaac Asimov"
- "Find books about machine learning"
- "What science fiction books do I have?"

**Open the book in response**

AI will search through your library metadata and recommend relevant books, and you can open the book in response by clicking the book title.

**Update your library index** (recommended):
- Open Configuration -> Search tab
- Click "Update Library Data" to index titles and authors for **all books** in your library
- Run this again after adding or removing books

### Features

- **Natural Language Search**: Ask in plain language, no special syntax needed
- **Library-Wide**: Indexes and searches your full calibre library (compact metadata: book ID, title, author)
- **Smart Matching**: AI understands context and can find related books
- **Click to Open**: Click on book titles in the results to open them directly
- **Large Selection Helper**: If you select more than 50 books, Ask suggests AI Search instead of stuffing verbose metadata into the prompt

### Tips for AI Search

- Be specific about what you're looking for
- You can ask about genres, authors, topics, or any metadata
- AI Search works best with well-organized library metadata
- For library-wide discovery, use AI Search — do not select thousands of books manually
- For comparing a few books in depth, select up to about 30 books instead

## Keyboard Shortcuts

This plugin supports full shortcut customization via calibre.

How to customize:
1. Open calibre
2. Go to Preferences -> Shortcuts
3. Search for "Ask AI"
4. Edit the shortcuts you want

Common shortcuts (defaults):
- Ask AI: Ask (global): Ctrl+K
- Ask AI: Open Configuration: F2
- Ask AI: AI Search: Ctrl+Shift+L
- Ask AI: Send (in dialog): Ctrl+Enter (Cmd+Enter on macOS)
- Ask AI: Random Question (in dialog): Ctrl+Shift+R (Cmd+Shift+R on macOS)

Note: If you customized shortcuts in calibre, your custom settings take precedence.

## Random Questions

1. Click Random Question button (or Ctrl+Shift+R / Cmd+Shift+R)
2. AI suggests a question

Customize prompts in Configuration -> Prompts Tab -> Random Question Prompts

## Prompts

The Prompts Tab (accessible via toolbar menu or Configuration) lets you customize how the plugin communicates with AI.

### Persona

Define your research background and goals. This text is prepended to every prompt sent to AI.

Example personas:
- "As a literature professor, I focus on narrative techniques and literary analysis."
- "I'm researching 19th century European history, especially political movements."
- "As a student, I want simple explanations suitable for beginners."

The more specific your persona, the more relevant AI responses will be.

Tips:
- Include your field of study or profession
- Mention your expertise level (beginner, expert, etc.)
- Describe what aspects you care about most

### Prompt Templates

Three customizable templates:

1. **Single Book Prompt**: Used when asking about one book
   - Available variables: {title}, {author}, {publisher}, {pubyear}, {language}, {series}, {query}

2. **Multi-Book Prompt**: Used when asking about multiple selected books
   - Available variables: {books_metadata}, {query}

3. **Random Question Prompt**: Used when generating random questions
   - Available variables: {title}, {author}, {language}

### Use Interface Language

When enabled, the plugin adds an instruction asking AI to respond in your current plugin language. Useful if you want responses in a specific language regardless of the book's language.

### Reset to Default

Click "Reset Prompts to Default" to restore all prompts and settings to their original values.

## Other Features

- Parallel AI Comparison: Set Parallel AI Panels to 2 in Configuration, then compare responses from different AIs side-by-side
- History: Auto-saved conversations, click History button to view past Q&A
- PDF Export: Click Export PDF to save conversations, set default folder in Configuration -> Export Settings

## Configuration

General Settings:
- Language Change
- Dialog Size: Adjust window size
- Parallel AI Panels: Set to 2 for side-by-side comparison
- Request Timeout: How long to wait for an AI response
- Custom Prompt Length: Optional advanced limit (see chapter below)

AI Provider Settings:
- API Key: Your authentication key
- Base URL: Usually pre-filled
- Model: Select from dropdown or enter custom
- Enable Streaming: Get responses word-by-word

Search Tab:
- AI Search overview, privacy notice, and **Update Library Data** (full-library index)

Prompts Tab (separate tab for better management):
- Persona: Define your research background and goals to help AI provide more relevant responses
- Customize prompts for single book, multiple books, or random questions
- Use Interface Language: Ask AI to respond in your plugin language

Export Settings:
- Set default PDF save location

## Custom Prompt Length (New)

The plugin limits how much text is sent to the AI in a single request. This protects against timeouts and confusing errors when a prompt grows too large.

### Default limits (most users)

You do **not** need to change anything unless you hit a limit or use a large-context local model.

| Mode | Default limit |
|------|----------------|
| Single book | 128,000 characters |
| Multi-book (selected titles) | 256,000 characters |
| AI Search (full library index) | Uses compact format; see Search tab |

If the prompt is too long, the plugin shows a detailed message with the current size, the limit, and how many books were selected — plus guidance to use **AI Search** for library-wide questions.

### When to use a custom limit

Enable this only if you know your model supports a larger context window — for example **Ollama** with `num_ctx` set to 128k on the model side.

**Do not** select thousands of books manually and raise the limit to “make it fit.” Use **AI Search** instead. Custom limits are an advanced fallback, not the main way to search a large library.

### How to enable

1. Open Configuration -> **General**
2. Check **Custom prompt length limit**
3. Enter **Max prompt length** in characters (default suggestion: 524288)
4. Click **Save**

Rough guide: 1 token ≈ 3–4 characters. For Ollama, also configure `num_ctx` in your model settings.

### Multi-book behavior

- **Up to 30 books**: verbose metadata (title, author, publisher, etc.) for deeper comparison
- **More than 30 books**: compact one-line metadata per book
- **More than 50 books**: Ask offers to switch to **AI Search** automatically

## Troubleshooting

Question Too Long / Prompt Too Long:
- For library-wide questions: use **AI Search** (no books selected) or accept the switch when selecting 50+ books
- For multi-book comparison: up to 30 books use detailed metadata; larger selections switch to compact format automatically
- Very large libraries may truncate the index at the prompt limit — enable **Custom prompt length limit** in General if needed (suggested: 524288)
- Read the error message — it shows current length, limit, and suggested actions

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
- Your persona (if enabled)
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
4. Set up a detailed persona for more relevant responses.
5. Use Perplexity for research questions that need citations.
6. Use AI Search to quickly find books in your library without browsing.
7. If you see "Question too long", switch to AI Search, use compact mode (30+ books), or raise the custom limit for very large libraries.

## Getting Help

GitHub: https://github.com/sheldonrrr/ask_grok
calibre Forum: https://www.mobileread.com/forums/showthread.php?p=4547077
Email: sheldonrrr@gmail.com

