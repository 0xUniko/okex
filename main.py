import httpx, datetime, time
from selenium import webdriver
from selenium.webdriver import chrome
import pandas as pd
from dotenv import dotenv_values
from loguru import logger

from utils.google.login_google import login_gmail, GooglePasswordError
from utils.google.change_recovery_email import change_recovery_email
from utils.google.change_google_password import change_google_password
from utils.okx.change_okx_password import change_okx_password
from utils.okx.login_okx import login_okx
from utils.okx.change_authencator import change_authencator
from utils.okx.create_api import create_api
from utils.okx.get_recharge_address import get_recharge_address
from utils.okx.set_withdrawal_whitelist import set_withdrawal_whitelist

ap = 'http://local.adspower.com:50325'

import os

os.remove('.log')

logger.add('.log')

# chech whether the ads server is ready
assert httpx.get(ap + '/status').status_code == 200
logger.success('Ads server is ready')

accounts = pd.read_csv('accounts.csv').reset_index(drop=True)

for i in accounts.index:
    logger.info(f"account begin {accounts.loc[i,'account']}")

    try:
        if not accounts.isna().loc[i, [
                'new_okx_password', 'new_google_password',
                'new_recovery_email', 'qr_text', 'api_name', 'api_key',
                'secret_key', 'recharge_address', 'withdrawal_address'
        ]].values.any():
            logger.info('account has been done')
        else:
            # get the config and set the selenium driver
            res_data = httpx.get(ap + '/api/v1/browser/start',
                                 params={
                                     'serial_number':
                                     accounts.loc[i, 'browser_no'],
                                     'open_tabs': 1,
                                     'clear_cache_after_closing': 1
                                 }).json()['data']
            service = chrome.service.Service(res_data['webdriver'])
            options = chrome.options.Options()
            options.debugger_address = res_data['ws']['selenium']
            driver = webdriver.Chrome(service=service, options=options)

            # get the account info
            account = accounts.loc[i, 'account']

            gmail_psw = accounts.loc[
                i, 'original_google_password'] if accounts.isna().loc[
                    i, 'new_google_password'] else accounts.loc[
                        i, 'new_google_password']

            preregistered_email = accounts.loc[
                i, 'google_preregistered_email'] if accounts.isna().loc[
                    i, 'new_recovery_email'] else accounts.loc[
                        i, 'new_recovery_email']

            okx_psw = accounts.loc[
                i, 'original_okx_password'] if accounts.isna().loc[
                    i,
                    'new_okx_password'] else accounts.loc[i,
                                                          'new_okx_password']

            qr_text = '' if accounts.isna().loc[
                i, 'qr_text'] else accounts.loc[i, 'qr_text']

            # login gmail
            driver, logger = login_gmail(driver, logger, account, gmail_psw,
                                         preregistered_email)

            time.sleep(2)

            # change google recovery email
            new_recovery_email = dotenv_values()['NEW_RECOVERY_EMAIL']
            if accounts.loc[i, 'new_recovery_email'] != new_recovery_email:
                driver, logger = change_recovery_email(driver, logger, account,
                                                       gmail_psw)

                accounts.loc[i, 'new_recovery_email'] = new_recovery_email
                accounts.to_csv('accounts.csv', index=False)
            else:
                logger.info('google recovery email have been changed')

            # change google password
            new_gmail_password = dotenv_values()['NEW_GMAIL_PASSWORD']
            if accounts.loc[i, 'new_google_password'] != new_gmail_password:
                driver, logger = change_google_password(
                    driver, logger, account, gmail_psw)
                accounts.loc[i, 'new_google_password'] = new_gmail_password
                accounts.to_csv('accounts.csv', index=False)
            else:
                logger.info('google password has been changed')

            # login okx
            driver, logger = login_okx(driver, logger, account, okx_psw,
                                       qr_text)
            time.sleep(2)

            # set okx authenticator
            if qr_text == '':
                driver, logger, qr_text = change_authencator(
                    driver, logger, account)
                accounts.loc[i, 'qr_text'] = qr_text
                accounts.to_csv('accounts.csv', index=False)

                time.sleep(2)
            else:
                logger.info('qr_text has been set')

            # remove okx devices
            # driver, logger = remove_devices(driver, logger, account, qr_text)

            # change okx password
            default_okx_password = dotenv_values()['DEFAULT_OKX_PASSWORD']
            if accounts.loc[i, 'new_okx_password'] != default_okx_password:
                driver, logger = change_okx_password(driver, logger, account,
                                                     okx_psw, qr_text)
                logger.info("password changed")
                accounts.loc[i, 'new_okx_password'] = default_okx_password
                accounts.to_csv('accounts.csv', index=False)

                time.sleep(3)

                driver, logger = login_okx(
                    driver, logger, account,
                    dotenv_values()['DEFAULT_OKX_PASSWORD'])
            else:
                logger.info('okx password has been changed')

            # create okx api
            if accounts.isna().loc[i, 'api_name']:
                driver, logger, item_values = create_api(
                    driver, logger, account, qr_text)
                accounts.loc[i, 'api_name'] = str(datetime.date.today())
                accounts.loc[i, 'api_key'] = item_values['api_key']
                accounts.loc[i, 'secret_key'] = item_values['secret_key']
                accounts.to_csv('accounts.csv', index=False)

                time.sleep(5)
            else:
                logger.info('api has been set')

            # get okx recharged address
            if accounts.isna().loc[i, 'recharge_address']:
                driver, logger, okb_recharge_addr = get_recharge_address(
                    driver, logger)
                accounts.loc[i, 'recharge_address'] = okb_recharge_addr
                accounts.to_csv('accounts.csv', index=False)
                time.sleep(2)
            else:
                logger.info('recharge address has been set')

            # set okx withdrawal whitelist address
            withdrawal_addr = dotenv_values()['WITHDRAWAL_ADDRESS']
            if accounts.loc[i, 'withdrawal_address'] != withdrawal_addr:
                driver, logger = set_withdrawal_whitelist(
                    driver, logger, account, qr_text)
                accounts.loc[i, 'withdrawal_address'] = withdrawal_addr
                accounts.to_csv('accounts.csv', index=False)

    except GooglePasswordError as e:
        accounts.loc[i, 'remark'] = e.msg
        accounts.to_csv('accounts.csv', index=False)
        logger.exception(e.msg)

    except Exception:
        logger.exception("error occurs")

    finally:
        httpx.get(ap + '/api/v1/browser/stop',
                  params={'serial_number': accounts.loc[i, 'browser_no']})
