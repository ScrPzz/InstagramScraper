from calendar import c
from src.likes_scraper import LikesScraper
from scripts.chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By
from time import sleep

class ArgSpace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    

def test_ig_reach():
    
    scraper=LikesScraper()
    args=ArgSpace(output_folder='./output', password='ScrPzz*85', target_post='https://www.instagram.com/p/Cbaz0iup69q/', username='at85275')
    chrome_driver=ChromeDriver()
    Driver=chrome_driver.set_up_driver()
    Driver=chrome_driver.make_IG_access(driver=Driver, ig_usr=args.username, ig_pass=args.password)
    sleep(2)
    Driver.get('https://www.instagram.com/p/Cbaz0iup69q/')
    assert Driver.current_url == 'https://www.instagram.com/p/Cbaz0iup69q/'
    Driver.delete_all_cookies()
    Driver.quit()



def test_ig_basic_call_FAIL():
    """
    Test of the basic call (?__a=1) that allows to start scraping the profile. 

    >>> If this test is green the scraping will fail! <<<

    """
    scraper=LikesScraper()
    args=ArgSpace(output_folder='./output', password='ScrPzz*85', target_post='https://www.instagram.com/valeyellow46/?__a=1', username='at85275')
    chrome_driver=ChromeDriver()
    Driver=chrome_driver.set_up_driver()
    Driver=chrome_driver.make_IG_access(driver=Driver, ig_usr=args.username, ig_pass=args.password)
    sleep(2)
    Driver.get(args.target_post)
    content = Driver.page_source
    Driver.delete_all_cookies()
    Driver.quit()
    assert 'Sorry, something went wrong' in content
    
