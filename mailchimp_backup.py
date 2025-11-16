#!/usr/bin/env python3
"""
Mailchimp Data Export/Backup Tool

This script uses the Mailchimp Marketing API to export and backup your account data.
It supports exporting audiences, campaigns, templates, gallery files, and more.

Requirements:
    pip install requests

Usage:
    python mailchimp_backup.py
"""

import requests
import time
import json
import os
from datetime import datetime
from typing import List, Optional


class MailchimpBackup:
    """Handles Mailchimp account data export via the Marketing API."""

    def __init__(self, api_key: str):
        """
        Initialize the Mailchimp backup tool.

        Args:
            api_key: Your Mailchimp API key (format: xxxxx-usXX where XX is your data center)
        """
        self.api_key = api_key

        # Extract data center from API key
        if '-' not in api_key:
            raise ValueError("Invalid API key format. Should be: xxxxx-usXX")

        self.data_center = api_key.split('-')[1]
        self.base_url = f"https://{self.data_center}.api.mailchimp.com/3.0"
        self.auth = ('anystring', self.api_key)

    def create_export(
        self,
        include_stages: List[str],
        since_timestamp: Optional[str] = None,
        output_dir: str = "mailchimp_backups"
    ) -> dict:
        """
        Create an account export and download the resulting file.

        Args:
            include_stages: List of data types to export. Options:
                - 'audiences': Export audience/list data (contacts, emails, tags, custom fields)
                - 'campaigns': Export campaign content (HTML, settings)
                - 'templates': Export email templates
                - 'gallery_files': Export gallery assets (images, files)
                - 'reports': Export campaign reports (opens, clicks, bounces, email activity)
                - 'events': Export custom events
                - 'sms': Export SMS contacts and history
                - 'ecommerce': Export e-commerce data (products, orders)
                - 'appointments': Export appointment data
            since_timestamp: Optional ISO8601 timestamp to limit export to data after this date
            output_dir: Directory to save the exported .zip file

        Returns:
            dict: Export information including file path
        """
        print(f"🚀 Starting Mailchimp export...")
        print(f"📦 Exporting: {', '.join(include_stages)}")

        # Validate include_stages
        valid_stages = ['audiences', 'campaigns', 'templates', 'gallery_files', 'reports',
                       'events', 'sms', 'ecommerce', 'appointments']
        for stage in include_stages:
            if stage not in valid_stages:
                print(f"⚠️  Warning: '{stage}' may not be a valid stage. Valid options: {valid_stages}")

        # Create export request
        export_data = {
            "include_stages": include_stages
        }

        if since_timestamp:
            export_data["since_timestamp"] = since_timestamp
            print(f"📅 Filtering data since: {since_timestamp}")

        # Step 1: Create the export
        print("\n📝 Creating export request...")
        response = requests.post(
            f"{self.base_url}/account-exports",
            auth=self.auth,
            headers={"Content-Type": "application/json"},
            json=export_data
        )

        if response.status_code != 200:
            print(f"❌ Error creating export: {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": response.text}

        export_info = response.json()
        print(f"DEBUG - Full API response: {json.dumps(export_info, indent=2)}")
        export_id = export_info.get('id')

        print(f"✅ Export created successfully (ID: {export_id})")
        print(f"⏳ Waiting for export to complete...")

        # Step 2: Poll for completion
        max_attempts = 60  # 10 minutes max (60 * 10 seconds)
        attempt = 0

        while attempt < max_attempts:
            # Check export status
            status_response = requests.get(
                f"{self.base_url}/account-exports/{export_id}",
                auth=self.auth
            )

            if status_response.status_code != 200:
                print(f"❌ Error checking export status: {status_response.status_code}")
                return {"error": status_response.text}

            status_data = status_response.json()
            status = status_data.get('status')

            if status == 'complete':
                print(f"✅ Export completed!")

                # Step 3: Download the file
                download_url = status_data.get('download_url')
                if not download_url:
                    print("❌ No download URL found in export response")
                    return {"error": "No download URL"}

                # Create output directory
                os.makedirs(output_dir, exist_ok=True)

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mailchimp_backup_{timestamp}.zip"
                filepath = os.path.join(output_dir, filename)

                print(f"⬇️  Downloading export to: {filepath}")

                # Download the file
                download_response = requests.get(download_url, auth=self.auth)

                if download_response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(download_response.content)

                    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    print(f"✅ Download complete! File size: {file_size_mb:.2f} MB")
                    print(f"📁 Saved to: {filepath}")

                    return {
                        "success": True,
                        "export_id": export_id,
                        "filepath": filepath,
                        "file_size_mb": file_size_mb,
                        "download_url": download_url
                    }
                else:
                    print(f"❌ Error downloading file: {download_response.status_code}")
                    return {"error": f"Download failed: {download_response.status_code}"}

            elif status == 'processing':
                print(f"⏳ Still processing... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(10)
                attempt += 1

            else:
                print(f"⚠️  Unexpected status: {status}")
                print(f"Full response: {json.dumps(status_data, indent=2)}")
                return {"error": f"Unexpected status: {status}"}

        print(f"❌ Export timed out after {max_attempts} attempts")
        return {"error": "Export timed out"}

    def get_account_info(self) -> dict:
        """Get basic account information to verify API key is working."""
        response = requests.get(
            f"{self.base_url}/",
            auth=self.auth
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}


def main():
    """Main function to run the backup."""

    print("=" * 70)
    print("📧 MAILCHIMP DATA BACKUP TOOL")
    print("=" * 70)
    print()

    # Get API key from environment or prompt user
    api_key = os.getenv('MAILCHIMP_API_KEY')

    if not api_key:
        print("ℹ️  To set your API key permanently, add to your environment:")
        print("   export MAILCHIMP_API_KEY='your-api-key-usXX'")
        print()
        api_key = input("Enter your Mailchimp API key (format: xxxxx-usXX): ").strip()

    if not api_key:
        print("❌ No API key provided. Exiting.")
        return

    try:
        backup = MailchimpBackup(api_key)

        # Verify API key works
        print("\n🔐 Verifying API credentials...")
        account_info = backup.get_account_info()

        if 'error' in account_info:
            print(f"❌ Authentication failed: {account_info['error']}")
            print("\nℹ️  To get your API key:")
            print("   1. Log into your Mailchimp account")
            print("   2. Go to Account > Extras > API keys")
            print("   3. Create a new API key or copy an existing one")
            return

        print(f"✅ Authenticated as: {account_info.get('account_name', 'Unknown')}")
        print(f"📊 Total contacts: {account_info.get('total_subscribers', 'Unknown')}")
        print()

        # Configure what to export
        print("📋 What would you like to export?")
        print()
        print("Available options:")
        print("  1. Everything (audiences, campaigns, templates, gallery, reports, events, sms, ecommerce, appointments)")
        print("  2. Audiences only (contacts, emails, tags, custom fields, subscription history)")
        print("  3. Campaigns only")
        print("  4. Custom selection")
        print()

        choice = input("Enter your choice (1-4) [default: 1]: ").strip() or "1"

        if choice == "1":
            # Export EVERYTHING possible
            include_stages = [
                'audiences',      # All contact data
                'campaigns',      # Campaign content
                'templates',      # Email templates
                'gallery_files',  # Images and assets
                'reports',        # Campaign reports and email activity
                'events',         # Custom events
                'sms',           # SMS contacts
                'ecommerce',     # E-commerce data
                'appointments'   # Appointment data
            ]
        elif choice == "2":
            include_stages = ['audiences']
        elif choice == "3":
            include_stages = ['campaigns']
        elif choice == "4":
            print("\nAvailable stages:")
            print("  - audiences (contacts, emails, tags, custom fields)")
            print("  - campaigns (campaign content)")
            print("  - templates (email templates)")
            print("  - gallery_files (images and assets)")
            print("  - reports (email activity, opens, clicks)")
            print("  - events (custom events)")
            print("  - sms (SMS contacts)")
            print("  - ecommerce (products, orders)")
            print("  - appointments (appointment data)")
            stages_input = input("Enter stages (comma-separated): ").strip()
            include_stages = [s.strip() for s in stages_input.split(',') if s.strip()]
        else:
            print("Invalid choice. Using default (everything).")
            include_stages = ['audiences', 'campaigns', 'templates', 'gallery_files', 'reports',
                            'events', 'sms', 'ecommerce', 'appointments']

        # Optional: time filter
        print()
        filter_choice = input("Filter by date? (y/n) [default: n]: ").strip().lower()
        since_timestamp = None

        if filter_choice == 'y':
            print("\nEnter date in ISO8601 format (e.g., 2024-01-01T00:00:00Z)")
            since_timestamp = input("Since date: ").strip()

        # Create the export
        print()
        print("=" * 70)
        result = backup.create_export(
            include_stages=include_stages,
            since_timestamp=since_timestamp
        )
        print("=" * 70)

        if result.get('success'):
            print()
            print("🎉 Backup completed successfully!")
            print(f"📁 File: {result['filepath']}")
            print(f"💾 Size: {result['file_size_mb']:.2f} MB")
            print()
            print("⚠️  Note: You can only create one export per 24-hour period.")
        else:
            print()
            print(f"❌ Backup failed: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
