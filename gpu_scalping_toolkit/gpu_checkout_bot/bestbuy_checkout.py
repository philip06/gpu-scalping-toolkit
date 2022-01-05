from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_queue_cracker, proxy_loader

from helium import *
import chromedriver_autoinstaller
import pyotp
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def addProductToCart(sku, account_info):
    bestbuy_2fa_code = pyotp.TOTP(account_info["2fa_token"])

    chrome_options = proxy_loader.get_chromedriver(use_proxy=True)

    sku_page = f'https://www.bestbuy.com/site/{sku}.p?skuId={sku}'

    logger.info(
        f"BESTBUY - Starting browser with proxy: {proxy_loader.PROXY_HOST}:{proxy_loader.PROXY_PORT}")
    driver = start_chrome(sku_page, options=chrome_options)

    logger.info("BESTBUY - Waiting for add to cart button")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[data-button-state="ADD_TO_CART"]'))).click()

    add_to_cart = driver.find_element_by_css_selector(
        "button[data-button-state=\"ADD_TO_CART\"]")

    driver.execute_script("arguments[0].click();", add_to_cart)
    time.sleep(1)
    queue_end_time = bestbuy_queue_cracker.getQueueTime(
        driver, sku).queue_end_time

    while queue_end_time > datetime.datetime.now():
        queue_end_time = bestbuy_queue_cracker.reduceQueueTime(
            driver, sku, queue_end_time)

    logger.info(f"BESTBUY - Queue finished")

    add_to_cart = driver.find_element_by_css_selector(
        "button[data-button-state=\"ADD_TO_CART\"]")

    driver.execute_script("arguments[0].click();", add_to_cart)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-track=\"Sign In\"]")))

    write(account_info["user"], into="Email")
    write(account_info["password"], into="Password")
    click("Sign In")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.ID, "verificationCode")))

    # write(bestbuy_2fa_code.now(), into="Security Code")
    inputElement = driver.find_element_by_id("verificationCode")
    inputElement.send_keys(bestbuy_2fa_code.now())
    click("Continue")


# BESTBUY_2FA_TOKEN = "4YQJH2QGRIDMXRPD"
# BESTBUY_USER = "pcrilley06@gmail.com"
# BESTBUY_PASSWORD = "4w31d2EJGMCq"
# sku = "6454318"

# account_info = {
#     "user": BESTBUY_USER,
#     "password": BESTBUY_PASSWORD,
#     "2fa_token": BESTBUY_2FA_TOKEN
# }

# addProductToCart(sku, account_info)
