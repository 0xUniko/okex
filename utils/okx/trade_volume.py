from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from loguru._logger import Logger


def trade_volume(driver: Chrome, logger: Logger) -> Chrome:
    driver.get('https://www.okx.com/trade-convert/stablecoin/usdt')
    okx_tab = driver.current_window_handle
    # %%
    driver.find_element(By.CLASS_NAME, 'max').click()
    driver.find_element(By.CLASS_NAME, 'btn-content').click()
    # %%
    driver.get('https://www.okx.com/trade-convert/stablecoin/usdc')
    # %%
    # get recharge address
    driver.get('https://www.okx.com/balance/recharge')

    return driver