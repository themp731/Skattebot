#!/usr/bin/env python3
"""Create a safe local email preview.  This command never sends email."""
import argparse
import csv
from email.message import EmailMessage
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a weekly recap email dry-run or .eml preview")
    parser.add_argument("--recap", required=True, type=Path)
    parser.add_argument("--recipients", required=True, type=Path)
    parser.add_argument("--sender", default="skattebot@example.invalid")
    parser.add_argument("--subject", default="Skattebot weekly recap")
    parser.add_argument("--preview", type=Path, help="Where to write an RFC 822 .eml preview")
    parser.add_argument("--dry-run", action="store_true", help="Print the preview plan; never sends")
    parser.add_argument("--send", action="store_true", help="Reserved for a future explicit delivery integration")
    args = parser.parse_args()
    if args.send:
        parser.error("Real sending is intentionally not implemented in this local-only command.")
    if not args.dry_run and not args.preview:
        parser.error("Specify --dry-run and/or --preview; this command never sends by default.")
    with args.recipients.open(newline="", encoding="utf-8") as handle:
        recipients = [row["email"] for row in csv.DictReader(handle) if row.get("email")]
    recap = args.recap.read_text(encoding="utf-8")
    message = EmailMessage()
    message["From"] = args.sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = args.subject
    message.set_content(recap)
    preview = args.preview
    if preview:
        preview.parent.mkdir(parents=True, exist_ok=True)
        preview.write_bytes(message.as_bytes())
    print(f"DRY RUN: sender={args.sender}; subject={args.subject}; recipients={len(recipients)}; recap={args.recap}; preview={preview or 'not written'}")


if __name__ == "__main__":
    main()
