import time
from random import random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru._logger import Logger

from utils.okx.input_verification import input_verification
from utils.google.get_gmail_vericode import get_gmail_vericode


def remove_devices(driver: Chrome, logger: Logger, account: str, qr_text: str):
    logger.info('remove okx devices')

    logger.info('go to https://www.okx.com/account/security')
    driver.get('https://www.okx.com/account/security')

    try:
        remove_btns = WebDriverWait(
            driver,
            10).until(lambda d: d.find_elements(By.CLASS_NAME, 'remove'))
    except TimeoutException:
        logger.info('nothing to remove')
        return driver, logger

    btns_amount = len(remove_btns)

    max_retries = 10

    while btns_amount > 1 and max_retries != 0:
        max_retries -= 1

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'remove')))

        driver.find_elements(By.CLASS_NAME, 'remove')[-1].click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'okui-input-code-btn'))).click()

        time.sleep(2)
        input_errors = driver.find_elements(By.CLASS_NAME, 'okui-input-error')
        if input_errors:
            logger.info('input error')
            time.sleep(30 + random() * 3)
            driver.find_element(By.CLASS_NAME, 'btn-outline-secondary').click()
            continue

        logger.info('get remove okx devices vericode')
        driver, logger, vericode = get_gmail_vericode(driver, logger, account,
                                                      6)

        driver, logger = input_verification(driver, logger, vericode, qr_text)

        time.sleep(1)
        logger.info('confirm')
        driver.find_elements(By.CLASS_NAME, 'btn-fill-highlight')[1].click()

        time.sleep(5)

        try:
            remove_btns = WebDriverWait(
                driver,
                10).until(lambda d: d.find_elements(By.CLASS_NAME, 'remove'))
        except TimeoutException:
            logger.info('nothing to remove')
            break

        btns_amount = len(remove_btns)

        if btns_amount > 1:
            time.sleep(30 + random() * 3)

    return driver, logger
