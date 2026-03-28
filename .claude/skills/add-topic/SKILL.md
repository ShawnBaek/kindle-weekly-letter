---
name: add-topic
description: Add a new topic to the Kindle Weekly Letter. Use when the user wants to add a custom research topic.
disable-model-invocation: true
argument-hint: [topic name]
---

# Add Topic to Kindle Weekly Letter

The user wants to add a new topic: **$ARGUMENTS**

Follow these steps:

## Step 1: Gather Details

Ask the user:
1. **Topic name** — What should this topic be called in the EPUB?
2. **Audience** — Who is this for? (e.g., "senior engineers", "product managers", "beginners")
3. **Focus areas** — What subtopics should the agent search for? (list 3-5)
4. **Preferred sources** — Any specific websites, blogs, or publications to prioritize?
5. **What to avoid** — Any sources or content types to skip?

## Step 2: Create Agent Prompt

Create a new file at `prompts/agent_{topic_id}.md` following the same format as existing agent prompts in the `prompts/` directory. Read one (e.g., `prompts/agent_ai_news.md`) as a reference template.

The agent prompt must:
- Describe the research task clearly
- List preferred sources
- Specify quality criteria
- Return the standard JSON structure with: topic, articles, section_intro

## Step 3: Add Sources Config

Add an entry to `sources.json` for the new topic with the user's preferred sources. Read the existing `sources.json` to understand the format.

## Step 4: Register Topic

Add the new topic to `src/config.py` in the TOPICS list:
```python
{
    "id": "{topic_id}",
    "name": "{Topic Name}",
    "prompt_file": "agent_{topic_id}.md",
},
```

## Step 5: Update Prompts

Add the new agent to:
- `prompts/daily_collector.md` — add to the agent prompts list
- `prompts/sunday_compiler.md` — add to the proposal display template

## Step 6: Confirm

Tell the user:
- Topic "{Topic Name}" has been added
- It will start collecting articles at the next daily run
- They can run `/collect-now` to start immediately
- They can edit sources in `sources.json`
