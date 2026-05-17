---
name: openai-current-docs
description: Use when the user wants OpenAI API, model, SDK, Agents SDK, Responses API, ChatGPT app, or Codex product guidance that must be checked against the current official OpenAI docs before answering. This is a wrapper around the system openai-docs skill with an explicit current-docs-first requirement.
---

# OpenAI Current Docs

Use this skill as a thin wrapper around the system `openai-docs` skill.

## Required Behavior

When this skill is invoked:

1. Load and follow the `openai-docs` skill when it is available.
2. Check the current official OpenAI docs before answering.
3. Prefer the configured `openaiDeveloperDocs` MCP server for search and fetch.
4. Cite the official OpenAI doc pages used.
5. If the MCP server is unavailable or returns no useful result, follow the fallback rules in `openai-docs`: use only official OpenAI domains when browsing, and clearly say when fallback guidance was used.

## Scope

Use for:

- OpenAI API design or implementation guidance
- current model selection
- model or prompt migration guidance
- Responses API, Chat Completions, Agents SDK, Realtime API, Apps SDK, or Codex product questions
- verifying OpenAI parameters, limits, model names, or recommended API patterns

Do not use this skill as authority for:

- Mythic Edge parser truth ownership
- local credentials or API key handling
- pricing or availability unless verified in current official docs
- changing project code, model defaults, prompts, or environment variables unless the user explicitly asks for implementation

## Default Invocation Text

If the user wants a pasteable starter, use:

```text
Use $openai-current-docs. Check the current official OpenAI docs before answering.
```
