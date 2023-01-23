import datetime, time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.google.get_gmail_vericode import get_gmail_vericode
from utils.tools.authencator_calculator import calGoogleCode


def create_api(driver: Chrome, logger: Logger, account: str, qr_text: str):
    logger.info('create okx api')

    logger.info('go to https://www.okx.com/account/my-api')
    driver.get('https://www.okx.com/account/my-api')

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.CLASS_NAME, 'sub-account-add')).click()

    logger.info('create api')
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == 'https://www.okx.com/account/my-api/create')

    logger.info('input api name')
    WebDriverWait(driver, 10).until(lambda d: d.find_element(
        By.CSS_SELECTOR, 'input[maxlength="100"]')).send_keys(
            str(datetime.date.today()))

    default_okx_psw = dotenv_values()['DEFAULT_OKX_PASSWORD']
    logger.info('input api password')
    driver.find_element(By.CSS_SELECTOR,
                        'input[type="password"]').send_keys(default_okx_psw)

    logger.info('check the checkboxes')
    checkbox = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    checkbox[1].click()
    checkbox[2].click()

    WebDriverWait(driver, 10).until(lambda d: d.find_element(
        By.CLASS_NAME, 'okui-input-code-btn')).click()

    driver, logger, vericode = get_gmail_vericode(driver, logger, account, 1)

    driver.find_element(By.CLASS_NAME, 'code-email').find_element(
        By.CSS_SELECTOR, 'input[maxlength="6"]').send_keys(vericode)
    driver.find_element(By.CLASS_NAME, 'code-google').find_element(
        By.CSS_SELECTOR,
        'input[maxlength="6"]').send_keys(calGoogleCode(qr_text))

    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'btn-content').click()

    info_items = WebDriverWait(
        driver,
        10).until(lambda d: d.find_elements(By.CLASS_NAME, 'info-item'))
    item_values = driver.find_elements(By.CLASS_NAME, 'item-value')
    api_key = item_values[0].text
    api_name = item_values[1].text
    secret_key = item_values[4].text

    return driver, logger, {
        'api_key': api_key,
        'api_name': api_name,
        'secret_key': secret_key
    }
