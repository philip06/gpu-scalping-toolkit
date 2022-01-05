import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import time
import sys
import logging

from requests.exceptions import ProxyError, Timeout

from gpu_scalping_toolkit.gpu_scanner import discord_bot, helpers, start_checkout

# time to wait after scanning to before sending another notification (minutes)
RESCAN_TIMEOUT = 30
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scanProduct(sku, proxy_hash_list):
    product_url = "https://www.bestbuy.com/site/%s.p?skuId=%s&intl=nosplash" % (
        sku, sku)

    random_proxy = helpers.getRandomValidProxy(proxy_hash_list)

    logger.info(
        "Bestbuy: {} - Proxy: {}:{} | Scanning for product".format(sku, random_proxy["host"], random_proxy["port"]))

    headers = {
        "User-Agent": helpers.getUserAgent(),
        "cache-control": "max-age=0"
    }
    try:
        response = requests.get(product_url, headers=headers,
                                proxies={
                                    "https": "http://{}:{}@{}:{}/".format(random_proxy["user"], random_proxy["password"], random_proxy["host"], random_proxy["port"])
                                },
                                timeout=5)

        if response.status_code == 403:
            logger.warning(
                "Bestbuy: {} - 403 Proxy burned: {}:{}".format(sku, random_proxy["host"], random_proxy["port"]))
            random_proxy["valid"] = False
            return False

        html_string = response.content

        if sku == "high_demand_local":
            with open('high_demand_product.html', 'r') as f:
                html_string = f.read()

        logger.debug(html_string)
        product_available = _scanProduct(
            sku, html_string, "{}:{}".format(random_proxy["host"], random_proxy["port"]))
        # if we find this product, sleep for RESCAN_TIMEOUT mins before notifying again
        if product_available:
            logger.info("Bestbuy: {} - Proxy: {}:{} | Sleeping for {} minutes".format(sku,
                                                                                      random_proxy["host"], random_proxy["port"], RESCAN_TIMEOUT))
            time.sleep(60 * RESCAN_TIMEOUT)

        return product_available
    except (ProxyError, Timeout) as e:
        logger.warning(
            "Bestbuy: {} - Proxy timed out: {}:{}".format(sku, random_proxy["host"], random_proxy["port"]))
        logger.debug(e)
        random_proxy["valid"] = False
        return False


def _scanProduct(sku, html_string, proxy_url):
    soup = BeautifulSoup(html_string, 'html.parser')
    title = _scanProductForTitle(soup)

    if _scanForInternationalPrompt(sku, soup, proxy_url):
        return False

    # this type of "or" means that it will only execute _scanProductForHighDemand() if:
    #   _scanProductForAvailable() return False
    return _scanProductForAvailable(sku, title, soup, proxy_url) or _scanProductForHighDemand(sku, title, soup, proxy_url)


def _scanProductForHighDemand(sku, title, soup, proxy_host):
    result_list = soup(text=re.compile(r'High Demand Product'))
    if len(result_list) > 0:
        logger.info(
            "Bestbuy: {} - Proxy: {} | Restock imminent".format(sku, proxy_host))
        title = _scanProductForTitle(soup)
        discord_bot.alertBestbuyDrop(
            sku, "The following product is about to restock:", title)
        return True

    return False


def _scanProductForAvailable(sku, title, soup, proxy_host):
    add_to_cart_selector = 'button[data-button-state="ADD_TO_CART"]'
    is_in_stock = True if len(
        soup.select(add_to_cart_selector)) > 0 else False

    if is_in_stock:
        logger.info(
            "Bestbuy: {} - Proxy: {} | Sending alert to discord".format(sku, proxy_host))
        discord_bot.alertBestbuyDrop(
            sku, "The following product is now available:", title)
        # execute scanner
        start_checkout.startCheckout(sku)
    else:
        logger.info(
            "Bestbuy: {} - Proxy: {} |  Product not available".format(sku, proxy_host))

    return is_in_stock


def _scanForInternationalPrompt(sku, soup, proxy_host):
    result_list = soup(text=re.compile(r'Choose a country'))
    if len(result_list) > 0:
        logger.warning(
            "Bestbuy: {} - Proxy: {} | Choose a country prompt found".format(sku, proxy_host))
        return True

    return False


def _scanProductForTitle(soup):
    title_selector = "div.sku-title"
    return soup.select(title_selector)[0].text if len(
        soup.select(title_selector)) > 0 else "Title not found"


available_test_sku = "6462204"
high_demand_test_sku = "6454318"
# in case pny goes out of stock again, we have local html copy
high_demand_local = "high_demand_local"
oos_test_sku = "6429440"

if __name__ == '__main__':
    sku = sys.argv[1]
    proxy_hash_list = helpers.getProxyHash()

    while True:
        scanProduct(sku, proxy_hash_list)
        time.sleep(5)
