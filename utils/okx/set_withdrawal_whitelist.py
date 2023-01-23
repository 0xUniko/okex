import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.google.get_gmail_vericode import get_gmail_vericode
from utils.tools.authencator_calculator import calGoogleCode


def set_withdrawal_whitelist(driver: Chrome, logger: Logger, account: str,
                             qr_text: str):
    logger.info('set withdrawal whitelist')

    logger.info('go to https://www.okx.com/balance/withdrawal-address/okb/184')
    driver.get('https://www.okx.com/balance/withdrawal-address/okb/184')

    time.sleep(3)

    WebDriverWait(
        driver,
        10).until(lambda d: d.find_element(By.CLASS_NAME, 'add')).click()

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'okui-input-input')) == 4)
    driver.find_elements(By.CLASS_NAME, 'okui-input-input')[1].click()

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'okui-select-item')) == 2)
    driver.find_elements(By.CLASS_NAME, 'okui-select-item')[1].click()

    time.sleep(1)
    driver.find_elements(By.CLASS_NAME, 'okui-input-input')[2].send_keys(
        dotenv_values()['WITHDRAWAL_ADDRESS'])
    for checkbox in driver.find_elements(By.CSS_SELECTOR,
                                         'input[type="checkbox"]'):
        checkbox.click()

    WebDriverWait(driver, 10).until(lambda d: len(
        d.find_elements(By.CLASS_NAME, 'okui-input-code-btn')) == 2)
    driver.find_element(By.CLASS_NAME, 'okui-input-code-btn').click()

    driver, logger, vericode = get_gmail_vericode(driver, logger, account, 1)

    driver.find_element(By.CSS_SELECTOR,
                        'input[maxlength="6"]').send_keys(vericode)
    driver.find_elements(By.CSS_SELECTOR, 'input[maxlength="6"]')[2].send_keys(
        calGoogleCode(qr_text))

    driver.find_elements(By.CLASS_NAME, 'btn-content')[1].click()

    time.sleep(2)

    return driver, logger
