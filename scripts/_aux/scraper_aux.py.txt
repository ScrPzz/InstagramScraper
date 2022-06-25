import logging
import os
import json


from scripts.aux.misc_aux import extract_shortcode_from_url

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


def save(data, target, args):

    check_or_create_folders(target=target, args=args)
    short_code = extract_shortcode_from_url(target)

    with open(f"{args.output_folder}/{short_code}/comments_raw.csv", "w+") as f:
        json.dump(data, f)
        logging.info("Raw data correctly saved/overwrote.")


def check_or_create_folders(target, args):

    short_code = extract_shortcode_from_url(target)

    if os.path.exists(args.output_folder):

        if os.path.exists(f"{args.output_folder}/{short_code}"):
            pass
        else:
            os.mkdir(f"{args.output_folder}/{short_code}")
    else:
        os.mkdir(args.output_folder)
        os.mkdir(f"{args.output_folder}/{short_code}")