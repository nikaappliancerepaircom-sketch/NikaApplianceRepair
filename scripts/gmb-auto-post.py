#!/usr/bin/env python3
"""
Google Business Profile Auto-Poster
Automatically creates GMB posts from newly published blog posts

SETUP REQUIRED:
1. Create Google Cloud Project: https://console.cloud.google.com/
2. Enable "Google My Business API"
3. Create OAuth2 credentials (Desktop app)
4. Download credentials.json to this folder
5. Run once manually to authorize and create token.json

Environment Variables:
- GMB_ACCOUNT_ID: Your GMB account ID
- GMB_LOCATION_ID: Your GMB location ID
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# Check for required packages
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("[ERROR] Required packages not installed. Run:")
    print("  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# OAuth2 scopes for GMB
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# File paths
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'
TOKEN_FILE = SCRIPT_DIR / 'gmb_token.json'
POSTED_LOG = SCRIPT_DIR.parent / 'blog' / '_gmb_posted.json'

def get_credentials():
    """Get or refresh OAuth2 credentials"""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"[ERROR] Missing {CREDENTIALS_FILE}")
                print("Download OAuth2 credentials from Google Cloud Console")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def get_gmb_service():
    """Initialize GMB API service"""
    creds = get_credentials()
    return build('mybusinessbusinessinformation', 'v1', credentials=creds)

def get_gmb_posts_service():
    """Initialize GMB Posts API service"""
    creds = get_credentials()
    # Note: Posts are managed through the "My Business" API
    return build('mybusiness', 'v4', credentials=creds)

def get_published_posts():
    """Get list of published blog posts"""
    log_file = SCRIPT_DIR.parent / 'blog' / '_published_log.json'

    if not log_file.exists():
        print("[INFO] No published posts log found")
        return []

    with open(log_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_posted_to_gmb():
    """Get list of posts already shared to GMB"""
    if not POSTED_LOG.exists():
        return []

    with open(POSTED_LOG, 'r', encoding='utf-8') as f:
        return json.load(f)

def mark_posted_to_gmb(post_data):
    """Mark a post as shared to GMB"""
    posted = get_posted_to_gmb()
    posted.append({
        'filename': post_data['filename'],
        'title': post_data['title'],
        'posted_at': datetime.now().isoformat()
    })

    with open(POSTED_LOG, 'w', encoding='utf-8') as f:
        json.dump(posted, f, indent=2)

def create_gmb_post(service, account_id, location_id, post_data):
    """
    Create a post on Google Business Profile

    Post types:
    - STANDARD: Regular update
    - EVENT: Event with dates
    - OFFER: Promotional offer
    - PRODUCT: Product highlight
    """

    # Build the post
    summary = post_data.get('title', '')[:1500]  # Max 1500 chars
    url = f"https://nikaappliancerepair.com{post_data.get('url', '')}"

    # Create post body
    post_body = {
        'languageCode': 'en',
        'summary': f"NEW BLOG POST: {summary}\n\nRead our latest appliance repair guide and get expert tips!",
        'callToAction': {
            'actionType': 'LEARN_MORE',
            'url': url
        },
        'topicType': 'STANDARD'
    }

    # Add media if available
    if post_data.get('featured_image'):
        post_body['media'] = [{
            'mediaFormat': 'PHOTO',
            'sourceUrl': post_data['featured_image']
        }]

    try:
        # Create the post
        parent = f"accounts/{account_id}/locations/{location_id}"
        result = service.accounts().locations().localPosts().create(
            parent=parent,
            body=post_body
        ).execute()

        print(f"[OK] Created GMB post: {summary[:50]}...")
        return result

    except Exception as e:
        print(f"[ERROR] Failed to create GMB post: {e}")
        return None

def create_gmb_post_simple(post_data, dry_run=False):
    """
    Simplified GMB post creation for manual/scheduled use

    Since GMB API requires OAuth2 flow, this function prepares
    the post content for manual posting or third-party tools
    """
    import sys

    title = post_data.get('title', 'New Blog Post')
    url = post_data.get('url', '')

    # Create post content optimized for GMB (1500 char limit)
    # Using text alternatives for emojis to avoid encoding issues
    post_content = f"""[WRENCH] NEW: {title}

Read our latest appliance repair guide with expert tips for Toronto homeowners!

[BOOK] Full article: https://nikaappliancerepair.com{url}

#ApplianceRepair #Toronto #HomeMaintenance"""

    # Version with emojis for actual posting
    post_content_emoji = f"""\U0001f527 NEW: {title}

Read our latest appliance repair guide with expert tips for Toronto homeowners!

\U0001f4d6 Full article: https://nikaappliancerepair.com{url}

#ApplianceRepair #Toronto #HomeMaintenance"""

    if dry_run:
        # Use safe print for Windows console
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

        print(f"\n{'='*60}")
        print("GMB POST PREVIEW")
        print('='*60)
        try:
            print(post_content_emoji)
        except UnicodeEncodeError:
            print(post_content)
        print('='*60)
        print(f"Character count: {len(post_content_emoji)}/1500")
        print(f"URL: https://nikaappliancerepair.com{url}")
        print('='*60 + '\n')
    else:
        try:
            print(post_content_emoji)
        except UnicodeEncodeError:
            print(post_content)

    return {
        'content': post_content,
        'url': f"https://nikaappliancerepair.com{url}",
        'cta': 'LEARN_MORE'
    }

def main():
    import argparse

    parser = argparse.ArgumentParser(description='GMB Auto-Poster')
    parser.add_argument('--dry-run', action='store_true', help='Preview posts without creating')
    parser.add_argument('--manual', action='store_true', help='Output post content for manual posting')
    parser.add_argument('--count', type=int, default=1, help='Number of posts to create')

    args = parser.parse_args()

    # Get published posts
    published = get_published_posts()
    if not published:
        print("[INFO] No published posts found")
        return

    # Get already posted to GMB
    already_posted = [p['filename'] for p in get_posted_to_gmb()]

    # Find new posts to share
    new_posts = [p for p in published if p['filename'] not in already_posted]

    if not new_posts:
        print("[INFO] All published posts have been shared to GMB")
        return

    print(f"[INFO] Found {len(new_posts)} posts to share to GMB")

    # Process posts
    for post in new_posts[:args.count]:
        if args.manual or args.dry_run:
            create_gmb_post_simple(post, dry_run=True)
        else:
            # Full API integration
            account_id = os.environ.get('GMB_ACCOUNT_ID')
            location_id = os.environ.get('GMB_LOCATION_ID')

            if not account_id or not location_id:
                print("[ERROR] Missing GMB_ACCOUNT_ID or GMB_LOCATION_ID environment variables")
                print("Run with --manual flag for manual posting")
                return

            try:
                service = get_gmb_posts_service()
                result = create_gmb_post(service, account_id, location_id, post)
                if result:
                    mark_posted_to_gmb(post)
            except Exception as e:
                print(f"[ERROR] API error: {e}")
                print("Try running with --manual flag")

if __name__ == '__main__':
    main()
