import time, re
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.google.login_google import login_gmail


def get_gmail_vericode(driver: Chrome, logger: Logger, account: str,
                       paraph: int):
    time.sleep(10)

    logger.info('get gmail vericode')
    original_tab = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver, logger = login_gmail(driver, logger, account,
                                 dotenv_values()['NEW_GMAIL_PASSWORD'],
                                 dotenv_values()['NEW_RECOVERY_EMAIL'])

    WebDriverWait(driver, 10).until(lambda driver: (
        driver.current_url == 'https://mail.google.com/mail/u/0/#inbox' or
        driver.current_url == 'https://mail.google.com/mail/u/0/'))

    WebDriverWait(
        driver,
        10).until(lambda d: len(d.find_elements(By.TAG_NAME, 'tr')) > 6)

    time.sleep(5)

    logger.info('click the first mail in gmail')
    driver.find_elements(By.TAG_NAME, 'tr')[7].click()

    WebDriverWait(driver, 20).until(lambda d: len(
        d.find_elements(
            By.CSS_SELECTOR,
            'p[style="margin:0 auto;word-break:break-word;text-align:left;width:90%;font-family:SF Pro Text,SF Pro Icons,robot,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:14px;line-height:20px;font-weight:normal;color:#000000"]'
        )) >= paraph)

    time.sleep(5)

    logger.info('get vericode')

    vericode = re.search(
        '[0-9]{6}',
        driver.find_elements(
            By.CSS_SELECTOR,
            'p[style="margin:0 auto;word-break:break-word;text-align:left;width:90%;font-family:SF Pro Text,SF Pro Icons,robot,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:14px;line-height:20px;font-weight:normal;color:#000000"]'
        )[paraph].text).group(0)

    logger.info(f'vericode: {vericode}')

    driver.close()
    driver.switch_to.window(original_tab)

    return driver, logger, vericode
