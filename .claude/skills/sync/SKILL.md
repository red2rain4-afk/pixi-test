---
name: sync
description: Git sync - commit all changes, pull, and push in one command
disable-model-invocation: true
allowed-tools: Bash(git *)
---

# Git Sync

Sync local changes with remote repository.

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Recent commits: !`git log --oneline -3 2>/dev/null || echo "No commits yet"`

## Task

Execute the following steps in a single response:

1. **Check for changes**: If no changes, skip to step 4
2. **Stage all changes**: `git add -A`
3. **Commit**: Create a concise commit message based on the changes
4. **Pull**: `git pull --rebase` to sync with remote
5. **Push**: `git push` to upload changes

## Rules

- If there are merge conflicts during pull, stop and report them
- Commit message should be clear and descriptive (Korean or English based on context)
- Do NOT push to main/master without explicit confirmation if there are significant changes
- Always show the final git status after completion
