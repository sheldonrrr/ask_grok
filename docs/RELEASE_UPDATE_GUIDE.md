# Release Update Guide (Beyond Version Bump)

What to update **besides** the version number when shipping a new Ask AI Plugin release.
For the version-number checklist, see [VERSION_UPDATE_CHECKLIST.md](VERSION_UPDATE_CHECKLIST.md).
For file naming, see [README.md](README.md).

## 1) Code / Feature Checklist

- Ensure new providers/features are wired into:
  - `models/` implementation
  - `models/__init__.py` registration
  - `api.py` model/provider mapping
  - `config.py` defaults + UI wiring
  - i18n keys (at least `en`/`zh`, and maintained languages as needed)
- Confirm "Random Question" behavior is not unintentionally affected.
- Confirm streaming vs non-streaming behavior matches expectations.

## 2) Documentation Checklist

### 2.1 Changelog

- Create a **new** file: `docs/CHANGELOG_VX.Y.Z_EN.md` (do not edit previous version files for release notes).
- Structure: MobileRead BBCode section + GitHub Markdown section (copy from the previous changelog).
- Keep only the **latest two** changelogs; delete older ones.

### 2.2 Tutorial

- Edit **in place**: `tutorial/tutorial_v1.0.md` (do not create `tutorial_v*.md` copies).
- Update the header: `Latest updated: <date>, Ask AI Plugin vX.Y.Z`
- Add or adjust short user-facing sections when behavior changes.

### 2.3 README / provider notes

- Update root `README.md` for new providers or user-visible behavior.
- Optionally update `aiprovider/<slug>.md` for developer reference (not shipped in the zip).

## 3) Tutorial loading

- UI loads only `tutorial/tutorial_v1.0.md` (`ui.py`, `tutorial_viewer.py`).
- No multi-version fallback chain.

## 4) Build + Smoke Test

```bash
calibre-customize -b .
./scripts/package.sh          # → dist/Ask_AI_Plugin_vX.Y.Z.zip
calibre-debug -g
```

Verify: plugin loads, About shows `vX.Y.Z`, config/providers work, streaming if enabled, Random Question still clean.

## 5) Packaging Sanity

**Included in zip (runtime):** plugin Python, `i18n/`, `images/`, `lib/ask_ai_plugin_vendor/`, `tutorial/tutorial_v1.0.md`, `.env.example`, etc.

**GitHub only (excluded by `scripts/package.sh`):**

- `docs/` (including changelogs)
- `aiprovider/`
- `scripts/`, `tests/`, `bin/`
- `.cursor/`, `.github/`, `backend/`

Canonical artifact name: `dist/Ask_AI_Plugin_vX.Y.Z.zip`.
