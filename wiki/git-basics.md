# Git Basics

**Summary:** A short git primer for collaborators new to git (written for Alex),
covering the core concepts and the exact workflow this repo uses — enough to work
confidently, short enough not to get in the way of website development.

## What git is

Git tracks every version of every file in this project. Each saved snapshot (a
*commit*) records what changed, who changed it, and when — so nothing is ever
truly lost, and two people can work on the same site without overwriting each
other. GitHub is the website that hosts our shared copy of the repository.

## Seven terms that cover almost everything

| Term | Meaning |
|---|---|
| **repository (repo)** | The project folder plus its entire history. Ours: `github.com/mabryp/gw-church` |
| **commit** | A saved snapshot with a message describing the change |
| **branch** | A parallel line of work. `main` is the official one; work happens on short-lived side branches |
| **push / pull** | Push = send your commits up to GitHub. Pull = bring down what others pushed |
| **pull request (PR)** | A proposal to merge a branch into `main`, where others can review it first |
| **merge** | Accepting a PR — its commits become part of `main` |
| **working tree** | The files as they currently sit on disk, including edits not yet committed |

## The workflow in this repo

Claude does most of the typing, but this is what's happening underneath:

1. **Pull first** — `git pull` at session start so you're building on the latest.
2. **Branch** — site changes go on a feature branch, never straight to `main`.
3. **Edit, then commit** — small commits with clear messages.
4. **Push and open a PR** — pushing a branch that touches `site/` triggers an
   automatic preview deploy; the preview URL appears as a comment on the PR.
5. **Review on preprod, Phillip merges** — merging the PR is the approval that
   deploys the live site (gw-church.org). **Never merge your own site PR**; that
   decision belongs to the owner. Full pipeline: [ci-cd.md](ci-cd.md).

Wiki/log-only changes are the one exception: they may be committed directly to
`main` because the deploy pipeline ignores them.

## Cheat sheet

```
git status                    # what's changed? (safe to run anytime, run it often)
git pull                      # get the latest from GitHub
git checkout -b my-branch     # create and switch to a new branch
git add <file>                # stage a change for the next commit
git commit -m "message"       # snapshot the staged changes
git push -u origin my-branch  # send the branch to GitHub
git log --oneline -10         # recent history, one line per commit
git diff                      # exactly what you've edited but not committed
```

## Learning with the AI

- Ask Claude to **explain before it runs** any git command — per
  [CLAUDE.md](../CLAUDE.md), sessions run in teaching mode for you.
- `git status` and `git log` are read-only — experiment freely with them.
- Commits are safety nets, not risks: once something is committed, it is very
  hard to lose. The time to be careful is *before* committing (deleting or
  overwriting uncommitted work) and when *merging* (that's what deploys).
- If something looks wrong, stop and ask — in git, almost everything is
  recoverable, and forcing your way past an error is the main way to make
  things worse.

## Sources

Not compiled from `raw/` — authored 2026-08-02 at the owner's request as
onboarding material, from this repo's own workflow rules (`CLAUDE.md`,
[ci-cd.md](ci-cd.md)).
