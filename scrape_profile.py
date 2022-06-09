from src.profile_scraper import ProfileScraper


if __name__ == "__main__":

    scraper = ProfileScraper()

    Driver, proxy, args = scraper.setup()

    _ = scraper.scrape(driver=Driver, args=args, proxy=proxy, save_raw_data=True)
