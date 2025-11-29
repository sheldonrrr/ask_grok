# Ask Grok User Manual v0.2

*Ask Grok Version: 1.2.3, Updated: Wed Sep 3, 2025* 

**Note:** If the version number you see in your plugin is behind the current user manual version (v1.2.1), please upgrade the plugin to access more powerful features.

### YouTube Tutorial

*[YouTube Tutorial for v1.1.19, start to use Ask Grok Plugin step by step](https://youtu.be/QdeZgkT1fpw)*

### Getting Started

Before using Ask Grok, please ensure:

- You have downloaded and installed [calibre](https://calibre-ebook.com/)
- You have obtained a valid API Key from:
	- [Grok(x.AI)](https://console.x.ai/), such as `xai-******W1IyTUlomJq9******gzEmuvhW8tqyEyr8enZ6xjUEeqePspDdopCwtRLARlkVLU6PLKU*****`
	- [Google Gemini](https://aistudio.google.com/), such as `AIzaSy***-knmtsdgA******_yi21Nv5K******`
	- [DeepSeek](https://platform.deepseek.com/), such as `sk-******7086ea49f78c8904f37b******`
	- Custom (Local LLM like using [Ollama](https://ollama.com/)) –- No API key strictly needed, as it runs locally. Ensure Ollama is installed and a model is running on your system.
	- Free API Key for 6 months, from [Nvidia Build](https://build.nvidia.com/), you can find `Free API Key` section in this page.

For more details on obtaining API keys:  
- For Grok: Go to https://console.x.ai/, create a team if needed, navigate to API Keys, click Create API Keys, name it (e.g., calibre_Ask_Grok), save, and copy the generated Key value (e.g., Bearer x-ai ***** or x-ai *****).  
- For Google Gemini: Visit the [Google AI Studio](https://aistudio.google.com/) or Google Cloud Console to generate your API key.  
- For DeepSeek: Obtain your API key from the [DeepSeek Platform](https://platform.deepseek.com/) .  
- For Ollama (Local AI): Configure the local server endpoint if needed.

**Note on API Keys vs. Consumer Subscriptions:**  
AI providers often separate their services into two types: subscriptions for regular users (toC, or "to Consumer") like chatting on their website or app, and API Keys for developers or tools (toB, or "to Business") like this plugin. Even if you've paid for a subscription (e.g., SuperGrok or Gemini Pro), you usually need a separate API Key for programmatic access, and it might come with its own usage-based fees (e.g., per query or word count).  
- **Why the difference?** Subscriptions cover casual use with simple limits, but API Keys let you build or integrate into apps like Ask Grok, so companies charge extra to handle the higher demands and costs. For example:  
  - x.AI (Grok): Your SuperGrok sub works for direct chatting, but API calls need credits—check the x.AI console for API billing details.  
  - Google Gemini: A sub gives app access, but API use via AI Studio or Cloud Console requires a key and may add Google Cloud charges (often with a free tier).  
  - DeepSeek: Similar setup—grab a key from their platform and watch for pay-per-use pricing.  
  - Ollama: It's all local, so no fees—just runs on your own computer.  
If you're still confused, check the provider's developer docs or contact the plugin's author to figure out why.

### Installation

**1. Install from calibre Plugin Index (Recommended)**

Ask Grok is now available in the official calibre Plugin Index:

1. In calibre, select "Preferences" -> "Plugins" -> "Get new plugins" ↡
2. Search for "Ask Grok" in the search box ↡
3. Select the plugin and click "Install" ↡
4. After installation, restart calibre

**2. Manual Installation**

Alternatively, you can download the latest version from the [releases page](https://github.com/sheldonrrr/ask_grok/releases).  
Import the file to calibre custom plugins:

1. In calibre, select "Preferences" -> "Plugins" -> "Load Plugin from file" ↡
2. Select the downloaded plugin file to install ↡
3. After installation, restart calibre

### Configuring the API Key and AI Models in the Plugin

To set up the Token and select your AI model in the Ask Grok plugin:

- Click the Ask Grok dropdown menu in the toolbar, then select Configure ↡
- Select your desired AI Model (e.g., Grok, Gemini, DeepSeek, Ollama) ↡
- Paste your API Key (if applicable) into the relevant input box (e.g., X.AI Authorization Token for Grok) ↡
- For Ollama, you might configure the local server endpoint ↡
- Customize other settings like Edit Random Question Prompts or Enable Streaming Config ↡
- Click Save ↡

You’ll see a Save successful message. At this point, Ask Grok is successfully installed on your computer. Next, let’s explore all the features of this plugin.

### Free API Key

Recently, Nvidia released a free API key for llama, Deepseek-r1, you can get a free API key from [here](https://build.nvidia.com/).

**Available models:**

- meta/llama-4-maverick-17b-128e-instruct,
- meta/llama-4-scout-17b-16e-instruct
- meta/llama-3.3-70b-instruct
- deepseek-ai/deepseek-r1
- qwen/qwen2.5-coder-32b-instruct

**Base URL:**

`https://integrate.api.nvidia.com/v1`

**API Key:**

After logging in and validating through your phone number, you can generate an API Key to use. Now the only limit is the rate limit, just limited to 40 RPM.(If you are using it for personal use, there is almost no limit.)

### Features

- Ask questions about books with AI directly in calibre  
- Configurable API key for various AI models: Grok, Google Gemini, and DeepSeek  
- Support for Ollama (Local AI) for private and local AI interactions  
- Automatically includes the current book's metadata (title, author, publisher) - no copy-paste needed  
- Simple single input-output dialog interface  
- Customizable prompt template  
- Preview-able interface shortcuts  
- Check plugin version info in the interface  
- New! Edit Random Question Prompts: Customize the AI-generated question ideas.  
- New! Enable Streaming Config for every AI: Choose whether to receive AI responses as they are generated for a more interactive experience.  
- Enhanced Internationalization: Extensive interface text has been added for a more globally friendly experience.  

### Q&A Features

- Automatically select book metadata and create custom questions to evaluate a book using AI - [GIF Preview with my Dropbox Share](https://www.dropbox.com/scl/fi/qxgdedbat3218xn6vpjwh/Answer_out.gif?rlkey=hiwoqvo69iapv83zfrc9rb37s&st=wis1cgsu&dl=0)
- Generate random questions with AI and review the AI’s responses - [GIF Preview with my Dropbox Share](https://www.dropbox.com/scl/fi/tlsf4hpysx5d5irecxr3q/Random_Question.gif?rlkey=47khau6l2k9x5svkzy6j7im41&st=vuq330df&dl=0)

### How to Use the Plugin

1. Select a book in your calibre library.  
2. Click the Ask Grok button in the toolbar.  
3. Select your preferred AI model from the dropdown.  
4. Enter your question in the popup dialog.  
5. Click Send to get the AI’s answer.  
6. Click Random Question to see AI-generated question ideas.  
7. Utilize the Edit Random Question Prompts option in configurations to customize these suggestions.  

**Shortcuts**  
- Send: Command + Enter  

### Supported Languages

Danish (da), German (de), English (en), Spanish (es), Finnish (fi), French (fr), Japanese (ja), Dutch (nl), Norwegian (no), Portuguese (pt), Russian (ru), Swedish (sv), Simplified Chinese (zh), Traditional Chinese (zht), Cantonese (yue)

### Troubleshooting

If you keep encountering Request Failed or other usability issues, please completely remove and reinstall the latest version of the plugin.

To thoroughly delete Ask Grok's local configuration files and plugin folder:

- Calibre Preferences  ↡
- Select Miscellaneous  ↡
- Click Open calibre configuration folder (Button)  ↡
- Open the Plugins folder  ↡
- Delete all items with `ask_grok` as the prefix  ↡
- Install the latest version of the plugin  ↡
- Restart calibre

### Recent Updates

**v1.2.0 New Features:**  
- AI: Google Gemini Supported  
- AI: Ollama Local AI Supported  
- AI: DeepSeek Supported  

**v1.2.1 Fixes:**  
- The Random Question button is now correctly triggered when the Grok model is selected.  
- Results returned by Gemini and Grok models are no longer truncated.  
- Extensive internationalization interface text has been added for better user experience.

**v1.2.2 Fixes:**  
- The Random Question button is now correctly triggered when the DeepSeek model is selected.  

### Privacy Handling

The plugin sends book metadata (title, author, publisher, publish time, language) to the selected AI model but excludes user-defined data like Tags or Comments.  
Your AI API Key (Grok, Gemini, DeepSeek) is stored locally in a JSON file and isn’t sent to any third-party server.  
Uses Python’s requests module for external API calls; no third-party servers are involved in data processing by the plugin itself beyond direct API calls to your chosen AI provider.  
The privacy policy of each AI model (Grok, Gemini, DeepSeek) regarding data usage for model training may vary. Please consult their respective official statements.  

※

_READ_

- [Ask Grok - A Book AI Plugin in calibre](http://simp.ly/publish/xYW5Tr)

_DOWNLOAD_

- [Download on GitHub Latest Release](https://github.com/sheldonrrr/ask_grok/releases)

_SUPPORT AUTHOR_

- iMessage for Hi: [imessage://sheldonrrr@gmail.com](imessage://sheldonrrr@gmail.com)
- Email: [sheldonrrr@gmail.com](mailto:sheldonrrr@gmail.com)
- Star GitHub Repo: [https://github.com/sheldonrrr/ask_grok](https://github.com/sheldonrrr/ask_grok)
- calibre forum: [https://www.mobileread.com/forums/showthread.php?p=4503254#post4503254](https://www.mobileread.com/forums/showthread.php?p=4503254#post4503254)