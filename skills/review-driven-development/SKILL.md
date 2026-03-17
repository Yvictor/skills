---
name: review-driven-development
description: |
  Use when developing features from GitHub/GitLab issues through to merged PRs/MRs with iterative review cycles.
  Covers: issue research, implementation planning, worktree isolation, coding, testing, PR/MR creation,
  multi-reviewer code review (current agent, codex exec, claude -p), fix-review loops until APPROVE,
  merge and cleanup. Composable with TDD, BDD, systematic-debugging, and other methodology skills.
  Use this whenever: user provides an issue number (#NN), asks to implement a feature from an issue,
  wants to create a reviewed PR/MR, or needs code reviewed iteratively before merging.
  Even if the user just says "implement #42" or "work on issue 15", this skill applies.
---

# Review-Driven Development

A complete issue-to-merge workflow where the **iterative review cycle** is the core driver. The PR/MR doesn't just get created — it gets reviewed N rounds with fixes until the verdict is APPROVE.

**Announce at start:** "Using review-driven-development to implement issue #NN through the full review cycle."

## Overview

```
Issue → Research → Plan → Worktree → Implement → Test → PR/MR → Review ⟲ Fix → APPROVE → Merge
                                                                 ↑_____________↩ (repeat until clean)
```

The review cycle (Phase 5) is what separates this from a simple "code and push" workflow. Every PR/MR goes through at least one structured review round, with findings posted directly to the PR/MR. Issues get fixed, re-reviewed, and the cycle repeats until the verdict is APPROVE.

---

## Phase 1: Issue Research

When the user provides an issue number:

1. **Fetch issue details** — auto-detect platform:
   - GitHub: `gh issue view <NN> --json title,body,labels,assignees`
   - GitLab: `glab issue view <NN>`
   - If neither works, ask the user for the issue URL

2. **Research the codebase** — launch Explore agents to understand:
   - What code is involved
   - What patterns exist in the codebase
   - What reference repos or docs are relevant (check CLAUDE.md, memory)

3. **Enter plan mode** to present the implementation plan

## Phase 2: Plan + Worktree

The plan MUST include:

- **Worktree setup**: directory path, branch name (read CLAUDE.md/memory for naming conventions)
- **Files to modify**: list the key files with what changes each needs
- **Existing code to reuse**: functions, patterns, utilities found during research
- **Test strategy**: what commands to run (read from CLAUDE.md)
- **Verification**: how to confirm the changes work

After user approves the plan:

1. Create worktree + branch
2. Rebase onto latest default branch (`origin/master` or `origin/main`)
3. Begin implementation

## Phase 3: Implementation

Execute the plan following project-specific patterns from CLAUDE.md and memory.

- Follow existing code patterns — read similar files first
- Run project-specific build/test commands (from CLAUDE.md)
- Run real examples or integration tests if applicable
- This phase composes with other skills:
  - If **TDD** skill is active → write tests first, then implementation
  - If **systematic-debugging** skill is active → use it when hitting issues
  - If **brainstorming** skill is active → use it for design decisions

## Phase 4: Commit + PR/MR

1. **Rebase** onto latest default branch (`git fetch origin && git rebase origin/master` or `origin/main`)
2. **Stage specific files** — never `git add -A` or `git add .`
3. **Commit** with descriptive message
4. **Push** to remote with `-u` flag (use `--force-with-lease` if rebased)
5. **Create PR/MR**:
   - GitHub: `gh pr create --title "..." --body-file /tmp/pr_body.md`
   - GitLab: `glab mr create --title "..." --description "$(cat /tmp/pr_body.md)"`
6. **PR/MR body format**:

```markdown
## Summary
- Bullet points describing what changed and why

Closes #NN

## Test plan
- [x] Test results summary
- [x] Verification steps completed
```

## Phase 5: Review Cycle (THE CORE)

This is the heart of review-driven development. The PR/MR enters an iterative review loop.

### Step 1: Choose review strategy

Ask the user which review strategy to use (only on first review round):

| Strategy | Reviewers | When to use |
|----------|-----------|-------------|
| **Single** | Current agent (code-reviewer subagent) | Quick iterations, small changes |
| **Double** | Agent + `codex exec "..."` | Important features, want second perspective |
| **Triple** | Agent + `codex exec "..."` + `claude -p "..."` | Critical changes, maximum coverage |

### Step 2: Execute reviews

For each reviewer, provide the full PR/MR diff and ask them to check:

- Pattern compliance with the codebase (compare against similar existing files)
- Error handling consistency
- Test coverage
- Type safety and correctness
- Any issues categorized as:
  - **B** (Bug/Important) — must fix before merge
  - **S** (Suggestion) — nice to have
  - **N** (Note) — informational only

External reviewers:
```bash
# Codex review
codex exec "Review PR #NN for <repo>. Run 'git diff master...HEAD' to see the diff. Check: 1) pattern compliance 2) error handling 3) test coverage 4) correctness. Write findings."

# Claude review
claude -p "Review the git diff for PR #NN. $(git diff master...HEAD). Check pattern compliance, error handling, test coverage. Write findings with B/S/N categorization and a verdict."
```

### Step 3: Post combined review

Post the combined review findings to the PR/MR:

```bash
# GitHub
gh api repos/{owner}/{repo}/pulls/{NN}/reviews -X POST -f body="$(cat /tmp/review.md)" -f event="COMMENT"

# GitLab
glab mr note {NN} -m "$(cat /tmp/review.md)"
```

The review comment MUST include:

1. **Pattern compliance checklist** — table of checks with PASS/FAIL
2. **Issues** — categorized as B (bug), S (suggestion), N (note)
3. **Verdict** — `APPROVE` or `REQUEST_CHANGES`

### Step 4: Fix issues (if any)

If the review found B-level issues:

1. Enter plan mode with the specific issues to fix
2. Implement fixes
3. Re-run tests
4. Commit + push (new commit, don't amend)
5. **Update PR/MR body** to reflect current state (updated test counts, fixed issues, etc.)

### Step 5: Re-review

Rebase onto latest default branch if needed, then run the same review strategy again on the updated code. Post the new review to the PR/MR.

### Step 6: Repeat

Continue the fix → re-review loop until the verdict is **APPROVE** from all reviewers.

## Phase 6: Merge + Cleanup

**This phase REQUIRES explicit user confirmation.** Do NOT auto-merge. Wait for the user to say "merge", "ok merge", "ship it", etc.

Once confirmed:

1. **Merge**:
   - GitHub: `gh pr merge <NN> --merge` (or `--squash`/`--rebase` per CLAUDE.md)
   - GitLab: `glab mr merge <NN>`
2. **Cleanup**:
   - Remove worktree: `git worktree remove <path>`
   - Delete local branch: `git branch -d <branch>`
3. **Confirm**: show the merge commit on the default branch

---

## Principles

- **CLAUDE.md first** — always read project instructions before starting. Build commands, test commands, naming conventions, merge strategy — it's all there.
- **Memory** — check auto-memory for user preferences and project context from prior sessions.
- **Platform agnostic** — support both GitHub (`gh`) and GitLab (`glab`). Auto-detect from git remote.
- **Review is non-negotiable** — every PR/MR gets at least one structured review round with findings posted to the PR/MR itself.
- **Composable** — this skill handles the lifecycle; other skills handle methodology (TDD, debugging, brainstorming).
- **Only Phase 6 blocks on user** — all other phases proceed autonomously. Phase 6 (merge+cleanup) waits for explicit user confirmation.
