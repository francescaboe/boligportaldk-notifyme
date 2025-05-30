import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict


class BoligScraper:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.seen_listings = self._load_seen_listings()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return json.load(f)

    def _load_seen_listings(self) -> set:
        try:
            with open(self.config['listings_cache_file'], 'r') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            return set()

    def _save_seen_listings(self):
        with open(self.config['listings_cache_file'], 'w') as f:
            for listing_id in self.seen_listings:
                f.write(f"{listing_id}\n")

    def _extract_listing_id(self, url: str) -> str:
        """Extract the listing ID from the URL."""
        if 'id-' in url:
            return url.split('id-')[-1].split('/')[0]
        return url  # fallback to full URL if ID not found

    def get_new_listings(self) -> List[Dict]:
        try:
            print(f"\nFetching listings from: {self.config['search_url']}")
            response = requests.get(self.config['search_url'], headers=self.headers)

            if response.status_code != 200:
                print(f"Error: Got status code {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # Debug information
            print(f"Page title: {soup.title.string}")

            new_listings = []

            # Try multiple selector patterns
            property_cards = (
                    soup.select("a[data-test='property-card-link']") or  # Primary selector
                    soup.select("div.css-1ohpmkg a") or  # Secondary selector
                    soup.select("div.css-1ljz216 a") or  # Another possible selector
                    soup.select("a[href*='/lejligheder/']")  # Fallback selector
            )

            print(f"Found {len(property_cards)} property cards")

            for card in property_cards:
                try:
                    listing_url = card.get('href')
                    if not listing_url:
                        continue

                    if not listing_url.startswith('http'):
                        listing_url = f"https://www.boligportal.dk{listing_url}"

                    listing_id = self._extract_listing_id(listing_url)

                    # Debug information
                    print(f"Processing listing: {listing_id} - {listing_url}")

                    if listing_id not in self.seen_listings:
                        # Get basic information from the card
                        title = card.get_text().strip()

                        # Try to get price from the card
                        price_elem = card.select_one("[data-test='price']") or card.select_one(".css-1e8e3fr")
                        price = price_elem.text if price_elem else "Price not found"

                        details = {
                            'url': listing_url,
                            'id': listing_id,
                            'title': title,
                            'price': price,
                            'found_at': datetime.now().isoformat()
                        }

                        new_listings.append(details)
                        self.seen_listings.add(listing_id)
                        print(f"New listing found: {listing_id}")

                except Exception as e:
                    print(f"Error processing card: {str(e)}")
                    continue

            if new_listings:
                self._save_seen_listings()
                print(f"Found {len(new_listings)} new listings")
            else:
                print("No new listings found")

            return new_listings

        except Exception as e:
            print(f"Error fetching listings: {str(e)}")
            return []