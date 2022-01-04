import proxy_loader
from helium import *
import chromedriver_autoinstaller
import pyotp
import time
import base64
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
logging.basicConfig(level=logging.INFO)

ACCEPTABLE_QUEUE_TIME = 60000
BESTBUY_2FA_TOKEN = "QW2LN7JNEHEVV65Y"
BESTBUY_USER = "pcrilley06@gmail.com"
BESTBUY_PASSWORD = "4w31d2EJGMCq"
sku = "6454318"


def getQueueTime(driver, sku) -> int:
    purchase_tracker = driver.execute_script(
        "return localStorage.getItem(\"purchaseTracker\");")

    a2c_transaction_code = json.loads(
        base64.b64decode(purchase_tracker))[sku][2]

    return _getQueueTime(a2c_transaction_code)


def _getQueueTime(a2ctransactioncode) -> int:
    content = a2ctransactioncode.split("-")
    saveContextMenuId = [int(x, 16) for x in content]

    v1 = int(content[2] + content[3], 16)
    v2 = saveContextMenuId[1]
    v3 = v1 / v2

    return int(1e3 * v3)


def reduceQueueTime(driver, sku):
    backup_cookies = driver.get_cookies()
    backup_purchaseTracker = driver.execute_script(
        "return localStorage.getItem('purchaseTracker')")
    old_queue_time = getQueueTime(driver, sku)
    clearSoftBan(driver)

    # keep retrying until it finds purchaseTracker. minimizing time in between rerolls
    while True:
        try:
            new_queue_time = getQueueTime(driver, sku)
            logging.info(
                f"BESTBUY - Successfully pulled purchaseTracker")
            break
        except:
            logging.info(
                f"BESTBUY - Failed to pull purchaseTracker. Retrying...")
            time.sleep(0.1)

            # new queue time sucks, restore old session
    if old_queue_time < new_queue_time:
        for cookie in backup_cookies:
            driver.add_cookie(cookie)
        driver.execute_script(
            "localStorage.setItem('purchaseTracker', arguments[0])", backup_purchaseTracker)

        logging.info(
            f"BESTBUY - Current queue time: {int(old_queue_time / 1000)} seconds. Found slower queue time at: {int(new_queue_time / 1000)}")
        return old_queue_time
    else:
        logging.info(
            f"BESTBUY - Current queue time: {int(new_queue_time / 1000)} seconds. Reduced time from {int(old_queue_time / 1000)} to {int(new_queue_time / 1000)}")
        return new_queue_time


def clearSoftBan(driver):
    logging.info("BESTBUY - Clearing soft bans for session")
    driver.delete_all_cookies()
    driver.execute_script('localStorage.clear();')

    add_to_cart = driver.find_element_by_css_selector(
        "button[data-button-state=\"ADD_TO_CART\"]")

    driver.execute_script("arguments[0].click();", add_to_cart)


bestbuy_2fa_code = pyotp.TOTP(BESTBUY_2FA_TOKEN)

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()


chrome_options = proxy_loader.get_chromedriver(use_proxy=True)
# chrome_options.add_extension(
#     '~/git_repos/bestbuy-queue-cracker.crx')
# chrome_options.add_extension(
#     'NerdSpeak_Stock_Helper_1.0.0.0.crx')

sku_page = f'https://www.bestbuy.com/site/{sku}.p?skuId={sku}'

logging.info("BESTBUY - Starting browser with extensions")
driver = start_chrome(sku_page, options=chrome_options)

logging.info("BESTBUY - Waiting for add to cart button")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'button[data-button-state="ADD_TO_CART"]'))).click()
time.sleep(1)
queue_time = 100000

while queue_time > ACCEPTABLE_QUEUE_TIME:
    queue_time = reduceQueueTime(driver, sku)


# at this point queue is really and fast, wait for it to almost be finished
time.sleep(int(queue_time / 1000))

add_to_cart = driver.find_element_by_css_selector(
    "button[data-button-state=\"ADD_TO_CART\"]")

driver.execute_script("arguments[0].click();", add_to_cart)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[data-track=\"Sign In\"]")))


write(BESTBUY_USER, into="Email")
write(BESTBUY_PASSWORD, into="Password")
click("Sign In")

WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.ID, "verificationCode")))

# write(bestbuy_2fa_code.now(), into="Security Code")
inputElement = driver.find_element_by_id("verificationCode")
inputElement.send_keys(bestbuy_2fa_code.now())
click("Continue")
