# /version-up — Bump plugin version

Follow the project rule in `.cursor/rules/version-update.mdc` end-to-end.

## Target version

- If the user wrote a version after the command (e.g. `/version-up 1.5.1`), use that `X.Y.Z`.
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

Verify with:

```bash
grep -n "VERSION = (\|version.*= (\|version=" version.py __init__.py setup.py
```

## Docs

- Create `docs/CHANGELOG_VX.Y.Z_EN.md` (BBCode + GitHub Markdown; user-facing).
- Keep only the latest **two** changelogs; delete older ones.
- Edit `tutorial/tutorial_v1.0.md` **in place** (date + plugin version; feature text if needed). Never add a new `tutorial_v*.md`.
- See also `docs/README.md` for naming.

## After version bump

- Do **not** commit/push unless the user also ran `/push` or asked to commit.
- Do **not** package unless the user also ran `/pack` or asked to package.
- Summarize what changed and the new version.

## Never

- Skip updating `__init__.py` `VERSION` (update push trigger)
- Ship without a changelog file for the new version
