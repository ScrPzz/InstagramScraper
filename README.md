# Instagram scraper

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

I present you a Python tool that allows you to scrape profile informations, likes and comments from Instagram.
Remember that scraping is a potentially illegal activity. This tool allows you to scrape, but the author does not encourage you to do it, nor to retain or sell scraped data.

## Setting up the project

Clone the project:

``` git clone git@github.com:ScrPzz/IG_scraper.git ```

Install the requirements:

``` pip install -r requirements.txt ```

Go to the project folder and run:

```python setup.py develop```

I suggest you not to use your personal IG account to leverage this tool: IG policies are pretty strict and variable and your profile is not unlikely to be banned, even if temporarily. As of today (June 7th 2022) the limit of calls to the IG apis seems to be 200/hour. A rule of thumb:

- access to a post ~ 1 call

- 1 iteration ~ 1 call

- 12 post loaded ~ 1 call

All the scripts got some `sleep` with random and fixed values to not spam calls too fast and the db requests too are randomized, but i strongly suggest you to not be greedy. Go slow!

## Likes scraper

This tool extract infos about the users that gave like to a certain post. Due to IG policies only a limited number of likes are visible (you cannot scroll the full likes list). I'm not sure if it is a fixed percentage of the total number of likes or a fixed number. Anyway, you'll be able to scrape some thousands and that's allow you to extract some kind of statistics.

To start the tool quickly go to the project folder and run:

``` python scrape_likes.py -u {IG_USER} -p {IG_PASS} -t {POST_FULL_URL} ```

this will get you *roughly* 70 likes, if available.

Optional args are:

- `output folder`: i'll let you guess the meaning of that one by yourself. Default is `./output`
- `max_iterations`: max number of *scrolls*, each scroll meaning *roughly* 12-15 likes. Default is 5.

Output will be a pandas dataframe written to a csv file and saved on the choosen output folder.

Columns names are pretty self-explanatory, but may vary in time.

## Comments scraper

This tool extract infos about the users that commented a certain post.

To start the tool quickly go to the project folder and run:

``` python scrape_comments.py -u {IG_USER} -p {IG_PASS} -t {POST_FULL_URL} ```

this will get you *roughly* 100 likes, if available.

Optional args are:

- `output folder`: i'll let you guess the meaning of that one by yourself. Default is `./output`
- `max_iterations`: max number of *scrolls*, each scroll meaning *roughly* 24 comments. Default is 5.

Output will be a pandas dataframe written to a csv file and saved on the choosen output folder.
Columns names are pretty self-explanatory, but may change in time.

## Profile scraper

This last tool allows you to scrape infos about all the posts that belongs to a profile.

To start the tool quickly go to the project folder and run:

``` python scrape_profile.py -u {IG_USER} -p {IG_PASS} -t {POST_FULL_URL} ```

this will get you *roughly* 40 posts infos, if available.

Optional args are:

- `output folder`: i'll let you guess the meaning of that one by yourself. Default is `./output`
- `max_iterations`: max number of *scrolls*, each scroll meaning *roughly* 24 comments. Default is 3.

Output will be a pandas dataframe written to a csv file and saved on the choosen output folder.

## Tests

There basic are tests units for each tool and to check the accessibility of Instagram by Selenoum. More to come.
Remember that also tests will make calls. I suggest you to run only the test you need and not the whole test suite at a time.

## Known issues

### Browser stuck at cookies wall

During the scraping you will be able to see all the steps on a Chrome window driven by Selenium. If you see the browser stuck on "cookies wall" for more that 7-8 seconds, please consider to kill the process and start a new one. As today i don't know why this happens, i suspect because of some cookies/cache stuff, but cannot find a stable solution.

### Imports

In case after installing webdriver_manager and browsermob-proxy via pip:

```pip install webdriver_manager```

```pip install browsermob-proxy```

you get an import error, try intalling the libs this way:

```python3.8 -m pip install webdriver_manager```

```python3.8 -m pip install browsermob-proxy```

## Collaboration

Everyone is warmly invited to suggest changes, fixes, new functionalities, ecc. Just create a pull request!

## TODO

### Urgent

- Login via session ID

- Add multiple post option for comments scraper ✔️

- Add multiple post option for likes scraper

- Download all the images from multi-images posts (now i'm downloading only the first one)

- User agent rotator onboarding

- MAC address spoofer creation

- Geolocation spoofer onboarding

- Add deep scrape functionality

- Containerize

### Secondary

- Improve the docs

- Unify the parsing methods

- Create a folder for each post and profile ✔️

- Extract location
