import os
from datetime import datetime
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Tweet:
    def __init__(self, tweet, login):
        self.id = tweet['id']
        self.login = login
        self.link = 'https://twitter.com/' + login + '/status/' + self.id
        self.created = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        if 'in_reply_to_status_id' in tweet:
            self.type = 'reply'
        elif 'possibly_sensitive' in tweet:
            self.type = 'tweet'
        else:
            self.type = 'retweet'
        self.status = 'unknown'  # 'unknown', 'exists', 'removed', 'max_attempts'

    def get_status(self, driver):
        def wait_for_any_element(drv, lctrs, timeout=int(os.getenv('WAIT'))):
            def any_element_present(drv_):
                for l, s in lctrs:
                    try:
                        e = drv_.find_element(*l)
                        if e:
                            return e, s
                    except NoSuchElementException:
                        pass
                return False
            return WebDriverWait(drv, timeout).until(any_element_present)

        exists = (By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        doesnt_exists = (By.XPATH, "//span[contains(text(), 'Hmm...this page doesn’t exist. Try searching for something else.')]")
        locators = [
            (exists, 'exists'),
            (doesnt_exists, 'removed')
        ]
        driver.get(self.link)
        element, status = wait_for_any_element(driver, locators)
        if element:
            return status
        else:
            return 'error'

    def remove(self, driver):
        wait = WebDriverWait(driver, int(os.getenv('WAIT')))
        attempts = int(os.getenv('MAX_ATTEMPTS'))
        while attempts > 0:
            self.status = self.get_status(driver)
            if self.status == 'removed':
                return

            if self.type == 'tweet':
                self.remove_tweet(wait)
            elif self.type == 'retweet':
                self.remove_retweet(wait)
            else:
                self.remove_reply(wait)
            sleep(int(os.getenv('MAX_ATTEMPTS')) + 1 - attempts)
            attempts -= 1
        self.status = 'max_attempts'

    def remove_tweet(self, wait):
        options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-label="More"]')))
        options.click()
        delete = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]')))
        delete.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]')))
        confirm.click()

    def remove_reply(self, wait):
        options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="cellInnerDiv"]:has(a[href="/{self.login}/status/{self.id}/quotes"]) div[aria-label="More"]')))
        options.click()
        delete = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]')))
        delete.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]')))
        confirm.click()

    def remove_retweet(self, wait):
        unretweet = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="unretweet"]')))
        unretweet.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="unretweetConfirm"]')))
        confirm.click()

    def __repr__(self):
        return f'{self.type} {self.id}, {self.status}'

    def __str__(self):
        return f'{self.type} {self.id} {self.status}'
