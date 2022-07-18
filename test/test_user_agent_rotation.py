from scripts.user_agents_rotator import UserAgent
from fake_useragent import UserAgent
import requests
from selenium import webdriver



def test_user_agent_setup():
    """ Testing correct user agent setup in Chrome driver using http://httpbin.org/headers as reference"""
    co = webdriver.ChromeOptions()
    ua = UserAgent()
    user_agent = {"User-Agent": str(ua.random)}
    co.add_argument(f'user-agent={user_agent}')
    r = requests.get('http://httpbin.org/headers', headers=user_agent)
    assert r.json()['headers']['User-Agent'] == co.arguments[0][27:-2]