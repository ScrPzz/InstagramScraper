from src.profile_scraper import ProfileScraper

if __name__ == "__main__":

    scraper = ProfileScraper()

    Driver, proxy, args = scraper.setup()

    _ = scraper.scrape(driver=Driver, args=args, proxy=proxy, save_raw_data=True)

    # TODO Save post urls to txt:

    # import pandas as pd

    # i=pd.read_csv('/home/atogni/_projects/IG_scraper/output/oceana/full_clean.csv')

    # i.shortcode=i.shortcode.apply(lambda x: 'https://www.instagram.com/p/'+x )

    # i.shortcode.to_csv('/home/atogni/_projects/IG_scraper/output/oceana/post_codes.txt',index=False, header=False)
