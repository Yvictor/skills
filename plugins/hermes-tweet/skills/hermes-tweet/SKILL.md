---
name: hermes-tweet
description: |
  Use when an AI coding agent needs to install, verify, or hand off Hermes Tweet, the native Hermes Agent plugin for X/Twitter automation through Xquik.
  Covers: Hermes plugin installation, XQUIK_API_KEY runtime setup, read-first workflows, action-gate safety, and links to the official package docs.
---

# Hermes Tweet

Hermes Tweet is a native Hermes Agent plugin for X/Twitter automation through Xquik. Use it when a Hermes runtime needs X search, account reads, monitoring, or explicitly approved account actions.

## Install

Install and enable the plugin in the Hermes runtime that will execute tools:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

If Hermes already discovered the plugin but did not enable it, run:

```bash
hermes plugins enable hermes-tweet
```

For a PyPI install inside the Hermes virtual environment:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
```

## Configure

Set the API key only in the runtime environment or `~/.hermes/.env`:

```bash
export XQUIK_API_KEY="xq_..."
```

Keep actions disabled unless the session needs approved posting, DMs, follows, media changes, monitors, or webhooks:

```bash
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Use `/reload` in an active Hermes CLI session, or restart gateway and cron sessions, after changing runtime environment values.

## Workflow

1. Use `tweet_explore` first. It searches the bundled endpoint catalog and does not need network access.
2. Use `tweet_read` for catalog-listed public or authenticated read paths after `XQUIK_API_KEY` is configured.
3. Use `tweet_action` only when `HERMES_TWEET_ENABLE_ACTIONS=true` and the user explicitly intends an account-changing action.
4. Install on the remote Hermes gateway host when Desktop connects to a remote profile.
5. Keep API keys out of prompts, issues, PR comments, tool arguments, and public logs.

## References

- Repository: https://github.com/Xquik-dev/hermes-tweet
- Install guide: https://github.com/Xquik-dev/hermes-tweet#install
- Surface guide: https://github.com/Xquik-dev/hermes-tweet/blob/master/docs/HERMES_SURFACES.md
