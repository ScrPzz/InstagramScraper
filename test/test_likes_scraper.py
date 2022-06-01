from src.likes_scraper import LikesScraper




class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    

def test_ig_reach():
    
    scraper=LikesScraper()
    args=Namespace(output_folder='./output', password='ScrPzz*85', target_post='https://www.instagram.com/p/Cbaz0iup69q/', username='at85275')
    Driver, _ = scraper.setup()
    scraper.scrape(driver=Driver, args=args)