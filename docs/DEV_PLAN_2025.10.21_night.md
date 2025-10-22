# Development Plan - 2025.10.21 Night

## Overview

This development plan focuses on enhancing the Ask Grok Calibre plugin with three major features:
1. **Dynamic Model List Loading** - Load available models from AI providers instead of manual input
2. **Add OpenAI and Anthropic Support** - Integrate two mainstream AI providers
3. **Add Nvidia AI Support** - Integrate Nvidia's free API service

---

## Feature 1: Dynamic Model List Loading

### Current Problem
- All model names rely on user manual input
- Users often make typos causing API errors
- No validation of model availability
- Poor user experience

### Proposed Solution
Implement automatic model list fetching from AI provider APIs with dropdown selection in config dialog.

### Technical Approach

#### 1.1 Add Model List API Support to Base Class

**File:** `models/base.py`

**Changes:**
```python
class BaseAIModel(ABC):
    # Add new abstract method
    @abstractmethod
    def fetch_available_models(self) -> list:
        """
        Fetch available models from AI provider
        Returns: List of model names
        """
        pass
    
    def supports_model_list_api(self) -> bool:
        """
        Check if provider supports model list API
        Returns: True if supported
        """
        return True
```

#### 1.2 Implement for Each Provider

**OpenAI-Compatible Providers** (Grok, DeepSeek, Nvidia, Custom):
- Endpoint: `GET {base_url}/models`
- Headers: `Authorization: Bearer {api_key}`
- Response parsing: Extract `data[].id`

**Gemini:**
- Endpoint: `GET {base_url}/models`
- URL param: `key={api_key}`
- Response parsing: Extract `models[].name`

**Anthropic:**
- Endpoint: `GET {base_url}/models`
- Headers: `x-api-key: {api_key}`, `anthropic-version: 2023-06-01`
- Response parsing: Extract `data[].id`

#### 1.3 Update Config Dialog UI

**File:** `config.py`

**Changes:**
- Replace model name `QLineEdit` with `QComboBox`
- Add "Refresh Models" button next to dropdown
- Show loading indicator while fetching
- Handle API errors gracefully
- Keep manual input option as fallback

**UI Layout:**
```
Model: [Dropdown ▼] [🔄 Refresh]
```

#### 1.4 Implementation Steps

1. Add `fetch_available_models()` to `BaseAIModel`
2. Implement for each provider:
   - `GrokModel.fetch_available_models()`
   - `GeminiModel.fetch_available_models()`
   - `DeepseekModel.fetch_available_models()`
   - `CustomModel.fetch_available_models()`
3. Update `ConfigDialog` to use `QComboBox`
4. Add refresh button with click handler
5. Add error handling and user feedback
6. Test with all providers

---

## Feature 2: Add OpenAI Support

### Why OpenAI
- Most popular AI provider
- Industry standard API format
- Wide model selection (GPT-4, GPT-3.5, etc.)
- Many users already have API keys

### Implementation

#### 2.1 Add to AIProvider Enum

**File:** `models/base.py`

```python
class AIProvider(Enum):
    AI_GROK = auto()
    AI_GEMINI = auto()
    AI_DEEPSEEK = auto()
    AI_CUSTOM = auto()
    AI_OPENAI = auto()      # NEW
    AI_ANTHROPIC = auto()   # NEW (Feature 3)
    AI_NVIDIA = auto()      # NEW (Feature 4)
```

#### 2.2 Add Default Configuration

**File:** `models/base.py`

```python
DEFAULT_MODELS = {
    # ... existing ...
    AIProvider.AI_OPENAI: ModelConfig(
        provider=AIProvider.AI_OPENAI,
        display_name="OpenAI",
        api_key_label="OpenAI API Key:",
        default_api_base_url="https://api.openai.com/v1",
        default_model_name="gpt-4o-mini"
    ),
}
```

#### 2.3 Create OpenAI Model Class

**File:** `models/openai.py` (NEW)

**Reference:** `aiprovider/openai_compatible.md`

**Key Features:**
- Endpoint: `{base_url}/chat/completions`
- Headers: `Authorization: Bearer {api_key}`
- Streaming support
- Model list API: `GET {base_url}/models`

**Implementation Structure:**
```python
class OpenAIModel(BaseAIModel):
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
    
    def prepare_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }
    
    def prepare_request_data(self, prompt, **kwargs):
        return {
            "model": self.config.get('model'),
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
    
    def fetch_available_models(self):
        # GET {base_url}/models
        # Parse response.data[].id
        pass
```

#### 2.4 Update Config and Factory

**Files:** `config.py`, `models/base.py`

- Add OpenAI to config defaults
- Register in `AIModelFactory`
- Add UI tab in `ConfigDialog`

#### 2.5 Implementation Steps

1. Create `models/openai.py`
2. Implement `OpenAIModel` class
3. Add to `AIProvider` enum
4. Add to `DEFAULT_MODELS`
5. Register in factory
6. Add config UI tab
7. Test with OpenAI API key

---

## Feature 3: Add Anthropic (Claude) Support

### Why Anthropic
- High-quality Claude models
- Strong reasoning capabilities
- Growing user base
- Competitive pricing

### Implementation

#### 3.1 Add to Configuration

**File:** `models/base.py`

```python
DEFAULT_MODELS = {
    # ... existing ...
    AIProvider.AI_ANTHROPIC: ModelConfig(
        provider=AIProvider.AI_ANTHROPIC,
        display_name="Anthropic (Claude)",
        api_key_label="Anthropic API Key:",
        default_api_base_url="https://api.anthropic.com/v1",
        default_model_name="claude-3-5-sonnet-20241022"
    ),
}
```

#### 3.2 Create Anthropic Model Class

**File:** `models/anthropic.py` (NEW)

**Reference:** `aiprovider/anthropic.md`

**Key Differences from OpenAI:**
- Endpoint: `{base_url}/messages` (not `/chat/completions`)
- Headers: `x-api-key` (not `Authorization: Bearer`)
- Required header: `anthropic-version: 2023-06-01`
- Required field: `max_tokens` in request body
- Model list API available

**Implementation Structure:**
```python
class AnthropicModel(BaseAIModel):
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    DEFAULT_API_BASE_URL = "https://api.anthropic.com/v1"
    ANTHROPIC_VERSION = "2023-06-01"
    
    def prepare_headers(self):
        return {
            "Content-Type": "application/json",
            "x-api-key": self.get_token(),
            "anthropic-version": self.ANTHROPIC_VERSION
        }
    
    def prepare_request_data(self, prompt, **kwargs):
        return {
            "model": self.config.get('model'),
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
    
    def fetch_available_models(self):
        # GET {base_url}/models
        # Headers: x-api-key, anthropic-version
        # Parse response.data[].id
        pass
```

#### 3.3 Implementation Steps

1. Create `models/anthropic.py`
2. Implement `AnthropicModel` class
3. Handle special headers (`x-api-key`, `anthropic-version`)
4. Handle `max_tokens` requirement
5. Implement model list fetching
6. Add to factory and config
7. Test with Anthropic API key

---

## Feature 4: Add Nvidia AI Support

### Why Nvidia
- **Free API access for 6 months**
- Popular models available (Llama, DeepSeek-R1, Qwen)
- Good for users without paid API keys
- Rate limit: 40 RPM (sufficient for personal use)

### Implementation

#### 4.1 Add to Configuration

**File:** `models/base.py`

```python
DEFAULT_MODELS = {
    # ... existing ...
    AIProvider.AI_NVIDIA: ModelConfig(
        provider=AIProvider.AI_NVIDIA,
        display_name="Nvidia AI",
        api_key_label="Nvidia API Key:",
        default_api_base_url="https://integrate.api.nvidia.com/v1",
        default_model_name="meta/llama-3.3-70b-instruct"
    ),
}
```

#### 4.2 Create Nvidia Model Class

**File:** `models/nvidia.py` (NEW)

**Reference:** `aiprovider/nvidia.md`

**Special Considerations:**
- OpenAI-compatible API format
- **CORS issue when fetching model list from browser**
- Solution: Calibre plugin runs in Python (not browser), so CORS not an issue
- Same format as Grok/DeepSeek

**Implementation Structure:**
```python
class NvidiaModel(BaseAIModel):
    DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"
    DEFAULT_API_BASE_URL = "https://integrate.api.nvidia.com/v1"
    
    # Same implementation as GrokModel (OpenAI-compatible)
    def prepare_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }
    
    def prepare_request_data(self, prompt, **kwargs):
        return {
            "model": self.config.get('model'),
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
    
    def fetch_available_models(self):
        # GET {base_url}/models
        # No CORS issue in Calibre plugin (Python requests)
        pass
```

#### 4.3 Popular Nvidia Models

Add these as suggestions in UI:
- `meta/llama-4-maverick-17b-128e-instruct`
- `meta/llama-4-scout-17b-16e-instruct`
- `meta/llama-3.3-70b-instruct`
- `deepseek-ai/deepseek-r1`
- `qwen/qwen2.5-coder-32b-instruct`

#### 4.4 Implementation Steps

1. Create `models/nvidia.py`
2. Implement `NvidiaModel` class (similar to Grok)
3. Add to factory and config
4. Add model suggestions in UI
5. Test with Nvidia API key
6. Verify no CORS issues (should work fine in Python)

---

## Implementation Order

### Phase 1: Foundation (Feature 1)
**Priority:** HIGH  
**Estimated Time:** 2-3 hours

1. Update `BaseAIModel` with `fetch_available_models()`
2. Implement for existing providers (Grok, Gemini, DeepSeek)
3. Update `ConfigDialog` UI with dropdown
4. Test model list fetching

**Why First:** This improves UX for existing providers and provides infrastructure for new ones.

---

### Phase 2: OpenAI Integration (Feature 2)
**Priority:** HIGH  
**Estimated Time:** 1-2 hours

1. Create `models/openai.py`
2. Implement `OpenAIModel` class
3. Add to configuration and factory
4. Test with OpenAI API

**Why Second:** Most requested provider, standard API format.

---

### Phase 3: Anthropic Integration (Feature 3)
**Priority:** MEDIUM  
**Estimated Time:** 1-2 hours

1. Create `models/anthropic.py`
2. Handle special headers and request format
3. Add to configuration and factory
4. Test with Anthropic API

**Why Third:** Different API format, good test of flexibility.

---

### Phase 4: Nvidia Integration (Feature 4)
**Priority:** MEDIUM  
**Estimated Time:** 1 hour

1. Create `models/nvidia.py`
2. Add to configuration and factory
3. Add model suggestions
4. Test with Nvidia API

**Why Last:** Similar to existing OpenAI-compatible providers, easiest to implement.

---

## Technical Considerations

### 1. Error Handling

**Model List Fetching:**
- Network errors → Show error message, allow manual input
- Invalid API key → Show authentication error
- Timeout → Show timeout message, retry option
- Empty list → Show warning, allow manual input

**API Calls:**
- Invalid model name → Show error with suggestion
- Rate limiting → Show rate limit message
- API errors → Show detailed error from provider

### 2. UI/UX Improvements

**Config Dialog:**
```
┌─────────────────────────────────────┐
│ Provider: [OpenAI ▼]                │
│                                     │
│ API Key: [******************]       │
│                                     │
│ Model: [gpt-4o-mini ▼] [🔄 Refresh]│
│                                     │
│ Base URL: [https://api.openai...]  │
│                                     │
│ [Test Connection]  [Save]  [Cancel]│
└─────────────────────────────────────┘
```

**Features:**
- Dropdown for model selection
- Refresh button to reload models
- Test connection button
- Loading indicator during fetch
- Error messages inline

### 3. Caching

**Model Lists:**
- Cache fetched model lists for 1 hour
- Refresh on user request
- Store in memory (not persistent)

**Benefits:**
- Reduce API calls
- Faster config dialog opening
- Better UX

### 4. Backward Compatibility

**Existing Configs:**
- Detect old config format (manual model input)
- Migrate to new format automatically
- Keep manual input as fallback option

**User Experience:**
- No breaking changes
- Smooth upgrade path
- Preserve existing settings

---

## File Changes Summary

### New Files
```
models/openai.py       # OpenAI implementation
models/anthropic.py    # Anthropic implementation  
models/nvidia.py       # Nvidia implementation
```

### Modified Files
```
models/base.py         # Add fetch_available_models() method
                       # Add new providers to enum
                       # Add new configs to DEFAULT_MODELS

config.py              # Update UI with dropdowns
                       # Add refresh button handlers
                       # Add new provider tabs

models/__init__.py     # Export new model classes

api.py                 # May need updates for error handling

i18n/*.py              # Add translations for new providers
```

---

## Testing Plan

### Manual Testing Checklist

**For Each Provider:**
- [ ] API key validation works
- [ ] Model list fetches successfully
- [ ] Dropdown populates with models
- [ ] Refresh button works
- [ ] Manual input still works (fallback)
- [ ] Chat requests work with selected model
- [ ] Streaming responses work
- [ ] Error handling works (invalid key, network error)

**Integration:**
- [ ] Switch between providers works
- [ ] Config saves and loads correctly
- [ ] Plugin loads without errors
- [ ] All existing features still work

---

## Success Criteria

### Feature 1: Dynamic Model List
- ✅ Model dropdown works for all providers
- ✅ Refresh button fetches latest models
- ✅ Error handling shows helpful messages
- ✅ Manual input still available as fallback

### Feature 2: OpenAI Support
- ✅ OpenAI provider appears in dropdown
- ✅ API key validation works
- ✅ Chat requests work with GPT models
- ✅ Streaming responses work

### Feature 3: Anthropic Support
- ✅ Anthropic provider appears in dropdown
- ✅ Special headers handled correctly
- ✅ Chat requests work with Claude models
- ✅ Model list fetching works

### Feature 4: Nvidia Support
- ✅ Nvidia provider appears in dropdown
- ✅ Free tier works correctly
- ✅ Popular models available
- ✅ No CORS issues

---

## Documentation Updates

### README.md
- Add OpenAI to supported providers
- Add Anthropic to supported providers
- Add Nvidia to supported providers
- Update API key instructions
- Add free tier information (Nvidia)

### CRITICAL_RULES.md
- Document new provider enum values
- Document model list API requirements

### PROJECT_STRUCTURE.md
- Add new model files
- Update architecture diagrams
- Document model list feature

---

## Timeline

**Total Estimated Time:** 5-8 hours

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 1 | Dynamic model list (base) | 2-3h | Pending |
| 2 | OpenAI integration | 1-2h | Pending |
| 3 | Anthropic integration | 1-2h | Pending |
| 4 | Nvidia integration | 1h | Pending |
| - | Testing & bug fixes | 1-2h | Pending |
| - | Documentation | 1h | Pending |

**Target Completion:** 2025.10.22 - 2025.10.23

---

## Notes

- All API documentation is in `aiprovider/` folder
- Follow existing code patterns in `models/grok.py`
- Use `CRITICAL_RULES.md` to avoid breaking changes
- Test on all platforms (Windows, macOS, Linux)
- Update version number after completion

---

**Created:** 2025.10.21 Night  
**Status:** Planning Phase  
**Next Action:** Review and edit this plan, then start Phase 1
