# Yvictor Skills

[Agent Skills](https://agentskills.io) for AI agents. A collection of development workflow skills born from real-world experience building software with AI coding agents.

These skills capture hard-won patterns — the kind of things you learn after watching AI agents produce PRs that look good but aren't merge-ready. Instead of repeating the same review feedback across sessions, encode it once as a skill and let every future session benefit.

## Available Skills

| Skill | Description |
|-------|-------------|
| [review-driven-development](skills/review-driven-development/) | Issue-to-merge workflow with iterative review cycles that produce merge-ready PRs |

### review-driven-development

AI agents are great at generating code, but PRs are rarely merge-ready on the first try. Pattern violations, inconsistent error handling, missing edge cases — these slip through because the agent doesn't review its own work against the codebase's actual conventions.

This skill builds an **iterative review cycle** into the development workflow. The agent reviews its own PR using multiple independent reviewers, posts findings to the PR, fixes issues, and re-reviews until the verdict is APPROVE. By the time you see the PR, it's already been through N rounds of automated review.

```
Issue → Research → Plan → Implement → PR → Review ⟲ Fix → APPROVE → Merge
                                            ↑________________↩ (repeat until clean)
```

6 phases: Issue Research → Plan + Worktree → Implementation → Commit + PR → Review Cycle → Merge + Cleanup

Supports multiple reviewer strategies (agent, `codex exec`, `claude -p`), works with GitHub and GitLab, and composes with TDD, BDD, and other methodology skills.

## Installation

### npx skills (all agents)

Installs to all supported agents (Codex, Claude Code, Cursor, Cline, Gemini CLI, Amp, and 30+ more):

```bash
npx skills add yvictor/skills --all
```

### Claude Code (plugin)

```bash
claude plugins marketplace add yvictor/skills
claude plugins install dev-workflow@yvictor-skills
```

### Manual

```bash
git clone https://github.com/Yvictor/skills.git
cp -r skills/skills/<skill-name> ~/.your-agent/skills/
```
