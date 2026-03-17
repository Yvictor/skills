# Yvictor Skills

[Agent Skills](https://agentskills.io) for AI-assisted development workflows. Compatible with any agent that supports the open Agent Skills format.

## Available Skills

| Skill | Description |
|-------|-------------|
| [review-driven-development](skills/review-driven-development/) | Issue-to-merge workflow with iterative review cycles |

## Installation

### Claude Code

```bash
claude plugins marketplace add yvictor/skills
claude plugins install dev-workflow@yvictor-skills
```

### OpenAI Codex

```bash
npx skills add yvictor/skills --all
```

### npx skills (any agent)

```bash
npx skills add yvictor/skills
```

### Manual

Copy the skill directory into your agent's skills folder:

```bash
git clone https://github.com/Yvictor/skills.git
cp -r skills/skills/review-driven-development ~/.your-agent/skills/
```

### Direct URL

Any agent can load the skill directly from:
```
https://raw.githubusercontent.com/Yvictor/skills/main/skills/review-driven-development/SKILL.md
```
