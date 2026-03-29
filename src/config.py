from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STYLES_DIR = PROJECT_ROOT / "styles"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Email (Yahoo SMTP)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.yahoo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
KINDLE_EMAILS = [
    e.strip() for e in os.getenv(
        "KINDLE_EMAILS",
        "yoshiboarder@kindle.com"
    ).split(",")
]

# Topics
TOPICS = [
    {
        "id": "english",
        "name": "English for Software Engineers",
        "prompt_file": "agent_english.md",
    },
    {
        "id": "ai_news",
        "name": "AI Engineering News",
        "prompt_file": "agent_ai_news.md",
    },
    {
        "id": "ios",
        "name": "iOS Engineering",
        "prompt_file": "agent_ios.md",
    },
    {
        "id": "business",
        "name": "Travel App Business",
        "prompt_file": "agent_business.md",
    },
    {
        "id": "news",
        "name": "Singapore & Korea News",
        "prompt_file": "agent_news.md",
    },
    {
        "id": "systems_lang",
        "name": "Swift / C++ / C / Rust / Python & Algorithms",
        "prompt_file": "agent_systems_lang.md",
    },
]
