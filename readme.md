# Boligportal scraper bot

## Project structure
```
boligportaldk-notifyme/
    ├── config/
    │   └── config.json
    ├── requirements.txt
    ├── main.py
    └── scraper.py
```

## Step-by-Step Plan
### Step 1: Set up the project

Create a new folder and initialize a virtualenv (optional but clean)

Add requests, beautifulsoup4, and python-dotenv or pydantic (if you want config support)

### Step 2: Scrape BoligPortal

Start with a URL like:
https://www.boligportal.dk/en/rental-apartments/copenhagen/

Use requests + BeautifulSoup to extract:

Title

Price

Size

Location

Link to listing

Unique ID

### Step 3: Store Seen Listings

Save IDs in seen_listings.json (or use in-memory set() for testing)

Skip notifying if a listing was already sent

### Step 4: Send Telegram Message

Create a Telegram bot via @BotFather

Use Telegram API to send a message like:

python
Copy
Edit
https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>&text=<msg>

### Step 5: Run in a Loop

Every X seconds:

Scrape listings

Check for new ones

Send Telegram messages

Sleep

