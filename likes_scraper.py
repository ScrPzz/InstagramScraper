from scripts.argparser import ArgParser
from scripts.chrome_driver import ChromeDriver

# TODO change this values:
ig_usr='at85275'
ig_pass='ScrPzz*85'
query_hash='d5d763b1e2acf209d62d22d184488e57'



if __name__ == "__main__":

    args=ArgParser.likes_scraper_read_input()

    driver=ChromeDriver.set_up_driver()

    