""" Useragent rotator class"""
from fake_useragent import UserAgent


class UserAgentRotator:
    def __init__(self):
        pass

    @classmethod
    def set_random_ua(self, driver_options):

        ua = UserAgent()
        user_agent = {"User-Agent": str(ua.random)}
        driver_options.add_argument(f"user-agent={user_agent}")
