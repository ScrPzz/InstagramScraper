import os
from time import sleep

from scripts.auxiliary.misc_aux import parse_url_list_from_file
from scripts.chrome_driver import ChromeDriver
from src.comments_scraper import CommentsScraper


class ArgSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_comments_scraper_basic():
    scraper = CommentsScraper()

    args = ArgSpace(
        output_folder=os.getenv("OUTPUT_FOLDER"),
        username=os.getenv("TEST_IG_USER"),
        password=os.getenv("TEST_IG_PWD"),
        target_post=os.getenv("TEST_TARGET_POST"),
        max_iterations=1,
        # source_file='/home/atogni/Desktop/to_scrape/tests.csv'
    )  # max_iterations is set to 1 in order to not make too many calls and get IG angry

    chrome_driver = ChromeDriver()

    proxy = chrome_driver.set_up_proxy()
    Driver = chrome_driver.set_up_driver(proxy=proxy)
    Driver = chrome_driver.make_IG_access_w_creds(
        driver=Driver, ig_usr=args.username, ig_pass=args.password
    )
    sleep(2)
    raw_data = scraper.scrape(driver=Driver, proxy=proxy, args=args, save_raw_data=True)

    comments_df = scraper.parse_and_save_data(
        raw_data=raw_data, args=args, target=args.target_post
    )
    assert ~comments_df.empty
    Driver.quit()
    sleep(5)


def test_comments_scraper_by_source_file():
    scraper = CommentsScraper()

    args = ArgSpace(
        output_folder=os.getenv("OUTPUT_FOLDER"),
        username=os.getenv("TEST_IG_USER"),
        password=os.getenv("TEST_IG_PWD"),
        # target_post=os.getenv("TEST_TARGET_POST"),
        max_iterations=1,
        source_file="/home/atogni/Desktop/to_scrape/test_source_file.csv",
    )  # max_iterations is set to 1 in order to not make too many calls and get IG angry

    chrome_driver = ChromeDriver()

    proxy = chrome_driver.set_up_proxy()
    Driver = chrome_driver.set_up_driver(proxy=proxy)
    Driver = chrome_driver.make_IG_access_w_creds(
        driver=Driver, ig_usr=args.username, ig_pass=args.password
    )
    sleep(2)

    target_urls = parse_url_list_from_file(args.source_file)

    for url in target_urls:
        raw_data = scraper.scrape(
            driver=Driver,
            args=args,
            proxy=proxy,
            save_raw_data=True,
            target_post=url,
        )
        _ = scraper.parse_and_save_data(raw_data=raw_data, args=args, target=url)
        sleep(6)
    Driver.quit()
