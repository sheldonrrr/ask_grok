# Bug Fix - 2025.10.21 Night

## Issue 1: New AI Providers Not Appearing in Dropdown

After implementing three new AI providers (OpenAI, Anthropic, Nvidia), they were not appearing in the configuration dialog's AI model dropdown list.

### Root Cause

The `model_mapping` dictionary in `config.py` was hardcoded with only the original four providers:
- Grok
- Gemini  
- DeepSeek
- Custom

The new providers were added to the backend (`models/base.py`, `config.py` defaults) but not to the UI dropdown population logic.

---

## Issue 2: No Configuration UI for New Providers

After fixing Issue 1, the new providers appeared in the dropdown, but when selected, no configuration interface was displayed (no API Key input, Base URL, Model name, streaming checkbox, etc.).

### Root Cause

The `ModelConfigWidget` class had hardcoded logic to only handle the original four providers in two methods:
1. `setup_ui()` method (lines 192-205) - Only created UI widgets for grok/gemini/deepseek/custom
2. `get_config()` method (lines 290-307) - Only saved config for grok/gemini/deepseek/custom

When a new provider was selected, `model_config` remained `None`, causing the entire configuration UI block to be skipped.

## Affected Code Locations

### Issue 1: Dropdown Population

Two locations in `/config.py` had the same issue:

**Location 1:** Line 561-568 (Initial dropdown setup)
```python
model_mapping = {
    AIProvider.AI_GROK: 'grok',
    AIProvider.AI_GEMINI: 'gemini',
    AIProvider.AI_DEEPSEEK: 'deepseek',
    AIProvider.AI_CUSTOM: 'custom'
    # Missing: OpenAI, Anthropic, Nvidia
}
```

**Location 2:** Line 819-827 (Dropdown refresh on language change)
```python
model_mapping = {
    AIProvider.AI_GROK: 'grok',
    AIProvider.AI_GEMINI: 'gemini',
    AIProvider.AI_DEEPSEEK: 'deepseek',
    AIProvider.AI_CUSTOM: 'custom'
    # Missing: OpenAI, Anthropic, Nvidia
}
```

### Issue 2: Configuration Widget

Two locations in `/config.py` `ModelConfigWidget` class:

**Location 3:** Line 192-213 (`setup_ui()` method - Provider detection)
```python
# Only handled grok, gemini, deepseek, custom
if self.model_id == 'grok':
    provider = AIProvider.AI_GROK
    # ...
elif self.model_id == 'custom':
    provider = AIProvider.AI_CUSTOM
    # Missing: openai, anthropic, nvidia
```

**Location 4:** Line 299-327 (`get_config()` method - Config saving)
```python
# Only handled grok, gemini, deepseek, custom
if self.model_id == 'grok':
    provider = AIProvider.AI_GROK
    # ...
elif self.model_id == 'custom':
    provider = AIProvider.AI_CUSTOM
    # Missing: openai, anthropic, nvidia
```

## Fixes Applied

### Fix 1: Dropdown Population

Added the three new providers to both `model_mapping` dictionaries:

```python
model_mapping = {
    AIProvider.AI_GROK: 'grok',
    AIProvider.AI_GEMINI: 'gemini',
    AIProvider.AI_DEEPSEEK: 'deepseek',
    AIProvider.AI_CUSTOM: 'custom',
    AIProvider.AI_OPENAI: 'openai',        # ADDED
    AIProvider.AI_ANTHROPIC: 'anthropic',  # ADDED
    AIProvider.AI_NVIDIA: 'nvidia'         # ADDED
}
```

### Fix 2: Configuration Widget UI

Added the three new providers to both conditional blocks in `ModelConfigWidget`:

**In `setup_ui()` method (lines 205-213):**
```python
elif self.model_id == 'openai':
    provider = AIProvider.AI_OPENAI
    model_config = get_current_model_config(provider)
elif self.model_id == 'anthropic':
    provider = AIProvider.AI_ANTHROPIC
    model_config = get_current_model_config(provider)
elif self.model_id == 'nvidia':
    provider = AIProvider.AI_NVIDIA
    model_config = get_current_model_config(provider)
```

**In `get_config()` method (lines 316-327):**
```python
elif self.model_id == 'openai':
    provider = AIProvider.AI_OPENAI
    config['api_key'] = self.api_key_edit.toPlainText().strip()
    config['display_name'] = 'OpenAI'
elif self.model_id == 'anthropic':
    provider = AIProvider.AI_ANTHROPIC
    config['api_key'] = self.api_key_edit.toPlainText().strip()
    config['display_name'] = 'Anthropic (Claude)'
elif self.model_id == 'nvidia':
    provider = AIProvider.AI_NVIDIA
    config['api_key'] = self.api_key_edit.toPlainText().strip()
    config['display_name'] = 'Nvidia AI (Free)'
```

## Files Modified

- `/config.py` - Updated 5 locations:
  - Two `model_mapping` dictionaries (lines 561-568 and 819-827)
  - `ModelConfigWidget.setup_ui()` method (lines 205-213)
  - `ModelConfigWidget.get_config()` method (lines 316-327)
  - Factory registration (lines 504-510)

- `/api.py` - Updated 1 location:
  - `_MODEL_TO_PROVIDER` dictionary (lines 40-48)

## Testing

After all three fixes:
1. Rebuild plugin with `cali-dag`
2. Open Calibre configuration dialog
3. **Verify all 7 AI providers appear in dropdown:**
   - x.AI (Grok)
   - Google Gemini
   - Deepseek
   - Custom
   - OpenAI ✅ NEW
   - Anthropic (Claude) ✅ NEW
   - Nvidia AI (Free) ✅ NEW

4. **Verify configuration UI appears for each provider:**
   - Select OpenAI → Should show: API Key input, Base URL, Model name, Enable Streaming checkbox
   - Select Anthropic → Should show: API Key input, Base URL, Model name, Enable Streaming checkbox
   - Select Nvidia → Should show: API Key input, Base URL, Model name, Enable Streaming checkbox

5. **Verify default values:**
   - OpenAI: Base URL = `https://api.openai.com/v1`, Model = `gpt-4o-mini`
   - Anthropic: Base URL = `https://api.anthropic.com/v1`, Model = `claude-3-5-sonnet-20241022`
   - Nvidia: Base URL = `https://integrate.api.nvidia.com/v1`, Model = `meta/llama-3.3-70b-instruct`

6. **Verify API requests work:**
   - Configure OpenAI with valid API key
   - Send a chat request (streaming) → Should use OpenAI API
   - Click "Random Question" button (non-streaming) → Should use OpenAI API
   - Repeat for Anthropic and Nvidia
   - Check logs to verify correct provider is being used

---

## Issue 3: API Request Routing Not Working for New Providers

After fixing the UI, when users actually try to send requests (either streaming chat or non-streaming random questions), the new providers would fail because the API routing logic didn't recognize them.

### Root Cause

Two more locations had hardcoded mappings for only the original four providers:

1. **`api.py`** - `_MODEL_TO_PROVIDER` dictionary (line 40-45) only mapped grok/gemini/deepseek/custom
2. **`config.py`** - Factory registration (line 504-507) only registered grok/gemini/deepseek/custom

When a request was made with a new provider:
- `_get_provider_from_model_name()` would return `DEFAULT_PROVIDER` (Grok) instead of the correct provider
- Factory might not have the model class registered
- Requests would fail or use wrong API endpoints

### Fix 3: API Request Routing

**In `api.py` (lines 40-48):**
```python
_MODEL_TO_PROVIDER = {
    'grok': AIProvider.AI_GROK,
    'gemini': AIProvider.AI_GEMINI,
    'deepseek': AIProvider.AI_DEEPSEEK,
    'custom': AIProvider.AI_CUSTOM,
    'openai': AIProvider.AI_OPENAI,      # ADDED
    'anthropic': AIProvider.AI_ANTHROPIC, # ADDED
    'nvidia': AIProvider.AI_NVIDIA        # ADDED
}
```

**In `config.py` (lines 504-510):**
```python
AIModelFactory.register_model('openai', OpenAIModel)
AIModelFactory.register_model('anthropic', AnthropicModel)
AIModelFactory.register_model('nvidia', NvidiaModel)
```

Note: Factory registration in `config.py` is redundant (already done in `models/__init__.py`) but kept for consistency.

---

## Status

- [x] Issue 1 identified (dropdown)
- [x] Issue 1 fixed
- [x] Issue 2 identified (config UI)
- [x] Issue 2 fixed
- [x] Issue 3 identified (API routing)
- [x] Issue 3 fixed
- [x] All syntax validated
- [ ] Testing pending (rebuild required)

## Related Documents

- [IMPLEMENTATION_SUMMARY_2025.10.21.md](./IMPLEMENTATION_SUMMARY_2025.10.21.md) - Original implementation
- [DEV_PLAN_2025.10.21_night.md](./DEV_PLAN_2025.10.21_night.md) - Development plan

---

**Fixed:** 2025.10.21 Night  
**Next Step:** Rebuild plugin and verify all providers appear in UI
