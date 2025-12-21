# Release Update Guide (Beyond Version Bump)

This guide summarizes what to update **besides** the version number when shipping a new Ask AI Plugin release.

## 1) Code / Feature Checklist

- Ensure new providers/features are wired into:
  - `models/` implementation
  - `models/__init__.py` registration
  - `api.py` model/provider mapping
  - `config.py` defaults + UI wiring
  - i18n keys (at least `en/zh`, and maintained languages as needed)
- Confirm "Random Question" behavior is not unintentionally affected.
- Confirm streaming vs non-streaming behavior matches expectations.

## 2) Documentation Checklist

### 2.1 Changelog

- Create a **new** changelog file for the release (do not edit previous versions), e.g.:
  - `docs/CHANGELOG_V1.3.7_EN.md`
- Use the same structure as previous changelogs:
  - BBCode section for MobileRead
  - Markdown bullet list section for GitHub

### 2.2 Tutorial

- Create a **new** tutorial file for the release (do not edit previous versions), e.g.:
  - `tutorial/tutorial_v0.5.md`
- Update the header line:
  - `Latest updated: <date>, Ask AI Plugin vX.Y.Z`
- Add a short section for any user-facing feature changes (new providers, new UX, etc.).

### 2.3 README

- Update `README.md` directly:
  - Add new provider to the provider list.
  - Add a short note about any user-facing behavior (e.g., Perplexity citations/search URLs appended).

## 3) UI / Tutorial Loading

If you maintain multiple tutorial versions, ensure the UI always loads the **latest** tutorial first:

- Prefer `tutorial/tutorial_v0.5.md`
- Fallback to `tutorial/tutorial_v0.4.md`
- Keep only the latest two tutorial files to reduce maintenance overhead

Relevant locations to check:

- `ui.py` tutorial tab/widget
- `tutorial_viewer.py` open-in-browser helper

## 4) Build + Smoke Test

- Build plugin:
  - `calibre-customize -b .`
- Run GUI:
  - `calibre-debug -g`

Verify:

- Plugin loads with no errors
- Configuration opens
- New provider appears in provider dropdown
- Provider can be tested successfully
- If streaming is enabled, UI updates properly
- Any appended extra sections (e.g. Perplexity citations) appear at the end
- Random Question still returns clean output

## 5) Packaging Sanity

Before shipping, confirm the new files are included in the plugin package:

- `docs/CHANGELOG_VX.Y.Z_EN.md`
- `tutorial/tutorial_v0.N.md`
- Any new provider docs under `aiprovider/`

If a file is missing from the built plugin zip, the UI fallback logic should still work.
