#!/usr/bin/env python3
"""
Simple lead scraper for demonstration purposes.

Given a list of company URLs, this script fetches the HTML and extracts
email addresses using a regular expression.  It prints the results to
stdout.  For production use, consider using a headless browser library
like Playwright to handle JavaScript and dynamic content.

Usage:

    python lead_scraper.py

Modify the `company_list` variable to target your own domains.
"""

import re
import requests
from bs4 import BeautifulSoup


def find_emails_from_html(html: str) -> set[str]:
    """Extract email addresses from a block of HTML text."""
    return set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html))


def scrape_emails(url: str) -> set[str]:
    """Fetch a webpage and extract email addresses."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to fetch {url}: {exc}")
        return set()

    soup = BeautifulSoup(resp.text, "html.parser")
    emails = find_emails_from_html(soup.get_text())
    return emails


def main() -> None:
    # Example company websites; replace with your targets
    company_list = [
        "https://example.com",
        "https://another-example.org",
    ]

    for company in company_list:
        emails = scrape_emails(company)
        if emails:
            print(f"{company} → {', '.join(emails)}")
        else:
            print(f"{company} → no emails found")


if __name__ == "__main__":
    main()