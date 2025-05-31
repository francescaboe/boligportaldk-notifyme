import time
import os
from datetime import datetime

from notifier import TelegramNotifier
from scraper import BoligScraper


def single_run():
    """Single execution run for Cloud Run job"""
    config_path = os.getenv('CONFIG_PATH', 'config/config.json')
    scraper = BoligScraper(config_path)
    notifier = TelegramNotifier()

    print(f"Starting single check of {scraper.config['search_url']}")
    print(f"Check started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        new_listings = scraper.get_new_listings()

        if new_listings:
            print(f"\nFound {len(new_listings)} new listings!")
            for listing in new_listings:
                print("\nNew listing found:")
                print(f"Rooms: {listing['rooms']} ({listing['size']} m²)")
                print(f"Location: {listing['city']}, {listing['street']}")
                print(f"Price: {listing['price']}")
                print(f"Listed: {listing['listing_age']}")
                print(f"URL: {listing['url']}")

                # Send Telegram notification
                if notifier.send_notification(listing):
                    print("✅ Telegram notification sent")
                else:
                    print("❌ Failed to send Telegram notification")

                print("-" * 50)
        else:
            print("\nNo new listings found in this check")

        print(f"\nCheck completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True

    except Exception as e:
        print(f"\nError in check: {str(e)}")
        return False


def cloud_run_with_internal_loop():
    """Run for a limited time with 30-second intervals in Cloud Run"""
    config_path = os.getenv('CONFIG_PATH', 'config/config.json')
    scraper = BoligScraper(config_path)
    notifier = TelegramNotifier()

    # Run for 10 minutes (20 checks at 30-second intervals)
    max_runtime_minutes = int(os.getenv('MAX_RUNTIME_MINUTES', '10'))
    max_checks = (max_runtime_minutes * 60) // 30

    print(f"Starting {max_checks} checks over {max_runtime_minutes} minutes")

    for i in range(max_checks):
        print(f"\n{'=' * 50}")
        print(f"Check {i + 1}/{max_checks} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 50}")

        try:
            new_listings = scraper.get_new_listings()

            if new_listings:
                print(f"\nFound {len(new_listings)} new listings!")
                for listing in new_listings:
                    print(f"New listing: {listing['rooms']} rm, {listing['city']}, {listing['price']}")

                    if notifier.send_notification(listing):
                        print("✅ Telegram notification sent")
                    else:
                        print("❌ Failed to send Telegram notification")
            else:
                print("No new listings found")

        except Exception as e:
            print(f"Error in check {i + 1}: {str(e)}")

        # Sleep for 30 seconds unless it's the last iteration
        if i < max_checks - 1:
            print(f"Waiting 30 seconds before next check...")
            time.sleep(30)

    print(f"\nCompleted all {max_checks} checks")
    return True


def continuous_run():
    """Continuous loop for local development"""
    scraper = BoligScraper('config/config.json')
    notifier = TelegramNotifier()

    print(f"Starting monitoring of {scraper.config['search_url']}")
    print(f"Will check every {scraper.config['check_interval']} seconds")

    try:
        while True:
            print(f"\n{'=' * 50}")
            print(f"Checking for new listings at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'=' * 50}")

            new_listings = scraper.get_new_listings()

            if new_listings:
                print(f"\nFound {len(new_listings)} new listings!")
                for listing in new_listings:
                    print("\nNew listing found:")
                    print(f"Rooms: {listing['rooms']} ({listing['size']} m²)")
                    print(f"Location: {listing['city']}, {listing['street']}")
                    print(f"Price: {listing['price']}")
                    print(f"Listed: {listing['listing_age']}")
                    print(f"URL: {listing['url']}")

                    # Send Telegram notification
                    if notifier.send_notification(listing):
                        print("✅ Telegram notification sent")
                    else:
                        print("❌ Failed to send Telegram notification")

                    print("-" * 50)
            else:
                print("\nNo new listings found in this check")

            print(f"\nWaiting {scraper.config['check_interval']} seconds before next check...")
            time.sleep(scraper.config['check_interval'])

    except KeyboardInterrupt:
        print("\nStopping the monitor...")
    except Exception as e:
        print(f"\nError in main loop: {str(e)}")


def main():
    # Determine which mode to run based on environment
    run_mode = os.getenv('RUN_MODE', 'continuous')  # 'single', 'loop', or 'continuous'

    if run_mode == 'single':
        # Single check and exit (for simple Cloud Run jobs)
        success = single_run()
        exit(0 if success else 1)
    elif run_mode == 'loop':
        # Multiple checks with 30-second intervals (for Cloud Run with internal timing)
        success = cloud_run_with_internal_loop()
        exit(0 if success else 1)
    else:
        # Continuous mode for local development
        continuous_run()


if __name__ == "__main__":
    main()
