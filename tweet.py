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

    def get_status(self, driver):
        driver.get(self.link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="primaryColumn"]')))
        sleep(1) #!
        try:
            spans = driver.find_elements(By.CSS_SELECTOR, "span")
            search_text = 'Hmm...this page doesn’t exist. Try searching for something else.'
            found = False
            for span in spans:
                if span.text == search_text:
                    found = True
                    break
            if found:
                return 'removed'
            else:
                return 'error' #! 'exists'
        except NoSuchElementException:
            return 'exists'

    def set_status(self, status):
        self.status = status

    def remove(self, driver):
        attempts = 3
        wait = WebDriverWait(driver, 10)  # ожидание до 10 секунд
        if self.type == 'tweet':
            self.remove_tweet(driver, wait, attempts)
        elif self.type == 'retweet':
            self.remove_retweet(driver, wait, attempts)
        else:
            self.remove_reply(driver, wait, attempts)

    def remove_tweet(self, driver, wait, attempts):
        status = self.get_status(driver)
        self.set_status(status)
        while status != 'removed':
            options = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-label="More"]')))
            options.click()
            delete = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]')))
            delete.click()
            confirm = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]')))
            # confirm.click()

            status = self.get_status(driver)
            attempts -= 1
            if attempts == 0:
                self.status = 'max_attempts'
                break

    def remove_reply(self, driver, wait, attempts):
        status = self.get_status(driver)
        self.set_status(status)
        while status != 'removed':
            options = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, f'div[data-testid="cellInnerDiv"]:has(a[href="/{self.login}/status/{self.id}/quotes"]) div[aria-label="More"]'))
            options.click()
            delete = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, f'div[data-testid="Dropdown"] > div[role="menuitem"]'))
            delete.click()
            confirm = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, f'div[data-testid="confirmationSheetConfirm"]'))
            # confirm.click()

            status = self.get_status(driver)
            attempts -= 1
            if attempts == 0:
                self.status = 'max_attempts'
                break

    def remove_retweet(self, driver, wait, attempts):
        status = self.get_status(driver)
        self.set_status(status)
        while status != 'removed':
            unretweet = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, f'div[data-testid="unretweet"]'))
            unretweet.click()
            confirm = wait.until(EC.presence_of_element_located(By.CSS_SELECTOR, f'div[data-testid="unretweetConfirm"]'))
            # confirm.click()

            status = self.get_status(driver)
            attempts -= 1
            if attempts == 0:
                self.status = 'max_attempts'
                break

    def __repr__(self):
        return f'{self.id}, {self.status}'

    def __str__(self):
        return f'{self.id} {self.type} {self.status}'
