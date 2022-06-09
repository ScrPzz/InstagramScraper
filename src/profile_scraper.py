from email.contentmanager import raw_data_manager
import logging
from scripts.argparser import ArgParser
from scripts.aux.misc_aux import _finditem_nested_dict
from scripts.chrome_driver import ChromeDriver
from time import sleep
import numpy as np
import random
import json
import pandas as pd
import os
from urllib.parse import urlparse


logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


class ProfileScraper:
    def __init__(self):
        pass

    def parse_and_save_full_profile_raw_har(self, har, args):
        cols_to_keep = [
            "__typename",
            "id",
            "shortcode",
            "display_url",
            "owner",
            "is_video",
            "accessibility_caption",
            "video_url",
            "video_view_count",
            "edge_media_to_caption",
            "edge_media_to_comment",
            "nft_asset_info",
            "product_type",
            "edge_liked_by",
        ]

        raw_data = []
        for n in range(0, len(har["log"]["entries"])):
            if "text" in har["log"]["entries"][n]["response"]["content"].keys():
                if (
                    "edge_owner_to_timeline_media"
                    in har["log"]["entries"][n]["response"]["content"]["text"]
                ):
                    raw_data.append(
                        _finditem_nested_dict(
                            json.loads(
                                har["log"]["entries"][n]["response"]["content"]["text"]
                            ),
                            "edge_owner_to_timeline_media",
                        )
                    )
        data = []
        for i in range(0, len(raw_data)):
            aux = _finditem_nested_dict(raw_data[i], "edges")
            data.append(aux)
        D = []
        for d in data:
            for n, v in enumerate(d):
                D.append(_finditem_nested_dict(v, "node"))

        # Write cleaned data to disk
        profile_short_url = urlparse(args.target_profile).path.strip("/")
        """if os.path.exists(args.output_folder):
                os.mkdir(f'{args.output_folder}/{profile_short_url}')
                pass
        else:
            os.mkdir(args.output_folder)
            os.mkdir(f'{args.output_folder}/{profile_short_url}')"""

        with open(
            f"{args.output_folder}/{profile_short_url}/full_clean.csv", "w+"
        ) as f:
            pd.DataFrame(D)[cols_to_keep].to_csv(f)
            logging.info("Raw data correctly saved/overwrote.")

        return pd.DataFrame(D)[cols_to_keep]

    def setup(self):
        argparser = ArgParser()
        chrome_driver = ChromeDriver()
        proxy = chrome_driver.set_up_proxy()
        args = argparser.profile_scraper_read_input()

        driver = chrome_driver.set_up_driver(proxy=proxy)
        self.driver = driver
        driver = chrome_driver.make_IG_access(
            driver=driver, ig_usr=args.username, ig_pass=args.password
        )
        return driver, proxy, args

    def scrape(self, driver, proxy, args, save_raw_data=bool):
        proxy.new_har(
            args.target_profile,
            options={"captureHeaders": True, "captureContent": True},
        )
        driver.get(args.target_profile)

        # Random time intervals to sleep between scrolls
        ttw = []
        for i in range(0, 20):
            ttw.append(np.round(random.uniform(5, 10), 2))

        ## 12 posts loaded each scroll
        MAX_SCROLLS = int(args.max_iterations)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        n_iter = 0
        while True and n_iter <= MAX_SCROLLS:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(int(random.choice(ttw)))

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            n_iter += 1

        sleep(5)
        raw_data = proxy.har
        driver.quit()

        # Write raw data to disk
        profile_short_url = urlparse(args.target_profile).path.strip("/")
        if save_raw_data:
            if os.path.exists(args.output_folder):
                if os.path.exists(f"{args.output_folder}/{profile_short_url}"):
                    pass
                else:
                    os.mkdir(f"{args.output_folder}/{profile_short_url}")
            else:
                os.mkdir(args.output_folder)
                os.mkdir(f"{args.output_folder}/{profile_short_url}")

        with open(f"{args.output_folder}/{profile_short_url}/full_raw.csv", "w+") as f:
            json.dump(proxy.har, f)
            logging.info("Raw data correctly saved/overwrote.")

        _ = self.parse_and_save_full_profile_raw_har(har=raw_data, args=args)

        return
