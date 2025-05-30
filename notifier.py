import requests
import os
from dotenv import load_dotenv
from typing import Dict
import urllib.parse
import json


class TelegramNotifier:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram bot token or chat ID not found in .env file")

    def format_message(self, listing: Dict) -> str:
        """Format listing information into a readable message."""
        return (
            f"🏠 *New Listing Found!*\n\n"
            f"📍 {listing['rooms']} ({listing['size']} m²)\n"
            f"📮 {listing['city']}, {listing['street']}\n"
            f"💰 {listing['price']}\n"
            f"⏰ {listing['listing_age']}\n\n"
            f"🔗 [View Listing]({listing['url']})"
        )

    def send_notification(self, listing: Dict) -> bool:
        """Send notification about new listing to Telegram."""
        try:
            message = self.format_message(listing)
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }

            response = requests.post(url, data=data)

            if not response.ok:
                print(f"Detailed error: {response.text}")  # This will show the actual error message
                response.raise_for_status()

            return True

        except Exception as e:
            print(f"Error sending Telegram notification: {str(e)}")
            print(f"Chat ID being used: {self.chat_id}")  # This will show what chat ID is being used
            return False