import os
from datetime import datetime

import pytz
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from load_backup import tweets_list
from selenium import webdriver
from tweet import Tweet

load_dotenv()


def main():
    options = FirefoxOptions()
    options.set_preference("layout.css.has-selector.enabled", True)
    # options.add_argument("--headless")
    tweets, replies, retweets = get_tweets()
    f_tweets = date_filter(tweets)
    f_replies = date_filter(replies)
    f_retweets = date_filter(retweets)
    preview(
        len(tweets),
        len(replies),
        len(retweets),
        len(f_tweets),
        len(f_replies),
        len(f_retweets)
    )

    autostart = os.getenv('AUTOSTART') == 'True'
    if not autostart:
        print(f'\nPress any key to continue...')
        input()

    driver = webdriver.Firefox(options=options)
    login(driver)

    print(f'\nRemoving tweets:')
    i = 1
    for t in f_tweets:
        t.remove(driver)
        print(f'  ({i}/{len(f_tweets)})  {t}')
        i += 1
    print(f'\nRemoving replies:')
    i = 1
    for t in f_replies:
        t.remove(driver)
        print(f'  ({i}/{len(f_replies)})  {t}')
        i += 1
    print(f'\nRemoving retweets:')
    i = 1
    for t in f_retweets:
        t.remove(driver)
        print(f'  ({i}/{len(f_retweets)})  {t}')
        i += 1

    driver.close()


def preview(tweets_n, replies_n, retweets_n, f_tweets_n, f_replies_n, f_retweets_n):
    start_date_str = os.getenv('START_DATE')
    stop_date_str = os.getenv('STOP_DATE')
    print(f'Full backup:')
    print(f'  tweets: {tweets_n}')
    print(f'  replies: {replies_n}')
    print(f'  retweets: {retweets_n}')
    print(f'\nObjects to remove ({start_date_str} - {stop_date_str})')
    print(f'  tweets: {f_tweets_n}')
    print(f'  replies: {f_replies_n}')
    print(f'  retweets: {f_retweets_n}')


def date_filter(objs):
    res = list()
    start_date = datetime.strptime(os.getenv('START_DATE'), '%Y-%m-%d')
    stop_date = datetime.strptime(os.getenv('STOP_DATE'), '%Y-%m-%d')
    local_timezone = pytz.timezone(os.getenv('TIMEZONE'))
    utc_start_date = local_timezone.localize(start_date).astimezone(pytz.utc)
    utc_stop_date = local_timezone.localize(stop_date).astimezone(pytz.utc)

    for o in objs:
        if utc_start_date <= o.created <= utc_stop_date:
            res.append(o)
    return res


def get_tweets():
    tweets = list()
    replies = list()
    retweets = list()
    login = os.getenv('NICKNAME')
    backup_file = os.getenv('BACKUP_PATH')
    for t in tweets_list(backup_file):
        obj = Tweet(t, login)
        if obj.type == 'tweet':
            tweets.append(obj)
        elif obj.type == 'reply':
            replies.append(obj)
        else:
            retweets.append(obj)
    return tweets, replies, retweets


def login(driver):
    nickname = os.getenv("NICKNAME")
    password = os.getenv("PASSWORD")
    wait = WebDriverWait(driver, 30) #!
    driver.get("https://twitter.com/i/flow/login")
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'input[autocomplete="username"]')))
    username.send_keys(f'{nickname}')
    username.send_keys(Keys.ENTER)
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'input[autocomplete="current-password"]')))
    username.send_keys(f'{password}')
    username.send_keys(Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href="/{nickname}"]')))


if __name__ == "__main__":
    main()
