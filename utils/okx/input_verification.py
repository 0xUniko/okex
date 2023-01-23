import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from loguru._logger import Logger

from utils.tools.authencator_calculator import calGoogleCode


def input_verification(driver: Chrome, logger: Logger, vericode: str,
                       qr_text: str):
    logger.info('input vericode', vericode)
    WebDriverWait(driver, 10).until(lambda d: d.find_element(
        By.CLASS_NAME, 'okui-input-input')).send_keys(vericode)

    logger.info('input qr_text')
    inputs = driver.find_elements(By.CLASS_NAME, 'okui-input-input')

    [i for i in inputs
     if i.is_displayed()][1].send_keys(calGoogleCode(qr_text))

    return driver, logger
