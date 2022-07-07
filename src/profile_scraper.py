""" Full profile scraper class"""
import json
import logging
import os
import random
import urllib.request
from time import sleep
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from scripts.argparser import ArgParser
from scripts.auxiliary.misc_aux import _finditem_nested_dict
from scripts.chrome_driver import ChromeDriver

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


# TODO: check if a post is Sidecar (multiple images) and save the images on a separated folder.


class ProfileScraper:
    def __init__(self):
        pass

    @staticmethod
    def _iterate(args, driver, ttw):  ## 12 posts loaded each scroll

        MAX_SCROLLS = int(args.max_iterations)

        last_height = driver.execute_script("return document.body.scrollHeight")
        n_iter = 0
        while True and n_iter <= MAX_SCROLLS:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(int(random.choice(ttw)))

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            n_iter += 1

    @classmethod
    def parse_and_save_full_profile_raw_har(self, har, args):
        """Function that parse and save the raw har file scraped"""
        cols_to_keep = [
            "__typename",
            "id",
            "taken_at_timestamp",
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
            "edge_sidecar_to_children",
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

        with open(
            f"{args.output_folder}/{profile_short_url}/full_clean.csv", "w+"
        ) as f:
            pd.DataFrame(D)[cols_to_keep].to_csv(f)
            logging.info("Raw data correctly saved/overwrote.")

        return pd.DataFrame(D)[cols_to_keep]

    @classmethod
    def setup(self):
        """Function that setup the driver and access IG"""
        argparser = ArgParser()
        chrome_driver = ChromeDriver()
        proxy = chrome_driver.set_up_proxy()
        args = argparser.profile_scraper_read_input()

        driver = chrome_driver.set_up_driver(proxy=proxy)
        driver = chrome_driver.make_IG_access_w_creds(
            driver=driver, ig_usr=args.username, ig_pass=args.password
        )
        return driver, proxy, args

    @classmethod
    def scrape(self, driver, proxy, args, save_raw_data=bool, download_imgs=bool):
        """Function that make the proper scraping"""
        proxy.new_har(
            args.target_profile,
            options={"captureHeaders": True, "captureContent": True},
        )
        driver.get(args.target_profile)

        # Random time intervals to sleep between scrolls
        ttw = []
        for i in range(0, 20):
            ttw.append(np.round(random.uniform(5, 10), 2))

        ProfileScraper._iterate(args=args, driver=driver, ttw=ttw)

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

        profile_infos_df = self.parse_and_save_full_profile_raw_har(
            har=raw_data, args=args
        )

        if download_imgs:
            ProfileScraper.download_images(
                args, profile_infos_df, profile_short_url=profile_short_url
            )

        return raw_data

    @staticmethod
    def download_images(args, df, profile_short_url):
        """Save posts images:
        - Single post images using the shortcode as image name;
        - Sidecar post (multiple images posts): shortcode as folder name"""

        def _parse_sidecar_data(shortcode_to_data):
            """Auxiliary function that returns a dict:
            {'shortcode': [list of direct urls]}"""
            parsed_sidecar_data = {}
            for k, v in short_code_to_url_sidecar.items():
                if isinstance(v, dict):
                    _v = []
                    for n in range(0, len(v["edges"])):
                        _v.append(v["edges"][n]["node"]["display_url"])
                    parsed_sidecar_data.update({k: _v})

            return parsed_sidecar_data

        base_profile_url = f"{args.output_folder}/{profile_short_url}"
        short_code_to_url_single_post = dict(
            zip(list(df["shortcode"]), list(df["display_url"]))
        )

        short_code_to_url_sidecar = dict(
            zip(list(df["shortcode"]), list(df["edge_sidecar_to_children"]))
        )
        short_code_to_url_sidecar = _parse_sidecar_data(short_code_to_url_sidecar)

        if os.path.exists(f"{base_profile_url}/post_imgs"):  # Images folder creation
            pass
        else:
            os.mkdir(f"{base_profile_url}/post_imgs")

        for k, v in short_code_to_url_sidecar.items():  # Saving single posts imgs
            if os.path.exists(f"{base_profile_url}/post_imgs/{k}"):
                pass
            else:
                os.mkdir(f"{base_profile_url}/post_imgs/{k}")
            n = 0
            for img_url in v:
                urllib.request.urlretrieve(
                    img_url, f"{base_profile_url}/post_imgs/{k}/{k}_{n}.jpg"
                )
                n += 1

        for img in short_code_to_url_single_post.items():  # Saving single posts imgs
            urllib.request.urlretrieve(
                img[1], f"{base_profile_url}/post_imgs/{img[0]}.jpg"
            )

        with open(
            f"{base_profile_url}/images_direct_urls.json", "w+"
        ) as f:  # saving the full shortcode to url data
            short_code_to_url_single_post.update(short_code_to_url_sidecar)
            json.dump(short_code_to_url_single_post, f)
