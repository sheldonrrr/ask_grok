# /push — Commit progress and push to the current branch’s remote

Commit the current worktree with a **readable English** message, then push to the **upstream of the current branch** (e.g. `dev` → `origin/dev`).

## Steps (do all of them)

1. Run in parallel:
   - `git status`
   - `git diff` and `git diff --staged`
   - `git log -5 --oneline` (match recent style; prefer readable English)
   - `git branch -vv` (confirm current branch and upstream)
2. Stage relevant changes (`git add` for intended files). **Never** stage secrets (`.env`, credentials, API keys).
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

## Stop and ask if

- There are no changes to commit
- Upstream is missing or ambiguous and push target is unclear
- Push would require force, or conflicts with remote
- Only secret/credential files are present

## Do not

- Update git config
- Skip hooks
- Push unrelated junk (`dist/*.zip`, `__pycache__`, `.env`)
- Force-push to `main` / `master`
