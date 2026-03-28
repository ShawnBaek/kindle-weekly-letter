# Daily Article Collector

You collect articles daily for the Kindle Weekly Letter. The project is at `/Users/sungwookbaek/Dropbox/Projects/kindle-letter`.

## Step 1: Check Current Status

Run this to see how many articles each topic has:
```bash
source .venv/bin/activate && python3 -c "from src.article_store import get_status_summary; print(get_status_summary())"
```

Topics that already have 10+ articles are DONE — skip them entirely.

## Step 2: Research Missing Topics

For each topic that has FEWER than 10 articles, launch an Agent subagent. Launch all needed agents IN PARALLEL (single message, multiple Agent tool calls).

Read the prompt file for each topic and use it as the agent prompt. Add this to each agent's prompt:
> "Find 2-3 high-quality articles published in the last 24-48 hours. Return JSON with topic, articles, and section_intro."

Agent prompts:
- `prompts/agent_english.md` → English for Software Engineers (topic_id: english)
- `prompts/agent_ai_news.md` → AI Engineering News (topic_id: ai_news)
- `prompts/agent_ios.md` → iOS Engineering (topic_id: ios)
- `prompts/agent_business.md` → Travel App Business (topic_id: business)
- `prompts/agent_news.md` → Singapore & Korea News (topic_id: news)
- `prompts/agent_systems_lang.md` → C++ / C / Rust / Python (topic_id: systems_lang)

## Step 3: Store Results

For each agent that returns results, save the articles using:
```bash
source .venv/bin/activate && python3 -c "
import json
from src.article_store import add_articles
articles = json.loads('''PASTE_JSON_ARRAY_HERE''')
count = add_articles('TOPIC_ID', articles)
print(f'Topic now has {count} articles')
"
```

Replace `TOPIC_ID` with the topic id and `PASTE_JSON_ARRAY_HERE` with the articles array from the agent.

Each article in the array should have: title, url, source, summary, relevance, confidence.

## Step 4: Report

Print the updated status:
```bash
source .venv/bin/activate && python3 -c "from src.article_store import get_status_summary; print(get_status_summary())"
```

If all topics have 10+ articles, print: "All topics ready for Sunday compilation!"
Otherwise print which topics still need more articles.

## Error Handling
- If an agent fails: skip it, try again tomorrow
- If an agent returns duplicates: the store deduplicates by URL automatically
- Never block on errors — collect what you can and move on
