# Boligportal Scraper Bot

An automated scraper that monitors boligportal.dk for new rental listings and sends notifications via Telegram.

## Features

- Monitors moligportal.dk search results in real-time
- Detects new listings automatically
- Sends instant Telegram notifications with listing details
- Maintains history of seen listings to avoid duplicates
- Configurable search parameters and check intervals

## Project Structure
```
boligportaldk-notifyme/
    ├── config/
    │   └── config.json
    ├── requirements.txt
    ├── main.py
    ├── notifier.py
    └── scraper.py
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/boligportaldk-notifyme.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Telegram credentials:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

4. Configure `config/config.json`:
```json
{
    "search_url": "https://www.boligportal.dk/your-search-url",
    "check_interval": 30,
    "listings_cache_file": "seen_listings.txt"
}
```

## Usage

Start the bot:
```bash
python main.py
```

## Components

- `main.py`: Main script that runs the monitoring loop
- `scraper.py`: Handles the scraping of Boligportal listings
- `notifier.py`: Manages Telegram notifications
- `config.json`: Configuration settings

## Requirements

- Python 3.7+
- Beautiful Soup 4
- Requests
- python-dotenv

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID for notifications

## Configuration Options

In `config.json`:
- `search_url`: The Boligportal.dk search URL to monitor
    for optimal results apply filters from the website, and then copy the resulting URL.
    for map search results, copy the URL from the map view, and remove the `&view=map` parameter.
- `check_interval`: Time between checks in seconds
- `seen-listings.txt`: File to store seen listing IDs

## GCloud Deployment
### Set your project
gcloud config set project YOUR_PROJECT_ID

### Build and push the image
gcloud builds submit --region=europe-west1

### Create Cloud Run Job
gcloud run jobs create boligportal-scraper \
    --image=gcr.io/YOUR_PROJECT_ID/boligportal-scraper:latest \
    --region=europe-west1 \
    --memory=1Gi \
    --cpu=1 \
    --max-retries=3 \
    --parallelism=1 \
    --task-timeout=1800 \
    --set-env-vars="CLOUD_RUN_JOB=true,TELEGRAM_BOT_TOKEN=your_token,TELEGRAM_CHAT_ID=your_chat_id"

### Create Cloud Scheduler job to trigger every 10 minutes
(within the 10 minutes it will run every 30 seconds)
gcloud scheduler jobs create http boligportal-scraper-schedule \
    --location=europe-west1 \
    --schedule="*/10 * * * *" \
    --uri="https://europe-west1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/YOUR_PROJECT_ID/jobs/boligportal-scraper:run" \
    --http-method=POST \
    --oauth-service-account-email=YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com

### Environment Variables Setup
Set these in your Cloud Run Job:

CLOUD_RUN_JOB=true
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
LISTINGS_CACHE_FILE=/app/data/seen_listings.txt
CONFIG_PATH=/app/config/config.json