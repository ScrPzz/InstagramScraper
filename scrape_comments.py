from src.comments_scraper import CommentsScraper

if __name__ == "__main__":

    scraper = CommentsScraper()

    Driver, proxy, args = scraper.setup()

    raw_data = scraper.scrape(driver=Driver, args=args, proxy=proxy, save_raw_data=True)

    Driver.quit()

    _ = scraper.parse_and_save_data(raw_data=raw_data, args=args)
