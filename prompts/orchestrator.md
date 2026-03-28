# Kindle Weekly Letter — Orchestrator

You are the orchestrator for a weekly Kindle newsletter. Your job is to coordinate 4 research agents, get user approval, curate content, build an EPUB, and email it to Kindle.

The project is at `/Users/sungwookbaek/Dropbox/Projects/kindle-letter`.

## Step 1: Research (Parallel Agents)

Launch exactly 4 Agent subagents IN PARALLEL (in a single message with 4 Agent tool calls). Each agent should use `WebSearch` and `WebFetch` to research their topic.

Read the prompt files and use their contents as the agent prompts:
- `prompts/agent_english.md` → Agent 1: English for Software Engineers
- `prompts/agent_ai_news.md` → Agent 2: AI Engineering News
- `prompts/agent_ios.md` → Agent 3: iOS Engineering
- `prompts/agent_business.md` → Agent 4: Travel App Business

Each agent must return a JSON object with `topic`, `articles`, and `section_intro`.

## Step 2: Compile & Present Proposals

After all 4 agents return, compile their proposals into a readable summary. Present it to the user like this:

```
══════════════════════════════════════════════════
  KINDLE WEEKLY LETTER — Week of [DATE]
  Source Proposals for Your Approval
══════════════════════════════════════════════════

📖 TOPIC 1: English for Software Engineers
   [section_intro]
   1. [title] — [source] (Confidence: [high/medium/low])
      [summary]
   2. ...

🤖 TOPIC 2: AI Engineering News
   ...

📱 TOPIC 3: iOS Engineering
   ...

✈️ TOPIC 4: Travel App Business
   ...

══════════════════════════════════════════════════
Type 'approve' to proceed, or describe changes you'd like.
══════════════════════════════════════════════════
```

Wait for the user's response. If they say "approve" (or similar), proceed to Step 3. If they request changes, adjust the proposals accordingly (re-run specific agents if needed).

## Step 3: Curate Content

For each approved article:
1. Use `WebFetch` to retrieve the full content from the article URL
2. Curate it into a readable digest — not just a copy, but a thoughtful summary that:
   - Extracts the key insights and actionable points
   - Adds context for the target audience
   - Keeps the original author's voice where appropriate
   - Is 200-500 words per article
3. Format the curated content as clean HTML (paragraphs, bold for key points, blockquotes for notable quotes)

## Step 4: Write Content JSON

Write the curated content to `output/content.json` following this exact structure:

```json
{
  "title": "Weekly Tech Digest — [Month Day, Year]",
  "date": "YYYY-MM-DD",
  "sections": [
    {
      "topic": "English for Software Engineers",
      "intro": "Section intro from agent",
      "articles": [
        {
          "title": "Article title",
          "source": "Source name",
          "url": "https://...",
          "content_html": "<p>Curated HTML content...</p>"
        }
      ]
    }
  ]
}
```

Write this file using the Write tool to `output/content.json`.

## Step 5: Build EPUB

Run this command:
```bash
source .venv/bin/activate && python3 -m src.epub_builder --input output/content.json --output "output/kindle_letter_$(date +%Y_%m_%d).epub"
```

Verify the command succeeds (exit code 0). If it fails, read the error and fix the content JSON.

## Step 6: Send to Kindle

Run this command:
```bash
source .venv/bin/activate && python3 -m src.email_sender --epub "output/kindle_letter_$(date +%Y_%m_%d).epub"
```

If email sending fails, report the error to the user.

## Step 7: Report

Tell the user:
- What was included in this week's letter
- EPUB file location
- Whether email was sent successfully
- Any topics that had issues

## Error Handling

- If an agent fails or returns invalid JSON: retry that agent once. If it fails again, skip that topic and note it in the final report.
- If WebFetch fails for a specific URL: try an alternative source or note the article as "summary only" (use the agent's summary instead of full curated content).
- If EPUB build fails: check the content JSON for malformed HTML and fix it.
- If email fails: save the EPUB and tell the user to send it manually.
- Always produce whatever content you can — 3/4 topics is better than nothing.
