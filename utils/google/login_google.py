import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru._logger import Logger


class GooglePasswordError(Exception):

    def __init__(self, msg):
        self.msg = msg


def use_another_account_to_login(driver: Chrome, logger: Logger):
    logger.info('use another account to login')

    gmail_login_div = driver.find_elements(
        By.XPATH, "//div[contains(@aria-label,'@gmail.com')]")

    if gmail_login_div:
        gmail_login_div[0].click()

        WebDriverWait(
            driver,
            10).until(lambda d: len(d.find_elements(By.TAG_NAME, 'ul')) == 2)

        driver.find_element(By.TAG_NAME,
                            'ul').find_elements(By.TAG_NAME, 'li')[-1].click()
    else:
        WebDriverWait(
            driver,
            10).until(lambda d: len(d.find_elements(By.TAG_NAME, 'ul')) == 2)

        driver.find_element(By.TAG_NAME,
                            'ul').find_elements(By.TAG_NAME, 'li')[-2].click()

    return driver, logger


def login_with_username_psw(driver: Chrome, logger: Logger, account: str,
                            gmail_psw: str):
    logger.info('login in with username and password')

    if not driver.find_elements(By.ID, 'identifierId'):
        if not driver.find_elements(By.NAME, 'password'):
            driver, logger = use_another_account_to_login(driver, logger)
        else:
            driver.find_element(By.NAME, 'password').send_keys(gmail_psw)
            driver.find_element(By.ID, 'passwordNext').click()

    account_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'identifierId')))

    time.sleep(2)

    if account_input.is_displayed():
        logger.info('enter the account')
        account_input.send_keys(account)
        driver.find_element(By.ID, 'identifierNext').click()

    psw_or_captcha = WebDriverWait(driver, 10).until(
        EC.any_of(EC.visibility_of_element_located((By.ID, 'captchaimg')),
                  EC.visibility_of_element_located((By.NAME, 'password'))))

    if psw_or_captcha.get_attribute('id') == 'captchaimg':
        logger.info('waiting for inputing captcha')
        psw_input = WebDriverWait(driver, 3600).until(
            EC.visibility_of_element_located((By.NAME, 'password')))
    else:
        psw_input = psw_or_captcha

    # time.sleep(2)
    logger.info('enter the password')

    psw_input.send_keys(gmail_psw)

    driver.find_element(By.ID, 'passwordNext').click()

    time.sleep(3)

    try:
        WebDriverWait(driver, 5).until(lambda d: len([
            e for e in d.find_elements(By.CSS_SELECTOR,
                                       'div[aria-live="assertive"]')
            if e.is_displayed()
        ]) > 1)

        raise GooglePasswordError('google password error')

    except TimeoutException:
        pass

    return driver, logger


def login_gmail(driver: Chrome, logger: Logger, account: str, gmail_psw: str,
                preregistered_email: str):
    logger.info("login gmail")

    logger.info('login gmail, go to https://gmail.google.com')
    driver.get('https://gmail.google.com')
    # gmail_tab = driver.current_window_handle
    if not (driver.current_url == 'https://mail.google.com/mail/u/0/#inbox'
            or driver.current_url == 'https://mail.google.com/mail/u/0/'):
        logger.info(
            f'cached login in status fail, current url is: { driver.current_url}'
        )

        # if driver.current_url == 'https://www.google.com/intl/zh-CN/gmail/about/':
        if driver.current_url[:27] == 'https://www.google.com/intl':
            driver.get('https://accounts.google.com/signin/v2')

        try:
            driver, logger = login_with_username_psw(driver, logger, account,
                                                     gmail_psw)
        except TimeoutException:
            btns = driver.find_elements(By.TAG_NAME, 'button')
            if len(btns) == 1:
                logger.info('have to confirm login')

                btns[0].click()
                time.sleep(2)

                try:
                    driver, logger = login_with_username_psw(
                        driver, logger, account, gmail_psw)
                except TimeoutException:
                    time.sleep(20)

        time.sleep(10)
    else:
        logger.info('already logined in')

    if not (driver.current_url == 'https://mail.google.com/mail/u/0/#inbox'
            or driver.current_url == 'https://mail.google.com/mail/u/0/'):
        logger.info(
            f'verify the preregistered email address, current url is: {driver.current_url}'
        )
        logger.info('select preregistered email')
        select_preregistered_email = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                'path[d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z"]'
            )))
        time.sleep(1)
        select_preregistered_email[1].click()

        logger.info('enter preregistered email')
        preregistered_email_input = WebDriverWait(driver, 3600).until(
            EC.visibility_of_element_located(
                (By.ID, 'knowledge-preregistered-email-response')))
        time.sleep(1)
        preregistered_email_input.send_keys(preregistered_email)
        driver.find_element(By.TAG_NAME, 'button').click()

    return driver, logger
