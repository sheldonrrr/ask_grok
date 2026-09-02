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

`ui.py` reads `VERSION_DISPLAY` from `version.py` — do not hardcode a version there.

Verify with:

```bash
grep -n "VERSION = (\|version.*= (\|version=" version.py __init__.py setup.py
```

## Release notes

- Create `release/CHANGELOG_VX.Y.Z_EN.md` (BBCode for MobileRead + Markdown for GitHub; **user-facing**, not a technical dump).
- Keep only the **latest** changelog; delete older ones.
- Edit `tutorial/tutorial_v1.0.md` **in place** (header `Latest updated` + plugin version; feature text only when needed). Never add a new `tutorial_v*.md`.

## After version bump

- Do **not** commit/push unless the user also ran `/push` or asked to commit.
- Do **not** package unless the user also ran `/pack` or asked to package.
- Summarize what changed and the new version.

## Never

- Skip updating `__init__.py` `VERSION` (update-push trigger for users)
- Ship without a changelog file for the new version
- Create duplicate tutorial files like `tutorial_v1.1.md`
