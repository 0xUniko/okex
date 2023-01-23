import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.google.login_google import login_with_username_psw


def change_google_password(driver: Chrome, logger: Logger, account: str,
                           gmail_psw: str):
    logger.info('change google password')

    logger.info(
        'go to https://myaccount.google.com/signinoptions/password?continue=https%3A%2F%2Fmyaccount.google.com%2Fpersonal-info'
    )
    driver.get(
        r'https://myaccount.google.com/signinoptions/password?continue=https%3A%2F%2Fmyaccount.google.com%2Fpersonal-info'
    )
    if driver.current_url[:34] == 'https://accounts.google.com/signin':
        driver, logger = login_with_username_psw(driver, logger, account,
                                                 gmail_psw)

    new_gmail_psw = dotenv_values()['NEW_GMAIL_PASSWORD']

    WebDriverWait(driver, 10).until(lambda d: len(
        d.find_elements(By.CSS_SELECTOR, 'input[type="password"]')) == 2)

    password_inputs = driver.find_elements(By.CSS_SELECTOR,
                                           'input[type="password"]')
    password_inputs[0].send_keys(new_gmail_psw)
    password_inputs[1].send_keys(new_gmail_psw)
    logger.info('press confirm btn')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    time.sleep(3)

    return driver, logger
