import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru._logger import Logger


def get_recharge_address(driver: Chrome, logger: Logger):
    logger.info('get recharge address')

    logger.info('go to https://www.okx.com/balance/recharge')
    driver.get('https://www.okx.com/balance/recharge')

    try:
        footer_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'okui-dialog-footer-box')))
        logger.info('system is busy')
        footer_box.find_element(By.TAG_NAME, 'button').click()
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'okui-dialog-footer-box')))
    except TimeoutException:
        pass

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'btn-content')) == 6)
    logger.info('select okb')
    driver.find_elements(By.CLASS_NAME, 'btn-content')[4].click()

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'okui-input-input')) == 2)
    logger.info('select network')
    driver.find_elements(By.CLASS_NAME, 'okui-input-input')[1].click()

    WebDriverWait(driver, 10).until(lambda d: len(
        d.find_elements(By.CLASS_NAME, 'options-label-detail')) == 2)
    logger.info('select okt network')
    driver.find_elements(By.CLASS_NAME, 'options-label-detail')[1].click()

    time.sleep(1)
    logger.info('click confirm')
    driver.find_element(By.CLASS_NAME, 'btn-content').click()

    time.sleep(2)
    logger.info('confirm the modal')
    driver.find_elements(By.CLASS_NAME, 'btn-content')[2].click()

    okb_recharge_addr = driver.find_element(By.CLASS_NAME, 'value').text

    logger.info('go to https://www.okx.com/balance/recharge')
    driver.get('https://www.okx.com/balance/recharge')
    # usdt

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'btn-content')) == 6)
    logger.info('select usdt')
    driver.find_elements(By.CLASS_NAME, 'btn-content')[0].click()

    try:
        footer_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'okui-dialog-footer-box')))
        logger.info('system is busy')
        footer_box.find_element(By.TAG_NAME, 'button').click()
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'okui-dialog-footer-box')))
    except TimeoutException:
        pass

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'okui-input-input')) == 2)
    logger.info('select network')
    driver.find_elements(By.CLASS_NAME, 'okui-input-input')[1].click()

    WebDriverWait(driver, 10).until(lambda d: len(
        d.find_elements(By.CLASS_NAME, 'options-label-detail')) == 5)
    logger.info('select okt')
    driver.find_elements(By.CLASS_NAME, 'options-label-detail')[2].click()

    time.sleep(1)
    logger.info('click confirm')
    driver.find_element(By.CLASS_NAME, 'btn-content').click()

    time.sleep(2)
    logger.info('confirm modal')
    driver.find_elements(By.CLASS_NAME, 'btn-content')[2].click()

    time.sleep(1)
    logger.info('check the address')
    driver.find_element(By.CLASS_NAME, 'value').click()
    WebDriverWait(driver, 10).until(lambda d: d.find_elements(
        By.CLASS_NAME, 'crypto-recharge-address-item'))
    logger.info('assert usdt and okt address is the same')
    assert okb_recharge_addr in [
        i.text for i in driver.find_elements(By.CLASS_NAME,
                                             'crypto-recharge-address-item')
    ]

    return driver, logger, okb_recharge_addr
