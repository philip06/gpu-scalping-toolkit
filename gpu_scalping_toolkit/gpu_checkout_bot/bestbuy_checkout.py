from multiprocessing.queues import Queue
from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_queue_cracker, proxy_loader, read_gmail

from helium import *
import chromedriver_autoinstaller
import pyotp
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

from gpu_scalping_toolkit.gpu_checkout_bot.account import AccountDTO

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def addProductToCart(queue: Queue, sku, account_info: AccountDTO, thread_id):
    bestbuy_2fa_code = pyotp.TOTP(account_info["2fa_token"])

    chrome_options = proxy_loader.get_chromedriver(
        use_proxy=True, account_info=account_info)

    sku_page = f'https://www.bestbuy.com/site/{sku}.p?skuId={sku}'

    logger.info(
        f"BESTBUY{thread_id} - Starting browser with proxy: {account_info['proxy_host']}:{account_info['proxy_port']}")
    driver = start_chrome(sku_page, options=chrome_options)

    logger.info(f"BESTBUY{thread_id} - Waiting for add to cart button")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[data-button-state="ADD_TO_CART"]'))).click()

    add_to_cart = driver.find_element_by_css_selector(
        "button[data-button-state=\"ADD_TO_CART\"]")

    driver.execute_script("arguments[0].click();", add_to_cart)
    time.sleep(1)
    queue_end_time = bestbuy_queue_cracker.getQueueTime(
        driver, sku).queue_end_time

    logger.info(
        f"BESTBUY{thread_id} - Initial queue time: {bestbuy_queue_cracker.getRemainingTime(queue_end_time)}")

    queue_piggyback = False
    while queue_end_time > datetime.datetime.now():
        # check if other task already completed queue
        if queue.qsize() > 0:
            backup_queue = queue.get_nowait()
            bestbuy_queue_cracker.restoreQueueTime(driver, backup_queue)
            queue.put(backup_queue)
            queue_piggyback = True
            logger.info(
                f"BESTBUY{thread_id} - Piggybacking on queue from another browser")
            break
        else:
            logger.info(f"BESTBUY{thread_id} - Nothing to piggyback on")
            queue_end_time = bestbuy_queue_cracker.reduceQueueTime(
                driver, sku, queue_end_time, thread_id)

    logger.info(f"BESTBUY{thread_id} - Queue finished")

    # if this browser isn't already piggybacking on another queue, alert other browsers to start piggybacking
    if not queue_piggyback:
        # save queues data in the order it finishes
        logger.info(
            f"BESTBUY{thread_id} - Most optimal queue found, notifying other browsers")
        queue.put(bestbuy_queue_cracker.saveQueueTime(driver))

    add_to_cart = driver.find_element_by_css_selector(
        'button[data-button-state="ADD_TO_CART"]')

    driver.execute_script("arguments[0].click();", add_to_cart)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-track=\"Sign In\"]")))

    write(account_info["email"], into="Email")
    write(account_info["password"], into="Password")
    click("Sign In")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.ID, "verificationCode")))

    # write(bestbuy_2fa_code.now(), into="Security Code")
    inputElement = driver.find_element_by_id("verificationCode")
    inputElement.send_keys(bestbuy_2fa_code.now())
    click("Continue")

    verification_code = read_gmail.get_bestbuy_verification_code(
        account_info["email"], account_info["gmail_password"], 10)
    logger.info(
        f"BESTBUY{thread_id} - Got email verification code: {verification_code}")

    # only need to do this if the email authentication comes up
    if verification_code:
        write(verification_code, into="Verification Code")
        click("Continue")


if __name__ == '__main__':
    import sys
    sku = sys.argv[1]

    BESTBUY_2FA_TOKEN = "4YQJH2QGRIDMXRPD"
    BESTBUY_EMAIL = "bbverify88@gmail.com"
    GMAIL_PASSWORD = "w9P4mfz7UY6N2S"
    BESTBUY_PASSWORD = "w9P4mfz7UY6N2S"

    account_info = {
        "email": BESTBUY_EMAIL,
        "password": BESTBUY_PASSWORD,
        "gmail_password": GMAIL_PASSWORD,
        "2fa_token": BESTBUY_2FA_TOKEN
    }

    PROXY_USER = "coiaacye"
    PROXY_PASS = "kkul1ixr4jnp"
    PROXY_HOST = "23.230.25.103"
    PROXY_PORT = 20000

    proxy_info = {
        "user": PROXY_USER,
        "password": PROXY_PASS,
        "host": PROXY_HOST,
        "port": PROXY_PORT
    }

    addProductToCart(sku, account_info, proxy_info)
