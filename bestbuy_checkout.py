import proxy_loader
import bestbuy_queue_cracker

from helium import *
import chromedriver_autoinstaller
import pyotp
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()
logging.basicConfig(level=logging.INFO)

ACCEPTABLE_QUEUE_TIME = 60000
BESTBUY_2FA_TOKEN = "QW2LN7JNEHEVV65Y"
BESTBUY_USER = "pcrilley06@gmail.com"
BESTBUY_PASSWORD = "4w31d2EJGMCq"
sku = "6454318"

bestbuy_2fa_code = pyotp.TOTP(BESTBUY_2FA_TOKEN)


chrome_options = proxy_loader.get_chromedriver(use_proxy=True)

sku_page = f'https://www.bestbuy.com/site/{sku}.p?skuId={sku}'

logging.info(
    f"BESTBUY - Starting browser with proxy: {proxy_loader.PROXY_HOST}:{proxy_loader.PROXY_PORT}")
driver = start_chrome(sku_page, options=chrome_options)

logging.info("BESTBUY - Waiting for add to cart button")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'button[data-button-state="ADD_TO_CART"]'))).click()
time.sleep(1)
queue_time = 100000

while queue_time > ACCEPTABLE_QUEUE_TIME:
    queue_time = bestbuy_queue_cracker.reduceQueueTime(driver, sku)


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
