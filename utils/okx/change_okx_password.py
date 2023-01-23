import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import dotenv_values
from loguru._logger import Logger

from utils.okx.login_okx import login_okx
from utils.tools.authencator_calculator import calGoogleCode
from utils.google.login_google import login_gmail


def change_okx_password(driver: Chrome, logger: Logger, account: str,
                        okx_psw: str, qr_text: str):
    logger.info('change okx password')

    logger.info('go to https://www.okx.com/account/users/login-pwd/modify')
    driver.get('https://www.okx.com/account/users/login-pwd/modify')

    logger.info('input origin password')
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.NAME, 'password')).send_keys(okx_psw)

    default_okx_psw = dotenv_values()['DEFAULT_OKX_PASSWORD']
    logger.info('input new password')
    driver.find_element(By.NAME, 'passwordNew').send_keys(default_okx_psw)
    driver.find_element(By.NAME, 'passwordAgain').send_keys(default_okx_psw)

    logger.info('input authentication code')
    driver.find_element(By.CLASS_NAME, 'code-google').find_element(
        By.CSS_SELECTOR,
        'input[maxlength="6"]').send_keys(calGoogleCode(qr_text))

    logger.info('check the checkbox')
    driver.find_element(By.CLASS_NAME, 'okui-checkbox-input').click()

    code_email = driver.find_elements(By.CLASS_NAME, 'code-email')
    if code_email:
        logger.info("get gmail vericode")

        code_email[0].find_element(By.CLASS_NAME,
                                   'okui-input-code-btn').click()

        time.sleep(10)

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

        time.sleep(5)

        vericode = WebDriverWait(driver, 10).until(lambda d: d.find_element(
            By.CSS_SELECTOR,
            'div[style="letter-spacing:0.05em;margin:0 auto;width:90%;white-space:nowrap;font-style:normal;font-weight:700;text-align:center;font-family:SF Pro Text,SF Pro Icons,robot,Helvetica Neue,Helvetica,Arial,sans-serif;font-size:32px;line-height:36px;text-decoration-line:underline;color:#000000"]'
        )).text

        logger.info(f'vericode is {vericode}')
        logger.info('input vericode')

        driver.close()
        driver.switch_to.window(original_tab)

        driver.find_element(By.CLASS_NAME, 'code-email').find_element(
            By.TAG_NAME, 'input').send_keys(vericode)

    logger.info('press confirm btn')
    driver.find_element(By.CLASS_NAME, 'btn-content').click()

    WebDriverWait(driver, 10).until(
        lambda d: d.current_url == 'https://www.okx.com/account/login')

    return driver, logger
