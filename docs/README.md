# Documentation naming

Conventions for files under `docs/`, `tutorial/`, and `aiprovider/` (GitHub / developer reference; most of these are **not** shipped in the plugin zip).

## `docs/`

| Kind | Pattern | Example |
|------|---------|---------|
| Changelog (required each release) | `CHANGELOG_VX.Y.Z_EN.md` | `CHANGELOG_V1.5.0_EN.md` |
| Process / ops guides | `SCREAMING_SNAKE.md` | `VERSION_UPDATE_CHECKLIST.md` |
| Product notes / PRDs | `SCREAMING_SNAKE.md` | `PRD_BOOK_CONTENT_CHAT.md` |

- Keep only the **latest two** changelog files.
- Changelog body: MobileRead BBCode section + GitHub Markdown section (see existing files).

## `tutorial/`

| File | Role |
|------|------|
| `tutorial_v1.0.md` | **Only** user manual shipped with the plugin; edit **in place** on each release |
| `about.md` | Origin story (optional reading; not loaded by the Tutorial UI) |

Do **not** add `tutorial_v1.1.md` etc. — use git history for diffs.

## `aiprovider/`

| Pattern | Example |
|---------|---------|
| lowercase provider / topic slug + `.md` | `gemini.md`, `nvidia_free.md`, `openai_compatible.md` |

Reference configs for developers; excluded from `scripts/package.sh`.

## Release zip (not under `docs/`)

Canonical artifact from `./scripts/package.sh`:

```text
dist/Ask_AI_Plugin_vX.Y.Z.zip
```

No spaces in the filename (Windows / shell friendly). Legacy names `Ask AI Plugin-X.Y.Z.zip` are obsolete.
