#!/usr/bin/env python3
"""
Google Indexing API Integration
Sends newly published blog post URLs to Google for fast indexing
Uses OAuth 2.0 with service account credentials
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    print("[WARNING] google-auth not installed. Run: pip install google-auth google-auth-httplib2")

# Google Indexing API endpoint
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

# Base URL for the website
BASE_URL = "https://nikaappliancerepair.com"


def get_credentials():
    """Load Google service account credentials from environment variable"""
    credentials_json = os.environ.get('GOOGLE_INDEXING_API_KEY')

    if not credentials_json:
        print("[ERROR] GOOGLE_INDEXING_API_KEY environment variable not set")
        return None

    try:
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES
        )
        print("[OK] Successfully loaded Google credentials")
        return credentials
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in GOOGLE_INDEXING_API_KEY: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to load credentials: {e}")
        return None


def send_url_to_google(session, url, action="URL_UPDATED"):
    """
    Send a single URL notification to Google Indexing API

    Args:
        session: Authorized session
        url: Full URL to index
        action: URL_UPDATED or URL_DELETED

    Returns:
        dict with success status and response
    """
    payload = {
        "url": url,
        "type": action
    }

    try:
        response = session.post(INDEXING_API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "url": url,
                "notifyTime": result.get("urlNotificationMetadata", {}).get("latestUpdate", {}).get("notifyTime"),
                "response": result
            }
        else:
            return {
                "success": False,
                "url": url,
                "status_code": response.status_code,
                "error": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


def get_published_posts():
    """Read recently published posts from log file"""
    base_dir = Path(__file__).parent.parent
    log_file = base_dir / 'blog' / '_published_log.json'

    if not log_file.exists():
        print(f"[INFO] No published log found at {log_file}")
        return []

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)

        # Filter posts published today
        today = datetime.now().strftime('%Y-%m-%d')
        today_posts = [p for p in posts if p.get('date') == today]

        print(f"[INFO] Found {len(today_posts)} posts published today ({today})")
        return today_posts
    except Exception as e:
        print(f"[ERROR] Failed to read published log: {e}")
        return []


def get_indexed_urls_log():
    """Get previously indexed URLs to avoid duplicates"""
    base_dir = Path(__file__).parent.parent
    log_file = base_dir / 'blog' / '_indexed_urls.json'

    if not log_file.exists():
        return set()

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return set(data.get('urls', []))
    except:
        return set()


def save_indexed_urls(urls):
    """Save indexed URLs to log file"""
    base_dir = Path(__file__).parent.parent
    log_file = base_dir / 'blog' / '_indexed_urls.json'

    existing = get_indexed_urls_log()
    all_urls = list(existing.union(set(urls)))

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'urls': all_urls
        }, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Send URLs to Google Indexing API')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be sent without actually sending')
    parser.add_argument('--url', type=str, help='Specific URL to index (for manual testing)')
    parser.add_argument('--all-today', action='store_true', help='Index all posts published today')
    args = parser.parse_args()

    print("=" * 70)
    print("GOOGLE INDEXING API")
    print("=" * 70)
    print()

    # Check if google-auth is available
    if not GOOGLE_AUTH_AVAILABLE:
        print("[ERROR] google-auth library not installed")
        print("        Run: pip install google-auth google-auth-httplib2")
        sys.exit(1)

    # Get credentials
    credentials = get_credentials()
    if not credentials and not args.dry_run:
        print("[ERROR] Cannot proceed without valid credentials")
        sys.exit(1)

    # Determine URLs to index
    urls_to_index = []

    if args.url:
        # Manual single URL
        urls_to_index.append(args.url)
    else:
        # Get today's published posts
        posts = get_published_posts()
        already_indexed = get_indexed_urls_log()

        for post in posts:
            # Build full URL
            url_path = post.get('url', '')
            if url_path.startswith('/'):
                full_url = BASE_URL + url_path
            else:
                full_url = BASE_URL + '/' + url_path

            # Skip if already indexed
            if full_url in already_indexed:
                print(f"[SKIP] Already indexed: {full_url}")
                continue

            urls_to_index.append(full_url)

    if not urls_to_index:
        print("\n[INFO] No new URLs to index")
        print("=" * 70)
        return

    print(f"\n[INFO] URLs to index: {len(urls_to_index)}")
    for url in urls_to_index:
        print(f"       - {url}")
    print()

    # Dry run mode
    if args.dry_run:
        print("[DRY RUN] Would send the above URLs to Google Indexing API")
        print("          Run without --dry-run to actually send")
        return

    # Create authorized session and send URLs
    session = AuthorizedSession(credentials)

    results = {
        "success": [],
        "failed": []
    }

    print("Sending URLs to Google Indexing API...")
    print("-" * 70)

    for url in urls_to_index:
        result = send_url_to_google(session, url)

        if result["success"]:
            print(f"[OK] {url}")
            print(f"     Notify time: {result.get('notifyTime', 'N/A')}")
            results["success"].append(url)
        else:
            print(f"[FAIL] {url}")
            print(f"       Error: {result.get('error', 'Unknown error')}")
            results["failed"].append(url)

    print("-" * 70)
    print(f"\nResults: {len(results['success'])} success, {len(results['failed'])} failed")

    # Save successfully indexed URLs
    if results["success"]:
        save_indexed_urls(results["success"])
        print(f"[OK] Saved {len(results['success'])} URLs to indexed log")

    print("=" * 70)

    # Exit with error if any failed
    if results["failed"]:
        sys.exit(1)


if __name__ == '__main__':
    main()
