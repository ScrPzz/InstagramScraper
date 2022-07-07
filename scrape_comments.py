"Single ore multiple post scraping for comments"


import time

from tqdm import tqdm

from scripts.auxiliary.misc_aux import parse_url_list_from_file
from src.comments_scraper import CommentsScraper

if __name__ == "__main__":

    scraper = CommentsScraper()
    # TODO add post images to the output folder
    Driver, proxy, args = scraper.setup()

    if args.source_file is None:

        raw_data = scraper.scrape(
            driver=Driver, args=args, proxy=proxy, save_raw_data=True
        )

        _ = scraper.parse_and_save_data(
            raw_data=raw_data, args=args, target=args.target_post
        )

        Driver.quit()
    else:
        target_urls = parse_url_list_from_file(args.source_file)
        for url in tqdm(target_urls):
            raw_data = scraper.scrape(
                driver=Driver,
                args=args,
                proxy=proxy,
                save_raw_data=True,
                target_post=url,
            )
            _ = scraper.parse_and_save_data(raw_data=raw_data, args=args, target=url)
            time.sleep(10)
        Driver.quit()
