# /upgrade-version — Bump plugin version

Follow the project rule in `.cursor/rules/version-update.mdc` end-to-end.

Alias: `/version-up` (same workflow).

## Target version

- If the user wrote a version after the command (e.g. `/upgrade-version 1.5.2`), use that `X.Y.Z`.
- Otherwise infer the next semver from the current `VERSION` in `version.py` and the nature of uncommitted/recent work:
  - features → MINOR
  - fixes only → PATCH
  - breaking → MAJOR
- State the chosen version before editing; if ambiguous, ask once.

## Required updates (all must match)

1. `version.py` → `VERSION = (X, Y, Z)`
2. `__init__.py` → `VERSION = (X, Y, Z) # 版本号推送触发`
3. `__init__.py` → `AskAIPlugin.version = (X, Y, Z)`
4. `setup.py` → `version='X.Y.Z'`
5. About version next to “最新更新” / latest update → must show `vX.Y.Z` via `VERSION_DISPLAY` from `version.py` (see below). Do not skip this check.
6. About latest-update copy → key `about_latest_update` in **every** `i18n/*.py` and the English fallback in `ui.py` (date + one sentence; see below). Do not skip any language.

`ui.py` reads `VERSION_DISPLAY` from `version.py` — do not hardcode a version there.

Verify with:

```bash
grep -n "VERSION = (\|version.*= (\|version=" version.py __init__.py setup.py
grep -n "VERSION_DISPLAY\|about_latest_update" ui.py version.py
grep -n "about_latest_update" i18n/*.py
python3 -m unittest tests.test_i18n_parity -v
```

## Release notes

- Create `release/CHANGELOG_VX.Y.Z_EN.md` (BBCode for MobileRead + Markdown for GitHub; **user-facing**, not a technical dump).
- Keep only the **latest** changelog; delete older ones.
- When the tutorial content changes, write `tutorial/tutorial_vX.Y.md` for the new tutorial version (header manual version, `Latest updated`, and plugin version; feature text only when needed). Keep exactly two tutorial markdown files: the latest and the immediately previous version. Delete older `tutorial_v*.md` files beyond those two. Do not keep editing the old filename after the header version changes. Point current-tutorial links at the latest file.

## About version and “最新更新” / latest update

The About page shows the version and the latest-update line as two labels. Both are required on every bump. Skipping either fails the bump.

### 5. Version number (must become `vX.Y.Z`)

The version beside the latest-update block is **not** inside `about_latest_update`. It is a separate label:

- File: `ui.py`, `AboutWidget.apply_translations`.
- Widget: `version_label`.
- Text: `{about_version_label}: {VERSION_DISPLAY}` (key `about_version_label`, e.g. “Version” / “版本”).
- Source: `version.py` → `VERSION_DISPLAY = f'v{VERSION_STRING}'`, which follows `VERSION = (X, Y, Z)` from step 1. There is no second copy to edit in `ui.py`.

After step 1, confirm that label still reads `VERSION_DISPLAY` and will therefore show `vX.Y.Z`. If you find a hardcoded `X.Y.Z` or `vX.Y.Z` on that label in `ui.py`, remove it and keep the `VERSION_DISPLAY` read.

`about_latest_update` has no version number today. Shape is date + one sentence only (Chinese `最新更新（YYYY.MM.DD）：…`, English `Latest update (YYYY.MM.DD): …`). Do not insert a version into that sentence. If a hardcoded `X.Y.Z` or `vX.Y.Z` is ever present inside `about_latest_update`, change that hardcoded version to the new `X.Y.Z` in **every** `i18n/*.py` and in the `ui.py` English fallback so they all match.

### 6. Latest-update sentence (`about_latest_update`)

Update key `about_latest_update` in **every** `i18n/*.py` and the English fallback in `ui.py` (the default of `i18n.get('about_latest_update', ...)` in `apply_translations`):

- Keep the existing shape: label, date in `YYYY.MM.DD`, then one short sentence.
- Set the date to today.
- Replace the sentence with one user-facing line for this release’s latest change or optimization. Translate it in each language; do not copy English into the other files.
- Every language file and the `ui.py` fallback must use the same date and the same meaning.

Confirm with the greps above: `ui.py` still formats the version label from `VERSION_DISPLAY` (About shows `vX.Y.Z`), and every `about_latest_update` string shares the new date and sentence. If any of those strings contain a version, they must all be the new `X.Y.Z`.

## After version bump

- Do **not** commit/push unless the user also ran `/push` or asked to commit.
- Do **not** package unless the user also ran `/build` (or `/pack`) or asked to package.
- Summarize what changed and the new version.

## Never

- Skip updating `__init__.py` `VERSION` (update-push trigger for users)
- Skip the About version check: `version_label` must keep reading `VERSION_DISPLAY` from `version.py` so About shows `vX.Y.Z`
- Skip `about_latest_update` in any `i18n/*.py` or the `ui.py` fallback (date + one translated sentence)
- Hardcode `X.Y.Z` / `vX.Y.Z` into `ui.py` or into `about_latest_update` (that sentence has no version unless one is already hardcoded, in which case replace it everywhere)
- Ship without a changelog file for the new version
- Edit an old `tutorial/tutorial_vX.Y.md` in place after its header version changes, or keep more than the latest tutorial markdown plus the immediately previous file
