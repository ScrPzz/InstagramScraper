""" Likes scraper class"""
import json
import logging
import os
import random
import urllib
from time import sleep

import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By

from scripts.argparser import ArgParser
from scripts.aux.misc_aux import extract_shortcode_from_url
from scripts.chrome_driver import ChromeDriver

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


class LikesScraper:
    def __init__(self):
        pass

    def raw_data_parser(self, likes_raw):
        R = []
        for j in range(0, len(likes_raw)):

            base = likes_raw[j]["data"]["shortcode_media"]["edge_liked_by"]["edges"]
            for i in range(0, len(base)):
                partial = []
                try:
                    try:
                        shortcode = base[i]["node"]
                        R.append(shortcode)
                    except:
                        pass
                except:
                    R.append(tuple(partial))
                    continue
        return pd.DataFrame(R)

    def setup(self):
        argparser = ArgParser()
        chrome_driver = ChromeDriver()

        args = argparser.likes_scraper_read_input()

        driver = chrome_driver.set_up_driver(proxy="")
        driver = chrome_driver.make_IG_access_w_creds(
            driver=driver, ig_usr=args.username, ig_pass=args.password
        )
        return driver, args

    def scrape(self, driver, args, **kwargs):

        query_hash = "d5d763b1e2acf209d62d22d184488e57"
        # Randomized time (seconds) to sleep for each iteration
        t = []
        for i in range(0, 20):
            t.append(np.round(random.uniform(7, 15), 2))

        # Randomized number of likes loaded for each iteration
        f = []
        for i in range(0, 20):
            f.append(np.round(random.uniform(12, 16), 2))

        short_code = extract_shortcode_from_url(args.target_post)
        likes_raw = []

        q_html = f"%22shortcode%22%3A%22{short_code}%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A{int(random.choice(f))}"
        u = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={{{q_html}}}"

        driver.get(u)
        content = driver.page_source
        content = driver.find_element(by=By.TAG_NAME, value="pre").text

        likes_raw.append(json.loads(content))

        parsed_json = json.loads(content)
        end_cursor = parsed_json["data"]["shortcode_media"]["edge_liked_by"][
            "page_info"
        ]["end_cursor"]
        has_next_page = parsed_json["data"]["shortcode_media"]["edge_liked_by"][
            "page_info"
        ]["has_next_page"]

        if "iterations" in kwargs.keys():
            n_iterations = kwargs["iterations"]
            if n_iterations == -1:
                n_iterations = 100
        else:
            n_iterations = 10

        go_on = True
        n_scraped = 0
        n = 0
        while go_on and n < n_iterations:
            if has_next_page and n < n_iterations:
                try:
                    print(n)
                    q_html = f'"shortcode"%3A"{short_code}"%2C"include_reel"%3A"true"%2C"first"%3A"{int(random.choice(f))}\
                        "%2C"after"%3A"{urllib.parse.quote_plus(str(end_cursor))}"'
                    u = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={{{q_html}}}"

                    sleep(int(random.choice(t)))
                    driver.get(u)
                    content = driver.page_source
                    content = driver.find_element(by=By.TAG_NAME, value="pre").text
                    parsed_json = json.loads(content)
                    likes_raw.append(json.loads(content))
                    end_cursor = parsed_json["data"]["shortcode_media"][
                        "edge_liked_by"
                    ]["page_info"]["end_cursor"]
                    has_next_page = parsed_json["data"]["shortcode_media"][
                        "edge_liked_by"
                    ]["page_info"]["has_next_page"]

                    n_scraped += f

                    n += 1
                    go_on = True
                    del content
                except:
                    n = n + 1

            else:
                go_on = False
                driver.close()
                # logging.info(f"Got {n_scraped} comments")

        data = self.raw_data_parser(likes_raw=likes_raw)

        if os.path.exists(args.output_folder):
            os.mkdir(f"{args.output_folder}/{short_code}")
        else:
            os.mkdir(args.output_folder)
            os.mkdir(f"{args.output_folder}/{short_code}")

        data.to_csv(f"{args.output_folder}/{short_code}/likes.csv", mode="w+")
        logging.info("Done!")
