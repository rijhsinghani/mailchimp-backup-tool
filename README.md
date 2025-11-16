# Mailchimp Backup Tool

A Python-based tool to export and backup all your Mailchimp account data using the official Mailchimp Marketing API.

## Features

✅ **Complete Data Export** - Export everything from your Mailchimp account:
- **Audiences**: All contacts, email addresses, names, phone numbers, tags, groups, custom fields, subscription status, member ratings, opt-in data, and GDPR information
- **Campaign Reports**: Complete email activity history including who was sent what, opens, clicks, bounces, unsubscribes
- **Campaigns**: All campaign content (HTML, text, settings, metadata)
- **Templates**: Email template HTML files
- **Gallery Files**: All images and assets from your File Manager
- **Events**: Custom events passed into Mailchimp
- **SMS**: SMS contacts and history
- **E-commerce**: Products and order data
- **Appointments**: Appointment data (if applicable)

✅ **Automated**: Single command to export everything
✅ **API-Based**: Uses official Mailchimp Marketing API
✅ **Date Filtering**: Optional time-based filtering for incremental backups
✅ **Easy to Use**: Interactive prompts guide you through the process

## What Gets Exported

### Contact Data (Audiences)
- Email addresses, names, phone numbers
- Subscription status (subscribed, unsubscribed, cleaned, pending)
- Tags and groups
- Custom fields/merge fields
- Member ratings
- Opt-in timestamps and IP addresses
- GDPR marketing permissions
- Location/geo data

### Email Activity (Reports)
- Complete send history (who received which campaigns)
- Opens with timestamps
- Clicks with timestamps and link tracking
- Bounces (hard/soft with reasons)
- Unsubscribes
- Abuse reports

### Campaign & Content
- Campaign HTML and text content
- Campaign metadata and settings
- Email templates
- Gallery assets and images

## Limitations

⚠️ **24-Hour Limit**: Mailchimp only allows ONE export per 24-hour period
⚠️ **Point-in-Time**: Exports are snapshots, not real-time
⚠️ **Not Included**: Automation workflow configurations, standalone landing pages, and account settings are not exportable via API

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/rijhsinghani/mailchimp-backup-tool.git
   cd mailchimp-backup-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install requests
   # or
   pip3 install requests
   ```

3. **Get your Mailchimp API key**:
   - Log into your Mailchimp account
   - Go to **Account → Extras → API keys**
   - Create a new API key or copy an existing one
   - Your API key format will be: `xxxxx-usXX` (where XX is your data center)

## Usage

### Basic Usage

Run the script:
```bash
python mailchimp_backup.py
```

The script will:
1. Prompt for your Mailchimp API key (or read from `MAILCHIMP_API_KEY` environment variable)
2. Verify your credentials
3. Ask what data you want to export
4. Create the export and download it

### Set API Key as Environment Variable (Optional)

To avoid entering your API key each time:

**macOS/Linux**:
```bash
export MAILCHIMP_API_KEY='your-api-key-usXX'
```

**Windows**:
```cmd
set MAILCHIMP_API_KEY=your-api-key-usXX
```

**Permanent Setup** (add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):
```bash
echo 'export MAILCHIMP_API_KEY="your-api-key-usXX"' >> ~/.zshrc
```

### Export Options

When you run the script, you can choose:

1. **Everything** - All available data (audiences, campaigns, templates, reports, gallery, events, SMS, e-commerce, appointments)
2. **Audiences only** - Just contact data
3. **Campaigns only** - Just campaign content
4. **Custom selection** - Pick specific data types

### Date Filtering

You can limit your export to data created after a specific date:

```
Filter by date? (y/n): y
Since date: 2024-01-01T00:00:00Z
```

## Output

Exports are saved to the `mailchimp_backups/` directory as ZIP files:

```
mailchimp_backups/
└── mailchimp_backup_20241116_143022.zip
```

The ZIP file contains CSV files with all your exported data organized by type.

## Example Output

```
======================================================================
📧 MAILCHIMP DATA BACKUP TOOL
======================================================================

🔐 Verifying API credentials...
✅ Authenticated as: Your Company Name
📊 Total contacts: 15,234

📋 What would you like to export?

Available options:
  1. Everything
  2. Audiences only
  3. Campaigns only
  4. Custom selection

Enter your choice (1-4) [default: 1]: 1

🚀 Starting Mailchimp export...
📦 Exporting: audiences, campaigns, templates, gallery_files, reports, events, sms, ecommerce, appointments

📝 Creating export request...
✅ Export created successfully (ID: abc123)
⏳ Waiting for export to complete...
✅ Export completed!
⬇️  Downloading export to: mailchimp_backups/mailchimp_backup_20241116_143022.zip
✅ Download complete! File size: 45.23 MB
📁 Saved to: mailchimp_backups/mailchimp_backup_20241116_143022.zip

🎉 Backup completed successfully!
```

## Troubleshooting

### "Authentication failed"
- Verify your API key is correct
- Ensure your API key includes the data center (e.g., `-us19`)
- Check that your API key has the necessary permissions

### "Export timed out"
- Large accounts may take longer to export
- The script waits up to 10 minutes - contact Mailchimp support if exports consistently fail

### "Only 1 export per 24 hours"
- This is a Mailchimp limitation
- Wait 24 hours from your last export before creating a new one

## API Documentation

This tool uses the Mailchimp Marketing API:
- [Account Exports Documentation](https://mailchimp.com/developer/marketing/docs/account-exports/)
- [Account Exports API Reference](https://mailchimp.com/developer/marketing/api/account-exports/)

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Pull requests are welcome! Please feel free to submit issues or improvements.

## Disclaimer

This tool is not officially affiliated with Mailchimp. Use at your own risk. Always verify your backups are complete and accurate.
