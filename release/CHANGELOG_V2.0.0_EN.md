# Ask AI Plugin - Version 2.0.0 Release Notes

[b]Changes (v2.0.0)[/b]
[list]
[*]The provider is now labeled SpaceXSI. A new SpaceXSI setup starts on grok-4.7. A model name you already saved is left as-is.
[*]A new DeepSeek setup starts on deepseek-flash. A DeepSeek model name you already saved is left as-is.
[*]A bad SpaceXSI API key is shown as an invalid key. If a request fails on the network, the message asks you to check your network, proxy, and firewall, and says the key may be invalid — try again with a key you know works. This wording is included in every language the plugin ships.
[*]Opening Ask is less likely to leave the pointer stuck as a busy cursor. The plugin clears a leftover wait cursor and restores the normal arrow. On Fedora the spinner can still finish its short animation; that comes from the desktop.
[*]The model list in the Ask window uses the same provider name as Settings, so SpaceXSI shows up even when an older display name is still stored. Saved model ids are not changed.
[*]A brand-new setup uses the current recommended models. Configs you already saved are not changed for you: OpenAI gpt-6.1-sol, Anthropic claude-opus-5-5, Gemini gemini-3.8-flash, Mistral mistral-large-4, and OpenRouter x-ai/grok-4.7. Left as they were: Kimi kimi-k3, Nvidia (your own key) nvidia/nemotron-3-nano-30b-a3b, Nvidia Free nvidia/nemotron-3.5-lightning-30b-a3b, and Perplexity sonar-pro.
[*]Questions sent to GPT-6 and Claude Opus 5 no longer include a temperature setting, because those models reject it. Older models can still use temperature.
[/list]

---

## GitHub Release Notes (v2.0.0)

### Changes
- The provider is now labeled SpaceXSI. A new SpaceXSI setup starts on grok-4.7. A model name you already saved is left as-is.
- A new DeepSeek setup starts on deepseek-flash. A DeepSeek model name you already saved is left as-is.
- A bad SpaceXSI API key is shown as an invalid key. If a request fails on the network, the message asks you to check your network, proxy, and firewall, and says the key may be invalid — try again with a key you know works. This wording is included in every language the plugin ships.
- Opening Ask is less likely to leave the pointer stuck as a busy cursor. The plugin clears a leftover wait cursor and restores the normal arrow. On Fedora the spinner can still finish its short animation; that comes from the desktop.
- The model list in the Ask window uses the same provider name as Settings, so SpaceXSI shows up even when an older display name is still stored. Saved model ids are not changed.
- A brand-new setup uses the current recommended models. Configs you already saved are not changed for you: OpenAI gpt-6.1-sol, Anthropic claude-opus-5-5, Gemini gemini-3.8-flash, Mistral mistral-large-4, and OpenRouter x-ai/grok-4.7. Left as they were: Kimi kimi-k3, Nvidia (your own key) nvidia/nemotron-3-nano-30b-a3b, Nvidia Free nvidia/nemotron-3.5-lightning-30b-a3b, and Perplexity sonar-pro.
- Questions sent to GPT-6 and Claude Opus 5 no longer include a temperature setting, because those models reject it. Older models can still use temperature.
