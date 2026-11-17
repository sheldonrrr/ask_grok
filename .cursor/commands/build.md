# /build — Package a minimal plugin zip for release

Build a **smallest runnable** Calibre plugin zip for local install / publishing. Use the **canonical packaging script**. Do not invent a one-off `zip` command unless `scripts/package.sh` is missing.

Alias: `/pack` (same workflow).

Packaging does not add 1 to the third version number. That number moves only when `caldbg-ag` runs.

## Steps

1. From the repo root, run:

```bash
bash scripts/package.sh
```

2. Confirm the artifact:

```text
dist/Ask_AI_Plugin_vX.Y.Z.zip
```

(`X.Y.Z` comes from `version.py` → `VERSION_STRING`.)

3. Sanity-check zip contents (quick list is enough):

**Must include (runtime):**

- Plugin Python modules at zip root (`__init__.py`, `ui.py`, `models/`, …)
- `i18n/`, `images/`, `lib/ask_ai_plugin_vendor/` (including `*.dist-info/` LICENSE/METADATA)
- `tutorial/tutorial_v1.2.md`, plus `tutorial_v1.2.zh.md`, `tutorial_v1.2.zht.md`, and `tutorial_v1.2.ja.md`
- the previous manual, `tutorial/tutorial_v1.1.md`
- `plugin-import-name-ask_ai_plugin.txt`
- `LICENSE`, `README.md`
- `.env.example` (script re-adds it if present)

**Must NOT include** (dev / repo-only — see `scripts/package.sh` and `.gitignore` packaging notes):

- `.git/`, `.cursor/`, `.github/`, other editor/tooling dirs
- `release/`, `aiprovider/`, `scripts/`, `tests/`, `bin/`, `backend/`, `dist/`
- `setup.py`, `requirements.txt`, `AGENTS.md`
- `ask_ai_plugin_gif_preview.gif` (README preview only; stays in git)
- `tutorial/about.md` (dev-only)
- Caches / junk: `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`, `node_modules/`
- OS junk: `.DS_Store`, `._*`, `__MACOSX/`, `Thumbs.db`, `Desktop.ini`, `$RECYCLE.BIN/`, etc.
- Secrets: `.env`, `.env.*` (except shipping `.env.example`)

4. Reply with the **full path** to the zip and the version string.

## Rules

- Prefer `scripts/package.sh` as the single source of truth for excludes. If excludes drift from `.gitignore` packaging notes or miss OS junk, **fix the script first**, then re-run `/build`.
- Do **not** commit the zip under `dist/` (gitignored).
- Do **not** bump the version here — use `/upgrade-version` (alias: `/version-up`).
- Do **not** upload/release unless the user also asks.

## Do not

- Hand-zip the whole repo (pulls in tests/scripts/release/dev trees)
- Package with `calibre-customize -b` as a substitute for the release zip
- Include local debug helpers, agent transcripts, or IDE folders
