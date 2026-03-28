"""Send EPUB to Kindle via Yahoo SMTP.

Usage:
    python3 -m src.email_sender --epub output/newsletter.epub
"""

import argparse
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

from .config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, SMTP_HOST, SMTP_PORT, KINDLE_EMAILS


def send_epub(epub_path: Path, to_emails: list[str] = KINDLE_EMAILS) -> bool:
    """Send EPUB file to all Kindle devices via SMTP. Returns True if all succeed."""
    if not EMAIL_ADDRESS:
        print("Error: EMAIL_ADDRESS not set in .env", file=sys.stderr)
        return False
    if not EMAIL_APP_PASSWORD:
        print("Error: EMAIL_APP_PASSWORD not set in .env", file=sys.stderr)
        return False

    epub_data = epub_path.read_bytes()
    subject = epub_path.stem.replace("_", " ").title()
    all_ok = True

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)

            for to_email in to_emails:
                msg = EmailMessage()
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.add_attachment(
                    epub_data,
                    maintype="application",
                    subtype="epub+zip",
                    filename=epub_path.name,
                )
                try:
                    smtp.send_message(msg)
                    print(f"Sent to {to_email}")
                except Exception as e:
                    print(f"Failed to send to {to_email}: {e}", file=sys.stderr)
                    all_ok = False

    except Exception as e:
        print(f"SMTP connection failed: {e}", file=sys.stderr)
        return False

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Send EPUB to Kindle via SMTP")
    parser.add_argument("--epub", required=True, help="Path to EPUB file")
    args = parser.parse_args()

    epub_path = Path(args.epub)
    if not epub_path.exists():
        print(f"Error: EPUB not found: {epub_path}", file=sys.stderr)
        sys.exit(1)

    success = send_epub(epub_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
