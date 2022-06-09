from time import sleep

from scripts.chrome_driver import ChromeDriver
from src.likes_scraper import LikesScraper


class ArgSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_ig_reach():

    LikesScraper()
    args = ArgSpace(
        output_folder="./output",
        password="ScrPzz*85",
        target_post="https://www.instagram.com/p/Cbaz0iup69q/",
        username="at85275",
    )
    chrome_driver = ChromeDriver()
    _driver = chrome_driver.set_up_driver()
    _driver = chrome_driver.make_IG_access_w_creds(
        driver=_driver, ig_usr=args.username, ig_pass=args.password
    )
    sleep(2)
    _driver.get("https://www.instagram.com/p/Cbaz0iup69q/")
    assert _driver.current_url == "https://www.instagram.com/p/Cbaz0iup69q/"
    _driver.delete_all_cookies()
    _driver.quit()


def test_ig_basic_call_FAIL():
    """
    Test of the basic call (?__a=1) that allows to start scraping the profile.

    >>> If this test is green the scraping will fail! <<<

    """
    LikesScraper()
    args = ArgSpace(
        output_folder="./output",
        password="ScrPzz*85",
        target_post="https://www.instagram.com/valeyellow46/?__a=1",
        username="at85275",
    )
    chrome_driver = ChromeDriver()
    _driver = chrome_driver.set_up_driver(proxy="")
    _driver = chrome_driver.make_IG_access_w_creds(
        driver=_driver, ig_usr=args.username, ig_pass=args.password
    )
    sleep(2)
    _driver.get(args.target_post)
    content = _driver.page_source
    _driver.delete_all_cookies()
    _driver.quit()
    assert "Sorry, something went wrong" in content
