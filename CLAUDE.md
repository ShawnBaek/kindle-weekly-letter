# Kindle Weekly Letter

Automated weekly Kindle newsletter — AI research agents collect articles daily, compile into a readable EPUB book, and deliver to your Kindle every Sunday.

## Quick Start

```bash
/setup-kindle          # Configure email, Kindle, and scheduling
/collect-now           # Start collecting articles immediately
/compile-now           # Compile and send EPUB now
/add-topic React       # Add a custom topic
/sources list          # View all sources with votes
/sources vote ios "Hacking with Swift"   # Upvote a source
```

## Default Topics (6)
1. English for Software Engineers
2. AI Engineering News (CTO-level)
3. iOS Engineering
4. Travel App Business
5. Singapore & Korea News (official publishers only)
6. C++ / C / Rust / Python

## Architecture
- **Daily collection**: 6 Agent subagents research topics in parallel, accumulate articles in `output/weekly/`
- **Sunday compilation**: Compile all articles, get user approval, generate EPUB, send to Kindle
- Each topic targets 10 articles/week — agents stop when a topic hits 10
- **Sources**: `sources.json` — community-curated, votable source list per topic
- **Skills**: `.claude/skills/` — slash commands for setup, topics, sources, manual triggers

## File Structure
```
├── .claude/skills/          # Slash commands (/setup-kindle, /add-topic, etc.)
├── .claude-plugin/          # Plugin manifest for distribution
├── prompts/                 # Agent prompts (read sources.json for source priorities)
│   ├── daily_collector.md   # Daily collection orchestrator
│   ├── sunday_compiler.md   # Sunday EPUB compilation orchestrator
│   └── agent_*.md           # Per-topic research agents
├── src/
│   ├── epub_builder.py      # EPUB generation (ebooklib + jinja2)
│   ├── email_sender.py      # SMTP email sender
│   ├── article_store.py     # Daily article accumulator with dedup
│   ├── content_formatter.py # HTML sanitization for Kindle
│   └── config.py            # Topic definitions, email config
├── sources.json             # Votable source list per topic
├── templates/               # EPUB Jinja2 templates
├── styles/kindle.css        # Kindle-optimized CSS
└── output/                  # Generated EPUBs and weekly article store
```

## Scheduling (launchd — macOS)
After running `/setup-kindle`, two launchd agents are created:
- `com.kindle-letter.daily-collector` — Daily at configured time
- `com.kindle-letter.sunday-compiler` — Sunday at configured time

## Key Commands
```bash
# Install dependencies
uv venv && source .venv/bin/activate && uv pip install -e .

# Build EPUB manually
python3 -m src.epub_builder --input output/content.json --output output/newsletter.epub

# Send EPUB manually
python3 -m src.email_sender --epub output/newsletter.epub

# Check collection status
python3 -c "from src.article_store import get_status_summary; print(get_status_summary())"
```

## Environment Variables (.env)
- `EMAIL_ADDRESS` — Your email address
- `EMAIL_APP_PASSWORD` — App Password (not your regular password)
- `SMTP_HOST` — Default: smtp.mail.yahoo.com
- `SMTP_PORT` — Default: 465
- `KINDLE_EMAILS` — Comma-separated Kindle email addresses

## Plugin Installation (for other users)
```bash
/plugin marketplace add https://raw.githubusercontent.com/ShawnBaek/kindle-letter/main/marketplace.json
/plugin install kindle-letter
```
