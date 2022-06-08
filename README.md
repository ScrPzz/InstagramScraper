# Instagram scraper

A Python setup to scrape posts infos, likes and comments from Instagram.

## Setup the project

run: python setup.py develop

## TODO

RIcordati di aggiungere queste known issues:
Se fallisce l'import di webdrivere_manager con pip install webdriver_manager:

python3.8 -m pip install webdriver_manager
IDEM per python3.8 -m pip install browsermob-proxy

### User agent rotator

Known issues:

- Some useragents features browser versions that can produce "Not supported anymore" message,
    but that does not seems to affect the results.
