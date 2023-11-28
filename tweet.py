from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class Tweet:
    def __init__(self, tweet, login):
        self.id = tweet['id']
        self.login = login
        self.link = f'https://twitter.com/{login}/status/{self.id}'
        self.created = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        if 'in_reply_to_status_id' in tweet:
            self.type = 'reply'
        elif 'possibly_sensitive' in tweet:
            self.type = 'tweet'
        else:
            self.type = 'retweet'
        self.status = 'unknown'  # 'unknown', 'exists', 'removed', 'max_attempts'
        self.delete_attempt = 3  # number of max delete attempts

    def get_status(self, driver):
        def wait_for_any_element(driver, locators, timeout=10):
            def any_element_present(drv):
                for locator, status in locators:
                    try:
                        element = drv.find_element(*locator)
                        if element:
                            return element, status
                    except NoSuchElementException:
                        pass
                return False
            return WebDriverWait(driver, timeout).until(any_element_present)

        locator1 = (By.CSS_SELECTOR, 'div[data-testid="tweetText"]')  # tweet exists
        locator2 = (By.CSS_SELECTOR, 'div[data-testid="error-detail"]')  # tweet didn't exists
        locators = [
            (locator1, 'exists'),
            (locator2, 'removed')
        ]

        driver.get(self.link)
        element, status = wait_for_any_element(driver, locators)
        if status == 'exists':
            return 'exists'
        elif status == 'removed':
            if element.text == 'Hmm...this page doesn’t exist. Try searching for something else.\nSearch':
                return 'removed'
            else:
                return 'error'
        else:
            return 'error'

    def remove(self, driver):
        wait = WebDriverWait(driver, 10) #!
        attempts = 3 #!
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
            sleep(4 - attempts) #!
            attempts -= 1
        self.status = 'max_attempts'

    def remove_tweet(self, wait):
        options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-label="More"]')))
        options.click()
        delete = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]')))
        delete.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]')))
        # confirm.click()

    def remove_reply(self, wait):
        options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="cellInnerDiv"]:has(a[href="/{self.login}/status/{self.id}/quotes"]) div[aria-label="More"]')))
        options.click()
        delete = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]')))
        delete.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]')))
        # confirm.click()

    def remove_retweet(self, wait):
        unretweet = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="unretweet"]')))
        unretweet.click()
        confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="unretweetConfirm"]')))
        # confirm.click()

    def __repr__(self):
        return f'{self.id}, {self.status}'

    def __str__(self):
        return f'{self.id} {self.type} {self.status}'
