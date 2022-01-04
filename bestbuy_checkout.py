import proxy_loader
from helium import *
import chromedriver_autoinstaller
import pyotp
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
logging.basicConfig(level=logging.INFO)

ACCEPTABLE_QUEUE_TIME = 90000
BESTBUY_2FA_TOKEN = "QW2LN7JNEHEVV65Y"
sku = "6454318"


def getQueueTime(driver, sku) -> int:
    return int(driver.execute_script(f'''
        function getQueueTime(a2ctransactioncode) {{
            var content = ("-", a2ctransactioncode.split("-"));
            var saveContextMenuId = content.map(function (e) {{
                return parseInt(e, 16);
            }});
            return function (canCreateDiscussions) {{
                return 1e3 * canCreateDiscussions;
            }}(function (_num2, _num1) {{
                return _num2 / _num1;
            }}(parseInt(function (buckets, a2ctransactioncode) {{
                return buckets + a2ctransactioncode;
            }}(content[2], content[3]), 16), saveContextMenuId[1]));
        }}
        const purchaseTracker = JSON.parse(atob(window.localStorage.getItem("purchaseTracker")));
        const a2ctransactioncode = purchaseTracker[{sku}][2];
        return getQueueTime(a2ctransactioncode);
    '''))


bestbuy_2fa_code = pyotp.TOTP(BESTBUY_2FA_TOKEN)

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()


chrome_options = proxy_loader.get_chromedriver(use_proxy=True)
chrome_options.add_extension(
    '~/git_repos/bestbuy-queue-cracker.crx')
chrome_options.add_extension(
    'NerdSpeak_Stock_Helper_1.0.0.0.crx')

sku_page = f'https://www.bestbuy.com/site/{sku}.p?skuId={sku}'

logging.info("BESTBUY - Starting browser with extensions")
driver = start_chrome(sku_page, options=chrome_options)

logging.info("BESTBUY - Waiting for queue modal")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "#gated-purchase-please-wait-modal > div > div > div > button"))).click()
logging.info("BESTBUY - Queue modal closed")

# queue time in ms
queue_time = getQueueTime(driver, sku)
logging.info(
    "BESTBUY - Found queue time: {} seconds".format(int(queue_time / 1000)))

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "#bestBuyQueueCracker"))).click()
time.sleep(1)

logging.info("BESTBUY - Found some shit")

while queue_time > ACCEPTABLE_QUEUE_TIME:
    driver.find_element_by_css_selector(
        "#bestBuyQueueCracker").click()
    time.sleep(1)
    queue_time = getQueueTime(driver, sku)
