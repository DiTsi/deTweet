import os
from time import sleep

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
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    tweets = get_tweets()

    login(driver)
    handle_tweets(driver, tweets)

    driver.close()


def handle_tweets(driver, tweets):
    # tabs = 10 #!

    # window_handles = driver.window_handles
    # driver.switch_to.window(window_handles[0])
    # driver.switch_to.window(window_handles[1])

    for t in tweets:
        t.remove(driver)
        print(t)


def get_tweets():
    tweets = list()
    login = os.getenv('NICKNAME')
    backup_file = os.getenv('BACKUP_PATH')
    for t in tweets_list(backup_file):
        tweets.append(Tweet(t, login))
    return tweets


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
