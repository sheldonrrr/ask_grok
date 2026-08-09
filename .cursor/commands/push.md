# /push — Commit progress, then push (default)

**Default:** always **commit first**, then push. Do not push-only unless the user explicitly says so (e.g. “push only”, “push without commit”, “push existing commits only”).

Commit the current worktree with a **readable English** message, then push to the **upstream of the current branch** (e.g. `dev` → `origin/dev`).

## Steps (do all of them)

1. Run in parallel:
   - `git status`
   - `git diff` and `git diff --staged`
   - `git log -5 --oneline` (match recent style; prefer readable English)
   - `git branch -vv` (confirm current branch and upstream)
2. Stage relevant changes (`git add` for intended files). **Never** stage secrets (`.env`, credentials, API keys). Also skip pack artifacts (`dist/*.zip`), `__pycache__/`, and other gitignored junk.
3. Draft a commit message that is:
   - **English**
   - **Readable** with connecting words (e.g. “Add … after …”, “Fix … when …”, “Update … for …”)
   - 1–2 short sentences focusing on **why**, not a file dump
   - Examples:
     - `Add a set-default prompt after adding an AI service.`
     - `Fix Kimi platform labels so they follow the UI language.`
     - `Harden Add AI and About flows for more reliable Windows behavior.`
4. Commit with a HEREDOC (see user git rules). Do **not** amend unless the user asked and amend rules are satisfied.
5. Push to the remote tracking branch for **this** branch:
   - If upstream exists: `git push`
   - If no upstream yet: `git push -u origin HEAD`
   - On `dev` with `origin/dev`: normal `git push` / `git push origin dev` is fine
   - **Never** `--force` / `--force-with-lease` unless the user explicitly asks
6. Report: commit subject, local branch, remote tracking branch, and push result (PR URL only if requested).

## If the worktree is already clean

- Skip creating an empty commit.
- If the branch is ahead of upstream, still `git push`.
- If everything is already up to date, say so.

## Stop and ask if

- There are no changes to commit **and** nothing to push
- Upstream is missing or ambiguous and push target is unclear
- Push would require force, or conflicts with remote
- Only secret/credential files are present

## Do not

- Update git config
- Skip hooks
- Push without committing when there are uncommitted changes (unless user explicitly asked for push-only)
- Push unrelated junk (`dist/*.zip`, `__pycache__`, `.env`)
- Force-push to `main` / `master`
