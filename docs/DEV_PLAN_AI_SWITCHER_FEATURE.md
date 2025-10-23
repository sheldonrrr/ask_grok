# AI Switcher Feature Development Plan

**Created:** 2025-10-23  
**Feature:** AI Provider Switcher & Configuration Status Indicator

---

## 📋 Feature Overview

### Current Problems
1. **No visual indication** of which AI providers have been configured
2. **Cannot switch AI providers** in the dialog window - must go to config page
3. **Poor user experience** when managing multiple AI providers

### Goals
1. Add checkmark (✓) prefix to configured AI providers in the config dropdown menu
2. Track AI configuration status in database (mark as "configured" when user saves valid config)
3. Convert read-only model display to switchable dropdown in dialog window
4. Display both provider name and model name (e.g., "Nvidia + deepseek-r1:1.5b")

---

## 🎯 Requirements Analysis

### Requirement 1: Visual Indicator in Config Menu
**What:** Add checkmark character (✓, not emoji) before configured AI names in config dropdown

**Criteria for "Configured":**
- User has entered API Key (except Ollama which doesn't require it)
- User has loaded model list OR entered custom model name
- User has clicked Save button

**Implementation:**
- Modify `config.py` dropdown display logic
- Store `is_configured` flag in model config
- Update dropdown item text format: `"✓ x.AI (Grok)"` vs `"x.AI (Grok)"`

### Requirement 2: Configuration Status Tracking
**What:** Add `is_configured` field to track AI setup status

**Storage Location:** `prefs['models'][model_id]['is_configured']`

**Trigger Conditions:**
```python
is_configured = (
    (has_api_key OR model_id == 'ollama') AND
    (has_model_name) AND
    (user_clicked_save)
)
```

**Files to Modify:**
- `config.py` - Add field to model config
- `config.py` - Set flag in `save_settings()`
- `config.py` - Check flag when building dropdown

### Requirement 3: AI Switcher in Dialog
**What:** Replace read-only label with dropdown in dialog window

**Current Implementation:**
- Location: `ui.py` line 903
- Widget: `QLabel` showing `"Model: x.AI (Grok)"`
- Position: Status bar (bottom-left)

**New Implementation:**
- Widget: `QComboBox` (dropdown)
- Position: Top-right corner of dialog
- Items: Only show configured AI providers
- Display format: `"Provider + Model"` (e.g., "Nvidia + deepseek-r1:1.5b")
- On change: Reload API client with new model

**Display Format Examples:**
```
x.AI (Grok) + grok-4-latest
Google Gemini + gemini-2.0-flash-exp
Deepseek + deepseek-chat
Custom + llama3
Nvidia + deepseek-r1:1.5b
OpenAI + gpt-4o-mini
Anthropic (Claude) + claude-3-5-sonnet-20241022
OpenRouter + meta-llama/llama-3.3-70b-instruct
Ollama (Local) + qwen2.5:14b
```

---

## 🏗️ Technical Design

### Data Structure Changes

#### 1. Model Config Schema
```python
# In prefs['models'][model_id]
{
    'api_key': str,           # Existing
    'api_base_url': str,      # Existing
    'model': str,             # Existing
    'display_name': str,      # Existing
    'enabled': bool,          # Existing
    'is_configured': bool,    # NEW - marks if fully configured
}
```

#### 2. Helper Functions
```python
# In config.py
def is_model_configured(model_id: str, model_config: dict) -> bool:
    """Check if a model is fully configured"""
    # Ollama doesn't need API key
    if model_id == 'ollama':
        has_auth = True
    else:
        api_key_field = 'auth_token' if model_id == 'grok' else 'api_key'
        has_auth = bool(model_config.get(api_key_field, '').strip())
    
    has_model = bool(model_config.get('model', '').strip())
    
    return has_auth and has_model

# In ui.py
def get_configured_models() -> List[Tuple[str, str, str]]:
    """Get list of configured models
    Returns: [(model_id, provider_name, model_name), ...]
    """
    prefs = get_prefs()
    models_config = prefs.get('models', {})
    configured = []
    
    for model_id, config in models_config.items():
        if config.get('is_configured', False):
            provider_name = config.get('display_name', model_id)
            model_name = config.get('model', 'unknown')
            configured.append((model_id, provider_name, model_name))
    
    return configured

def format_model_display(provider_name: str, model_name: str) -> str:
    """Format display text for model switcher"""
    return f"{provider_name} + {model_name}"
```

---

## 📝 Implementation Plan

### Phase 1: Configuration Status Tracking (1.5h)

#### Step 1.1: Add `is_configured` Field
**File:** `config.py`
**Location:** `ModelConfigWidget.get_config()`

```python
def get_config(self):
    config = {}
    # ... existing code ...
    
    # NEW: Determine if model is configured
    config['is_configured'] = self._is_model_configured(config)
    
    return config

def _is_model_configured(self, config: dict) -> bool:
    """Check if current model config is complete"""
    # Check API key (except Ollama)
    if self.model_id == 'ollama':
        has_auth = True
    else:
        api_key_field = 'auth_token' if self.model_id == 'grok' else 'api_key'
        has_auth = bool(config.get(api_key_field, '').strip())
    
    # Check model name
    has_model = bool(config.get('model', '').strip())
    
    return has_auth and has_model
```

#### Step 1.2: Update Dropdown Display
**File:** `config.py`
**Location:** `ConfigWidget.update_model_name_display()`

```python
def update_model_name_display(self):
    # ... existing code ...
    
    # Get current models config to check configured status
    prefs = get_prefs()
    models_config = prefs.get('models', {})
    
    for provider, model_id in model_mapping.items():
        if provider in DEFAULT_MODELS:
            display_name_key = f"model_display_name_{model_id}"
            translated_name = self.i18n.get(display_name_key, DEFAULT_MODELS[provider].display_name)
            
            # NEW: Add checkmark if configured
            model_config = models_config.get(model_id, {})
            if model_config.get('is_configured', False):
                translated_name = f"✓ {translated_name}"
            
            self.model_combo.addItem(translated_name, model_id)
```

### Phase 2: AI Switcher UI in Dialog (2h)

#### Step 2.1: Create Model Switcher Widget
**File:** `ui.py`
**Location:** `AskDialog.setup_ui()`

```python
def setup_ui(self):
    # ... existing code ...
    
    # NEW: Create top bar with model switcher
    top_bar = QHBoxLayout()
    
    # Title on the left
    title_label = QLabel(self.i18n['menu_title'])
    title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
    top_bar.addWidget(title_label)
    
    top_bar.addStretch()
    
    # Model switcher on the right
    model_switcher_label = QLabel(f"{self.i18n.get('current_ai', 'Current AI')}:")
    model_switcher_label.setStyleSheet("color: #666; font-size: 12px;")
    top_bar.addWidget(model_switcher_label)
    
    self.model_switcher = QComboBox()
    self.model_switcher.setMinimumWidth(250)
    self.model_switcher.currentIndexChanged.connect(self.on_model_switched)
    self._populate_model_switcher()
    top_bar.addWidget(self.model_switcher)
    
    layout.addLayout(top_bar)
    
    # ... rest of existing code ...
```

#### Step 2.2: Populate Model Switcher
**File:** `ui.py`

```python
def _populate_model_switcher(self):
    """Populate model switcher with configured models"""
    prefs = get_prefs()
    models_config = prefs.get('models', {})
    current_model = prefs.get('selected_model', 'grok')
    
    self.model_switcher.clear()
    
    # Get all configured models
    for model_id, config in models_config.items():
        if config.get('is_configured', False):
            provider_name = config.get('display_name', model_id)
            model_name = config.get('model', 'unknown')
            display_text = f"{provider_name} + {model_name}"
            
            self.model_switcher.addItem(display_text, model_id)
            
            # Select current model
            if model_id == current_model:
                self.model_switcher.setCurrentIndex(self.model_switcher.count() - 1)
    
    # If no configured models, show warning
    if self.model_switcher.count() == 0:
        self.model_switcher.addItem(self.i18n.get('no_configured_models', 'No AI configured'), None)
        self.model_switcher.setEnabled(False)

def on_model_switched(self, index):
    """Handle model switch event"""
    model_id = self.model_switcher.itemData(index)
    if not model_id:
        return
    
    # Save new selection
    prefs = get_prefs()
    prefs['selected_model'] = model_id
    
    # Reload API client
    self.api.reload_model()
    
    # Update window title
    model_display_name = self.api.model_display_name
    self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
    
    # Log the change
    logger.info(f"Switched to model: {model_id}")
```

#### Step 2.3: Remove Old Model Info Label
**File:** `ui.py`

```python
# DELETE or COMMENT OUT these lines:
# self.model_info_label = QLabel(...)
# self.statusBar.addPermanentWidget(self.model_info_label)

# UPDATE update_model_info() to use switcher instead
def update_model_info(self):
    """Update model info display after config change"""
    try:
        self.api.reload_model()
        
        # Refresh model switcher
        if hasattr(self, 'model_switcher'):
            self._populate_model_switcher()
        
        # Update window title
        model_display_name = self.api.model_display_name
        if hasattr(self, 'book_info') and self.book_info:
            self.setWindowTitle(f"{self.i18n['menu_title']} [{model_display_name}] - {self.book_info.title}")
    except Exception as e:
        logger.error(f"Error updating model info: {str(e)}")
```

### Phase 3: i18n Support (0.5h)

#### Add Translations
**File:** `i18n/en.py`

```python
'current_ai': 'Current AI',
'no_configured_models': 'No AI configured - Please configure in settings',
'switch_model': 'Switch AI Model',
```

**Note:** Only update English translations. Other languages will be updated later in batch.

### Phase 4: Testing & Refinement (1h)

#### Test Cases

1. **Configuration Status Tracking**
   - [ ] Configure new AI → checkmark appears in dropdown
   - [ ] Remove API key → checkmark disappears
   - [ ] Remove model name → checkmark disappears
   - [ ] Ollama without API key → still shows checkmark if model configured

2. **Model Switcher in Dialog**
   - [ ] Only configured models appear in switcher
   - [ ] Display format is correct: "Provider + Model"
   - [ ] Switching model reloads API client
   - [ ] Window title updates after switch
   - [ ] No configured models → switcher disabled with warning message

3. **Edge Cases**
   - [ ] First-time user (no configured models)
   - [ ] User configures first model → switcher becomes enabled
   - [ ] User unconfigures all models → switcher shows warning
   - [ ] Long model names → dropdown width handles properly

4. **Persistence**
   - [ ] Selected model persists across dialog close/open
   - [ ] Configuration status persists across Calibre restart

---

## 📂 Files to Modify

### Core Files
1. **`config.py`** (Major changes)
   - Add `is_configured` field logic
   - Update dropdown display with checkmarks
   - Modify `get_config()` and `save_settings()`

2. **`ui.py`** (Major changes)
   - Add model switcher widget
   - Remove old model info label
   - Add switch handler
   - Update `update_model_info()`

3. **`i18n/en.py`** (Minor changes)
   - Add new translation keys

### Supporting Files
4. **`api.py`** (No changes needed)
   - Existing `reload_model()` method works as-is

---

## ⏱️ Time Estimates

| Phase | Task | Estimated Time |
|-------|------|----------------|
| 1 | Configuration Status Tracking | 1.5h |
| 2 | AI Switcher UI | 2h |
| 3 | i18n Support | 0.5h |
| 4 | Testing & Refinement | 1h |
| **Total** | | **5 hours** |

---

## 🎨 UI Mockup

### Before (Current)
```
┌─────────────────────────────────────────────┐
│ Ask Grok [x.AI (Grok)] - Book Title        │
├─────────────────────────────────────────────┤
│ [Book Info Area]                            │
│                                             │
│ [Response Area]                             │
│                                             │
│ [Input Area]                                │
├─────────────────────────────────────────────┤
│ Model: x.AI (Grok)                          │
└─────────────────────────────────────────────┘
```

### After (New)
```
┌─────────────────────────────────────────────┐
│ Ask Grok    Current AI: [x.AI + grok-4] ▼  │
├─────────────────────────────────────────────┤
│ [Book Info Area]                            │
│                                             │
│ [Response Area]                             │
│                                             │
│ [Input Area]                                │
├─────────────────────────────────────────────┤
│ [Status messages]                           │
└─────────────────────────────────────────────┘
```

### Config Dropdown (Before)
```
Current AI: [x.AI (Grok)          ▼]
            [Google Gemini         ]
            [Deepseek              ]
            [Custom                ]
```

### Config Dropdown (After)
```
Current AI: [✓ x.AI (Grok)        ▼]
            [✓ Google Gemini       ]
            [  Deepseek            ]
            [✓ Custom              ]
```

---

## 🚀 Implementation Order

1. ✅ Create development plan document
2. ⏳ Phase 1: Add `is_configured` tracking
3. ⏳ Phase 2: Build model switcher UI
4. ⏳ Phase 3: Add English translations
5. ⏳ Phase 4: Test all scenarios
6. ⏳ Fix bugs and refine UX

---

## 📌 Notes

- Use Unicode checkmark character `✓` (U+2713), not emoji ✅
- Only show configured models in dialog switcher
- Config dropdown shows ALL models (with/without checkmark)
- Model switcher should be prominent but not intrusive
- Consider adding tooltip to switcher explaining the format
- Future enhancement: Add "Configure More AIs" button in dialog

---

## 🔍 Potential Issues & Solutions

### Issue 1: Model switcher too wide
**Solution:** Set max width, truncate long model names with ellipsis

### Issue 2: User switches model mid-conversation
**Solution:** Clear conversation history when switching? Or keep it?
**Decision:** Keep history, just switch the AI for new questions

### Issue 3: Configured model becomes invalid (API key expired)
**Solution:** Show error message, don't remove from switcher. Let user fix in config.

### Issue 4: No configured models on first use
**Solution:** Show helpful message with link to config page

---

## ✅ Success Criteria

- [x] Development plan created and reviewed
- [ ] Checkmarks appear for configured AIs in config dropdown
- [ ] Model switcher works in dialog window
- [ ] Display format shows "Provider + Model"
- [ ] Only configured models appear in switcher
- [ ] Switching models reloads API client correctly
- [ ] All test cases pass
- [ ] Code is clean and well-documented
- [ ] No regressions in existing functionality

---

**End of Development Plan**
