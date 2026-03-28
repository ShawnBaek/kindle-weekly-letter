---
name: sources
description: View, vote, unvote, add, or remove sources for any topic. Use when the user wants to manage sources for a topic.
disable-model-invocation: true
argument-hint: [vote|unvote|add|remove|list] [topic] [source]
---

# Manage Sources

Read `sources.json` at the project root.

## Commands

Based on `$ARGUMENTS`, do one of:

### `/sources list` or `/sources list [topic]`
Display all sources grouped by topic in a readable table:
```
Topic: AI Engineering News
  ▲5  Anthropic Blog (anthropic.com/blog) — active
  ▲5  OpenAI Blog (openai.com/blog) — active
  ▲4  Hacker News (news.ycombinator.com) — active
  ...
```
If a topic is specified, show only that topic. Sort by votes descending.

### `/sources vote [topic] [source name]`
Increment the vote count for the matching source by 1. Save to `sources.json`.

### `/sources unvote [topic] [source name]`
Decrement the vote count for the matching source by 1 (minimum 0). Save to `sources.json`.

### `/sources add [topic] [source name] [url]`
Add a new source to the specified topic with votes=1 and status=active. Save to `sources.json`.

### `/sources remove [topic] [source name]`
Set status to "inactive" (don't delete — keep for history). Save to `sources.json`.

### `/sources` (no arguments)
Show all sources for all topics with vote counts.

## Notes
- Match topic by id (e.g., "ai_news") or by partial name (e.g., "ai", "ios", "english")
- Match source by partial name, case-insensitive
- After any change, confirm what was updated and show the updated topic
- Sources with status "inactive" are shown with ~~strikethrough~~ but still kept in the file
- Agent prompts in `prompts/` reference `sources.json` — higher voted sources get higher priority
