import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from loguru._logger import Logger

from utils.google.get_gmail_vericode import get_gmail_vericode
from utils.okx.input_verification import input_verification


def change_authencator(
    driver: Chrome,
    logger: Logger,
    account: str,
):
    logger.info('change okx authencator')

    logger.info('go to https://www.okx.com/account/users/google/set')
    driver.get('https://www.okx.com/account/users/google/set')

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'qr-text')) == 3)

    WebDriverWait(driver, 10).until(
        lambda d: d.find_elements(By.CLASS_NAME, 'qr-text')[2].text[3:] != '')

    logger.info('click send vericode')
    driver.find_element(By.CLASS_NAME, 'okui-input-code-btn').click()

    logger.info('get authenticator code')
    qr_text = driver.find_elements(By.CLASS_NAME, 'qr-text')[2].text[3:]
    if not qr_text:
        raise Exception('fail to get qr text')
    logger.info(f'the qr_text is {qr_text}')

    logger.info('get_change_okx_authenticator_vericode')
    driver, logger, vericode = get_gmail_vericode(driver, logger, account, 1)

    driver, logger = input_verification(driver, logger, vericode, qr_text)
    driver.find_element(By.CLASS_NAME, 'item-confirm-btn').click()
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == 'https://www.okx.com/account/security')

    return driver, logger, qr_text
