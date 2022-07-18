""" Comments scraper class"""
import json
import logging
import random
from time import sleep

import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scripts.argparser import ArgParser
from scripts.auxiliary.scraper_aux import check_or_create_folders, save
from scripts.chrome_driver import ChromeDriver

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


class CommentsScraper:
    def __init__(self):
        pass

    @staticmethod
    def iterate(args, ttw, driver):
        # ~ 24 comments loaded each iteration
        check = True
        MAX_ITER = int(args.max_iterations)
        n = 0

        while check and n <= MAX_ITER:
            sleep(int(random.choice(ttw)))

            try:
                load_more_comments_button = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "[aria-label='Load more comments']")
                    )
                )
                load_more_comments_button.click()
            except:
                check = False
                if n == MAX_ITER:
                    logging.warning(
                        "Reached the max iterations number before exhausting the post comments. \
                            You may consider to raise the max iterations number"
                    )
                else:
                    logging.info("Exhausted all the post comments")
            n = n + 1

    @classmethod
    def setup(self):
        argparser = ArgParser()
        chrome_driver = ChromeDriver()
        proxy = chrome_driver.set_up_proxy()

        args = argparser.likes_scraper_read_input()

        driver = chrome_driver.set_up_driver(proxy=proxy)
        driver = chrome_driver.make_IG_access_w_creds(
            driver=driver, ig_usr=args.username, ig_pass=args.password
        )
        return driver, proxy, args

    @classmethod
    def scrape(self, driver, proxy, args, save_raw_data=bool, **kwargs):

        if "target_post" in kwargs:
            proxy.new_har(
                kwargs.get("target_post"),
                options={"captureHeaders": True, "captureContent": True},
            )
            driver.get(kwargs.get("target_post"))
            target = kwargs.get("target_post")
        else:
            proxy.new_har(
                args.target_post,
                options={"captureHeaders": True, "captureContent": True},
            )
            driver.get(args.target_post)
            target = args.target_post

        # Random time intervals to sleep between load more comment button pushes
        ttw = []
        for i in range(0, 20):
            ttw.append(np.round(random.uniform(4, 8), 2))

        # ~ 24 comments loaded each iteration
        CommentsScraper.iterate(args=args, ttw=ttw, driver=driver)

        R = json.loads(json.dumps(proxy.har, ensure_ascii=False))

        if save_raw_data:
            save(data=R, target=target, args=args)

        return R

    @classmethod
    def parse_and_save_data(self, raw_data, args, target):
        "Parse raw scraped data and write to disk"

        RAW = {}
        for n, v in enumerate(raw_data["log"]["entries"]):
            if v["response"]["content"]["mimeType"] in [
                "application/json; charset=utf-8",
                "application/json",
            ]:
                try:
                    RAW[n] = json.loads(v["response"]["content"]["text"])["comments"]
                except:
                    pass

        comments_df = pd.DataFrame.from_dict(RAW[list(RAW.keys())[0]])

        for k in list(RAW.keys())[1:]:
            comments_df = pd.concat([comments_df, pd.DataFrame.from_dict(RAW[k])])

        comments_df = comments_df.reset_index(drop=True)

        check_or_create_folders(target=target, args=args)

        short_code = target.split("/")[-1]

        # TODO FIX get the profile name from somewhere and create the correct folder!
        comments_df.to_csv(
            f"{args.output_folder}/{short_code}_comments_clean.csv", mode="w+"
        )
        logging.info("Data correctly saved/overwrote.")
        # print(f'Dave saved in: {f"{args.output_folder}_{short_code}_comments_clean.csv"}')
        return comments_df
