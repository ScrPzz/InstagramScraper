import logging
from scripts.argparser import ArgParser
from scripts.aux.misc_aux import extract_shortcode_from_url
from scripts.chrome_driver import ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import numpy as np
import random
import json
import pandas as pd
import os

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.CRITICAL)



class CommentsScraper():
    def __init__(self):
        pass

    def setup(self):
        argparser=ArgParser()
        chrome_driver=ChromeDriver()
        proxy=chrome_driver.set_up_proxy()

        args=argparser.likes_scraper_read_input()
        
        driver=chrome_driver.set_up_driver(proxy=proxy)
        driver=chrome_driver.make_IG_access(driver=driver, ig_usr=args.username, ig_pass=args.password)
        return driver, proxy, args

    def scrape(self, driver, proxy, args, save_raw_data=bool):
        proxy.new_har(args.target_post, options={'captureHeaders': True, 'captureContent':True})
        driver.get(args.target_post) 

        # Random time intervals to sleep between load more comment button pushes
        ttw=[]
        for i in range(0,20):
            ttw.append(np.round(random.uniform(2, 4), 2))

        ## 24 comments loaded each iteration
        check=True
        MAX_ITER=int(args.max_iterations)
        n=0
        #har_parts=[]
        while check and n<= MAX_ITER:
            sleep(int(random.choice(ttw)))
            
            try:
                load_more_comments_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Load more comments']")))
                load_more_comments_button.click()
                #har_parts.append(proxy.har)
            except: 
                check=False
                if n==MAX_ITER:
                    logging.warning('Reached the max iterations number before exhausting the post comments. You may consider to raise the max iterations number')
                else:
                    logging.info('Exhausted all the post comments')
            n=n+1

        driver.quit()
        R=json.loads(json.dumps(proxy.har, ensure_ascii=False))

        if save_raw_data:
            if os.path.exists(args.output_folder):
                pass
            else:
                os.mkdir(args.output_folder)
            short_code=extract_shortcode_from_url(args.target_post)
            with open(f'{args.output_folder}/{short_code}_comments_raw.csv', 'w+') as f:
                json.dump(R, f)
                logging.info('Raw data correctly saved/overwrote.')
        return R


    def parse_and_save_data(self, raw_data, args):
        RAW={}
        for n, v in enumerate(raw_data['log']['entries']):
            if v['response']['content']['mimeType'] in ['application/json; charset=utf-8', 'application/json']:
                try:
                    RAW[n]=json.loads(v['response']['content']['text'])['comments']
                except:
                    pass

        comments_df=pd.DataFrame.from_dict(RAW[list(RAW.keys())[0]])
        for k in list(RAW.keys())[1:]:
            comments_df=pd.concat([comments_df, pd.DataFrame.from_dict(RAW[k])])

        comments_df=comments_df.reset_index(drop=True)

        if os.path.exists(args.output_folder):
                logging.info('Output folder already exist')
                pass
        else:
            os.mkdir(args.output_folder)
        short_code=extract_shortcode_from_url(args.target_post)

        comments_df.to_csv(f'{args.output_folder}/{short_code}_comments_clean.csv', mode='w+')
        logging.info('Data correctly saved/overwrote.')
        return comments_df
        