import json
import logging
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


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger()

load_dotenv()


def main():
    nickname = os.getenv('NICKNAME')
    status_file_path = os.getenv('STATUS_PATH')
    formatted_datetime = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    status_file = f"{status_file_path}/{formatted_datetime}_{nickname}.json"

    options = FirefoxOptions()
    options.set_preference("layout.css.has-selector.enabled", True)
    if os.getenv('HEADLESS') == 'True':
        options.add_argument("--headless")
    delete_tweets = os.getenv('DELETE_TWEETS') == 'True'
    delete_replies = os.getenv('DELETE_REPLIES') == 'True'
    delete_retweets = os.getenv('DELETE_RETWEETS') == 'True'

    tweets, replies, retweets = get_tweets()
    f_tweets = date_filter(tweets)
    f_replies = date_filter(replies)
    f_retweets = date_filter(retweets)
    preview(
        len(tweets), len(replies), len(retweets),
        len(f_tweets), len(f_replies), len(f_retweets),
        delete_tweets, delete_replies, delete_retweets
    )
    autostart = os.getenv('AUTOSTART') == 'True'
    if not autostart:
        log.info(f'\nPress any key to continue...')
        input()
    form_status(status_file, nickname, 'starting', f_tweets, f_replies, f_retweets)

    log.info('')
    log.info(f'Starting driver...')
    driver = webdriver.Firefox(options=options)
    log.info('Driver started')
    log.info(f'Signing in...')
    login(driver)
    log.info('Signed in')

    if delete_tweets:
        log.info('')
        log.info(f'Removing tweets...')
        for i, t in enumerate(f_tweets, start=1):
            t.remove(driver)
            form_status(status_file, nickname, 'running', f_tweets, f_replies, f_retweets)
            log.info(f'  {t}  ({i}/{len(f_tweets)})')
    if delete_replies:
        log.info('')
        log.info(f'Removing replies...')
        for i, t in enumerate(f_replies, start=1):
            t.remove(driver)
            form_status(status_file, nickname, 'running', f_tweets, f_replies, f_retweets)
            log.info(f'  {t}  ({i}/{len(f_replies)})')
    if delete_retweets:
        log.info('')
        log.info(f'Removing retweets...')
        for i, t in enumerate(f_retweets, start=1):
            t.remove(driver)
            form_status(status_file, nickname, 'running', f_tweets, f_replies, f_retweets)
            log.info(f'  {t}  ({i}/{len(f_retweets)})')
    form_status(status_file, nickname, 'finished', f_tweets, f_replies, f_retweets)

    driver.close()


def preview(tweets_n, replies_n, retweets_n, f_tweets_n, f_replies_n, f_retweets_n, delete_tweets, delete_replies, delete_retweets):
    start_date_str = os.getenv('START_DATE')
    stop_date_str = os.getenv('STOP_DATE')
    log.info(f'Full backup:')
    log.info(f'  tweets: {tweets_n}')
    log.info(f'  replies: {replies_n}')
    log.info(f'  retweets: {retweets_n}')
    log.info(f'')
    log.info(f'Objects to remove ({start_date_str}..{stop_date_str}):')
    if delete_tweets:
        log.info(f'  tweets: {f_tweets_n}')
    if delete_replies:
        log.info(f'  replies: {f_replies_n}')
    if delete_retweets:
        log.info(f'  retweets: {f_retweets_n}')


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
    nickname = os.getenv('NICKNAME')
    backup_file = os.getenv('BACKUP_PATH')
    for t in tweets_list(backup_file):
        obj = Tweet(t, nickname)
        if obj.type == 'tweet':
            tweets.append(obj)
        elif obj.type == 'reply':
            replies.append(obj)
        else:
            retweets.append(obj)
    return tweets, replies, retweets


def form_status(status_file, username, status, tweets, replies, retweets):
    state = {
        'status': f'{status}',
        'username': f'{username}',
        'tweets': [{'id': p.id, 'status': p.status} for p in tweets],
        'replies': [{'id': p.id, 'status': p.status} for p in replies],
        'retweets': [{'id': p.id, 'status': p.status} for p in retweets]
    }
    with open(status_file, 'w') as json_file:
        json.dump(state, json_file, indent=2)


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
