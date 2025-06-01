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
    │   └── config.json     # configuration file
    ├── Dockerfile          # Docker image for cloud deployment
    ├── main.py             # Main script that runs the monitoring loop
    ├── notifier.py         # Telegram notifier
    ├── requirements.txt    # python dependencies
    └── scraper.py          # Handles the scraping of Boligportal listings
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

3. Create a `.env` file with your Telegram credentials: (google how to get telegram bot token and chat id, it's pretty straightforward)
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

4. Configure `config/config.json` to your liking:
- `search_url`: The Boligportal.dk search URL to monitor.
    For optimal results, apply filters from the website and then copy the resulting URL.
    For location filters, go to the map view, zoom in to the area of your liking, copy the resulting URL and remove the `&view=map` parameter.
- `check_interval`: Time between checks in seconds
- `seen-listings.txt`: File to store seen listing IDs

## Usage

### Local Development

Start the bot:

if you're using Pycharm the venv is activated for you automatically, otherwise
```
source venv/bin/activate    # (Linux/macOS) 

venv\Scripts\activate       # (Windows)
```
then
```bash
python main.py
```
### Cloud Deployment

I used apify, but you can use any cloud provider you want.
The setup is pretty straightforward, connect your GitHub repo to apify, and then you can deploy the actor.

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID for notifications

