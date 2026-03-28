---
name: setup-kindle
description: Set up Kindle Weekly Letter — configure email, Kindle device, and scheduling. Use when a new user wants to get started.
disable-model-invocation: true
---

# Kindle Weekly Letter — Setup Guide

Walk the user through the complete setup process.

## Step 1: Prerequisites Check

Run:
```bash
cd !`git rev-parse --show-toplevel` && python3 --version && (test -d .venv && echo "venv exists" || echo "no venv")
```

If no venv, create one and install:
```bash
uv venv && source .venv/bin/activate && uv pip install -e .
```

## Step 2: Email Configuration

Ask the user which email provider they use. Support:

| Provider | SMTP Host | Port |
|----------|-----------|------|
| Gmail | smtp.gmail.com | 465 |
| Yahoo | smtp.mail.yahoo.com | 465 |
| Outlook/Hotmail | smtp-mail.outlook.com | 587 |
| iCloud | smtp.mail.me.com | 587 |

Guide them to generate an **App Password** (not their regular password):

- **Gmail**: Google Account → Security → 2-Step Verification → App Passwords
- **Yahoo**: Account Security → Generate app password
- **Outlook**: Microsoft Account → Security → App Passwords
- **iCloud**: appleid.apple.com → Sign-In and Security → App-Specific Passwords

## Step 3: Kindle Email

Ask the user for their Kindle email address.

How to find it:
1. Go to Amazon → **Manage Your Content and Devices**
2. Click **Preferences** tab
3. Scroll to **Personal Document Settings**
4. Find "Send-to-Kindle E-Mail" — it looks like `username@kindle.com`

## Step 4: Approve Sender

**IMPORTANT**: Tell the user they must add their sender email to Kindle's approved list:
1. On the same **Personal Document Settings** page
2. Scroll to **Approved Personal Document E-mail List**
3. Click **Add a new approved e-mail address**
4. Add the email address from Step 2

## Step 5: Write .env

Create `.env` file with the collected info:
```
EMAIL_ADDRESS=user@provider.com
EMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
KINDLE_EMAILS=username@kindle.com
SMTP_HOST=smtp.provider.com
SMTP_PORT=465
```

## Step 6: Test Email

Send a test EPUB:
```bash
source .venv/bin/activate && python3 -m src.epub_builder --input output/sample_content.json --output output/test.epub && python3 -m src.email_sender --epub output/test.epub
```

Ask the user to check their Kindle. If it doesn't arrive within 5 minutes:
- Verify the sender email is in Kindle's approved list
- Check the Kindle email address is correct
- Try a different SMTP port (587 instead of 465 or vice versa)

## Step 7: Schedule

Ask what time they want:
- **Daily collection**: Default 9am local time
- **Weekly EPUB**: Default Sunday midnight local time

Ask their timezone, then convert to local system time for launchd.

Create launchd plists following the pattern in:
`~/Library/LaunchAgents/com.kindle-letter.daily-collector.plist`

Load them:
```bash
launchctl load ~/Library/LaunchAgents/com.kindle-letter.daily-collector.plist
launchctl load ~/Library/LaunchAgents/com.kindle-letter.sunday-compiler.plist
```

## Step 8: Done!

Tell the user:
- Email is configured and tested
- Daily collection runs at [time]
- Weekly EPUB compiles on Sunday at [time]
- Run `/collect-now` to start collecting immediately
- Run `/add-topic` to customize topics
- Edit `sources.json` to vote/edit sources per topic
