import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.google.login_google import login_with_username_psw
from utils.outlook.recovery_email import get_recovery_vericode


def change_recovery_email(driver: Chrome, logger: Logger, account: str,
                          gmail_psw: str):
    logger.info('change recovery email')
    new_recovery_email = dotenv_values()['NEW_RECOVERY_EMAIL']

    logger.info('go to recovery email')
    driver.get('https://myaccount.google.com/recovery/email')
    time.sleep(2)

    if driver.current_url[:34] == 'https://accounts.google.com/signin':
        driver, logger = login_with_username_psw(driver, logger, account,
                                                 gmail_psw)

    logger.info('enter new recovery email')
    i5 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'i5')))
    time.sleep(1)
    i5.clear()
    i5.send_keys(new_recovery_email)

    driver.find_elements(By.TAG_NAME, 'button')[6].click()

    time.sleep(10)

    logger.info('get vericode')
    is_latest_code, vericode = get_recovery_vericode()
    logger.info(f'the vericode is {vericode}')
    if not is_latest_code:
        logger.info('it is not the latest vericode')
        driver.find_elements(By.CSS_SELECTOR, 'a[role="button"]')[2].click()
        time.sleep(10)
        is_latest_code, vericode = get_recovery_vericode()
        logger.info('the vericode is ', vericode)
        if not is_latest_code:
            logger.info('it is not the latest vericode')
            raise Exception('error vericode')

    driver.find_element(By.ID, 'c2').send_keys(vericode)
    driver.find_elements(By.TAG_NAME, 'button')[8].click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, 'div[role="dialog"]')))

    time.sleep(2)

    logger.info('change recovery email succeeds')

    return driver, logger
