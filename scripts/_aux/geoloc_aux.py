""" Geolocation update and fetch functions"""
import logging

import pandas as pd

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.CRITICAL
)


def fetch_country_code(country: str):
    """Function that extract country infos (lat, long and full name) from a country code string.
    If no match satisfying match is found, will choose a random location.
    Returns a dictionary having latitude, longitude and accuracy as keys.
    Accuracy is hardcoded to 100 [?]
    """

    geoloc_data = pd.read_csv("./data/geolocations.csv")
    if len(country) == 2:
        print(f"Trying to fetch country by code: {str.upper(country)}")

        try:
            country_data = geoloc_data[
                geoloc_data["country_code"] == str.upper(country)
            ]
            if ~country_data.empty:

                location_params = {
                    "latitude": float(country_data["latitude"]),
                    "longitude": float(country_data["longitude"]),
                    "accuracy": 100,
                }

                logging.info(f"Localized to: {country_data['country_name'].values[0]}")
            else:
                # Choosing a random location
                import random

                country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
                location_params = {
                    "latitude": float(country_data["latitude"]),
                    "longitude": float(country_data["longitude"]),
                    "accuracy": 100,
                }
                logging.info(
                    "... cannot find the requested location. Localizing to random location"
                )

        except:
            import random

            country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
            location_params = {
                "latitude": float(country_data["latitude"]),
                "longitude": float(country_data["longitude"]),
                "accuracy": 100,
            }
            logging.info(
                "... cannot find the requested location. Localizing to random location"
            )
    else:
        import random

        country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
        location_params = {
            "latitude": float(country_data["latitude"]),
            "longitude": float(country_data["longitude"]),
            "accuracy": 100,
        }
        logging.info(
            "... cannot find the requested location. Localizing to random location"
        )
    return location_params


def fetch_country_name(country: str):
    """Function that extract country infos (lat, long and full name) from a country name string.
    If no match satisfying match is found, will choose a random location.
    Returns a dictionary having latitude, longitude and accuracy as keys.
    Accuracy is hardcoded to 100 [?]
    """

    geoloc_data = pd.read_csv("./data/geolocations.csv")
    if len(country) > 2:
        print(f"Trying to fetch country by name: {country}...")

        try:
            from fuzzywuzzy import fuzz

            for name in list(geoloc_data["country_name"]):
                ratio = fuzz.ratio(country.lower(), name.lower())
                partial_ratio = fuzz.partial_ratio(country.lower(), name.lower())
                if ratio > 50 and partial_ratio > 80:
                    country_data = geoloc_data[geoloc_data["country_name"] == str(name)]
                    break

            if ~country_data.empty:

                location_params = {
                    "latitude": float(country_data["latitude"]),
                    "longitude": float(country_data["longitude"]),
                    "accuracy": 100,
                }

                print(
                    f"... found! Localized to: {country_data['country_name'].values[0]}"
                )
            else:
                # Choosing a random location
                import random

                country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
                location_params = {
                    "latitude": float(country_data["latitude"]),
                    "longitude": float(country_data["longitude"]),
                    "accuracy": 100,
                }
                print(
                    f"... cannot find the requested location. \
                        Localazing to random location: {country_data['country_name']}"
                )

        except:
            import random

            country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
            location_params = {
                "latitude": float(country_data["latitude"]),
                "longitude": float(country_data["longitude"]),
                "accuracy": 100,
            }
            print(
                f"Some error occurred while trying to fetch the provided location.\
                     Localazing to random location: {country_data['country_name']}"
            )

    else:
        import random

        country_data = geoloc_data.iloc[random.randrange(0, len(geoloc_data))]
        location_params = {
            "latitude": float(country_data["latitude"]),
            "longitude": float(country_data["longitude"]),
            "accuracy": 100,
        }
        print(
            f"Invalid country code or country name input. \
            Localizing to random location: {country_data['country_name']}"
        )
    return location_params