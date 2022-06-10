from src.likes_scraper import LikesScraper

if __name__ == "__main__":

    scraper = LikesScraper()

    Driver, args = scraper.setup()

    scraper.scrape(driver=Driver, args=args)
