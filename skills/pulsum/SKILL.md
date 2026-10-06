---
name: pulsum
description: Pull the latest changes for the current git repository and summarize everything that changed since the last pull, including what changed, who changed it, and why they likely did it. Use when the user says "pulsum", "pull and summarize", "catch me up", "what changed since I last pulled", or "what did everyone do".
---

# Pulsum: Pull and Summarize

Pull the current branch's latest upstream changes. Then explain the incoming
changes as a short briefing: what changed, who did it, and why they most likely
did it.

## 1. Check the repository before pulling

Run these commands from the repository the user is working in:

```sh
git rev-parse --show-toplevel
git status --short --branch
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

- If the directory is not a git repository, stop and say so.
- If the branch has no upstream or HEAD is detached, ask which branch to pull.
  Do not guess.
- If there are uncommitted changes, do not stash, reset, or discard them. A
  fast-forward pull still works when the incoming files do not overlap the
  local edits. If they do overlap, report the conflicting files and ask how to
  proceed.

## 2. Record the starting point, then pull

```sh
BEFORE=$(git rev-parse HEAD)
git fetch --prune
git pull --ff-only
AFTER=$(git rev-parse HEAD)
```

- Use `--ff-only`. If the branch has diverged, stop and report how many
  commits are only local and how many are only upstream
  (`git rev-list --left-right --count HEAD...@{u}`). Ask whether to merge or
  rebase. Never pick one silently.
- If `BEFORE` equals `AFTER`, the pull brought nothing new. Use the previous
  pull as the starting point instead: find the most recent `pull` or `merge`
  entry with
  `git reflog show --date=iso --format='%h %gd %gs' HEAD | grep -E 'pull|merge' | head -5`.
  Then use the commit before it (`HEAD@{n+1}`) as `BEFORE`, and tell the user
  which pull you are summarizing and its date. If there is no earlier pull,
  say the branch is up to date and stop.
- For a shallow clone, run `git fetch --deepen=<n>` only if history is missing
  for the range.

## 3. Gather what changed

Use the range `$BEFORE..$AFTER`:

```sh
git log --no-merges --reverse --format='%h%x09%an%x09%ad%x09%s' --date=short $BEFORE..$AFTER
git shortlog -sn --no-merges $BEFORE..$AFTER
git diff --stat $BEFORE $AFTER
git diff --name-status $BEFORE $AFTER
```

Then look at the changes themselves:

- Read each commit with `git show --stat <sha>` and the relevant parts of
  `git show <sha>`. For large ranges, skim the diffs and read in full the
  files that matter most, such as core logic, public APIs, schemas, and
  configuration.
- Look up pull request context on GitHub when `gh` is available:
  `gh api repos/{owner}/{repo}/commits/<sha>/pulls --jq '.[] | {number, title, body, user: .user.login}'`.
  Fetch each pull request only once. Linked issues, PR descriptions, and review
  comments are the best evidence for why a change was made.
- Group commits that belong together, such as all commits from one PR or one
  feature, instead of describing each commit separately.
- Ignore pure noise unless it matters, such as lockfile churn, formatting-only
  commits, or generated files. Mention it in one line.

## 4. Infer why

For each group of changes, explain the most likely reason. Draw on, in order:

1. Pull request titles, descriptions, and linked issues
2. Commit messages
3. The code itself: new tests that describe a bug, added error handling,
   removed features, TODOs that were resolved, and changed defaults
4. Timing and sequence, such as a fix shortly after a feature, or a revert

Clearly separate stated reasons from guesses. Write "PR #123 says…" for stated
reasons and "Likely…" or "Probably…" for inferences. Do not invent motives that
the evidence does not support. Say "Reason unclear" instead.

## 5. Flag what affects the user

Call out anything the user must act on locally:

- New or changed dependencies, which need an install
- Database migrations or schema changes
- New or renamed environment variables, configuration, or secrets
- Breaking API changes, removed functions, or renamed files the user's local
  work may reference
- Changed build, test, or tooling commands
- Overlap with the user's uncommitted changes or local commits

## 6. Report

Use this shape. Keep it scannable and lead with the summary.

```md
**Pulled <n> commits from <m> people into `<branch>`** (<short BEFORE>..<short AFTER>, <date range>)

<2–3 sentences on the overall picture: the main themes of this batch.>

## What changed
- **<Theme or feature>**: <what changed>. <Why, stated or inferred>. (<people>, PR #<n>)
- …

## Who did what
- **<Name>** (<n> commits): <one line on their focus>
- …

## Action needed
- <Install deps, run migrations, set new env vars, and so on; or "None">

## Worth a look
- <Risky changes, surprising removals, reverts, or anything unclear>
```

- Order themes by impact, not by commit order.
- Link PRs and commits when the remote is on GitHub.
- For more than about 30 commits, keep "What changed" to the top 5 themes and
  put the rest in a single "Also" line.
- Omit empty sections, except "Action needed", where you write "None".
