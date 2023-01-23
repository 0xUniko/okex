import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from loguru._logger import Logger

from utils.tools.authencator_calculator import calGoogleCode


def login_okx(driver: Chrome,
              logger: Logger,
              account: str,
              okx_psw: str,
              qr_text: str = ''):
    logger.info('login okx')

    logger.info('go to https://www.okx.com/account/login')
    driver.get('https://www.okx.com/account/login')

    if driver.find_elements(By.CLASS_NAME, 'okui-input-input'):
        logger.info('enter username')
        usrname_input = driver.find_element(By.CLASS_NAME, 'okui-input-input')
        usrname_input.clear()
        usrname_input.send_keys(account)

        logger.info('enter password')
        psw_input = driver.find_element(By.CSS_SELECTOR,
                                        'input[data-testid="login-password"]')
        psw_input.clear()
        psw_input.send_keys(okx_psw)

        for _ in range(3):
            logger.info('press login btn')
            driver.find_element(By.CSS_SELECTOR, '#login-submit-btn').click()

            has_captcha = True
            try:
                logger.info('waiting for captcha')
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, 'geetest_box_wrap')))
            except TimeoutException:
                has_captcha = False
                pass

            if has_captcha:
                WebDriverWait(driver, 3600).until(
                    EC.invisibility_of_element_located(
                        (By.CLASS_NAME, 'geetest_box_wrap')))

                time.sleep(2)

                if driver.find_elements(By.CLASS_NAME, 'okui-input-input'):
                    logger.error('captcha fails')
                    continue

                logger.info('captcha succeed')

            if qr_text:
                try:
                    code_inputs = WebDriverWait(driver, 10).until(
                        lambda d: d.find_elements(By.CLASS_NAME, 'code-input'))
                    # code_inputs = driver.find_elements(By.CLASS_NAME, 'code-input')
                    if len(code_inputs) == 6:
                        authcode = calGoogleCode(qr_text)
                        logger.info('enter authentication code')
                        for i, c in enumerate(authcode):
                            code_inputs[i].send_keys(c)
                        logger.info('authentication code input finishes')
                except TimeoutException:
                    pass

            WebDriverWait(
                driver,
                20).until(lambda d: d.current_url == 'https://www.okx.com/')

            time.sleep(10)

            ok_ip_kyc_checkbox = driver.find_elements(By.CLASS_NAME,
                                                      'ok-ip-kyc-checkbox')

            if ok_ip_kyc_checkbox and ok_ip_kyc_checkbox[0].is_displayed():
                ok_ip_kyc_checkbox[0].click()
                driver.find_element(By.ID, 'okIpKycClose').click()

            break
    else:
        time.sleep(2)
        if driver.current_url == 'https://www.okx.com/':
            logger.info('already logged in')

    return driver, logger
