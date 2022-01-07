import requests
from bs4 import BeautifulSoup
from pprint import pprint
from enum import Enum
import re
import time
import sys
import logging
import threading

from requests.exceptions import ProxyError, Timeout

from gpu_scalping_toolkit.gpu_scanner import discord_bot, helpers, start_checkout

# time to wait after scanning to before sending another notification (minutes)
BESTBUY_RESCAN_TIMEOUT = 30
logging.basicConfig(level=logging.INFO)
bestbuy_scan_logger = logging.getLogger(__name__)


class PRODUCT_STATUS(Enum):
    OUT_OF_STOCK = 1
    RESTOCK_IMMINENT = 2
    AVAILABLE = 3


def scanProduct(sku, proxy_hash_list, product_status: PRODUCT_STATUS) -> PRODUCT_STATUS:
    product_url = "https://www.bestbuy.com/site/%s.p?skuId=%s&intl=nosplash" % (
        sku, sku)

    random_proxy = helpers.getRandomValidProxy(proxy_hash_list)

    bestbuy_scan_logger.info(
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
            bestbuy_scan_logger.warning(
                "Bestbuy: {} - 403 Proxy burned: {}:{}".format(sku, random_proxy["host"], random_proxy["port"]))
            random_proxy["valid"] = False
            return product_status

        html_string = response.content

        bestbuy_scan_logger.debug(html_string)
        product_status = _scanProduct(
            sku, html_string, f"{random_proxy['host']}:{random_proxy['port']}", product_status)
        # if we find this product, sleep for RESCAN_TIMEOUT mins before notifying again
        if product_status == PRODUCT_STATUS.AVAILABLE:
            bestbuy_scan_logger.info("Bestbuy: {} - Proxy: {}:{} | Sleeping for {} minutes".format(sku,
                                                                                                   random_proxy["host"], random_proxy["port"], BESTBUY_RESCAN_TIMEOUT))
            time.sleep(60 * BESTBUY_RESCAN_TIMEOUT)

        return product_status
    except (ProxyError, Timeout) as e:
        bestbuy_scan_logger.warning(
            "Bestbuy: {} - Proxy timed out: {}:{}".format(sku, random_proxy["host"], random_proxy["port"]))
        bestbuy_scan_logger.debug(e)
        random_proxy["valid"] = False
        return product_status
    except ConnectionError as e:
        bestbuy_scan_logger.warning(
            "Bestbuy: {} - Proxy: {}:{} | Connection error".format(sku, random_proxy["host"], random_proxy["port"]))
        bestbuy_scan_logger.debug(e)
        return product_status
    except Exception as e:
        bestbuy_scan_logger.warning(
            "Bestbuy: {} - Proxy: {}:{} | Unknown error".format(sku, random_proxy["host"], random_proxy["port"]))
        bestbuy_scan_logger.debug(e)
        return product_status


def _scanProduct(sku, html_string, proxy_url, product_status: PRODUCT_STATUS) -> PRODUCT_STATUS:
    soup = BeautifulSoup(html_string, 'html.parser')
    title = _scanProductForTitle(soup)

    if _scanForInternationalPrompt(sku, soup, proxy_url):
        return product_status

    if product_status.OUT_OF_STOCK:
        product_is_high_demand = _scanProductForHighDemand(
            sku, title, soup, proxy_url)

    product_is_available = _scanProductForAvailable(
        sku, title, soup, proxy_url)
    product_is_high_demand = False

    if not product_is_available and product_is_high_demand:
        return PRODUCT_STATUS.RESTOCK_IMMINENT
    elif not product_is_available:
        return PRODUCT_STATUS.OUT_OF_STOCK

    return PRODUCT_STATUS.AVAILABLE


def _scanProductForHighDemand(sku, title, soup, proxy_host):
    result_list = soup(text=re.compile(r'High Demand Product'))
    if len(result_list) > 0:
        bestbuy_scan_logger.info(
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
        bestbuy_scan_logger.info(
            "Bestbuy: {} - Proxy: {} | Sending alert to discord".format(sku, proxy_host))
        discord_bot.alertBestbuyDrop(
            sku, "The following product is now available:", title)
        # execute scanner
        # start_checkout.startCheckout(sku)
        thr = threading.Thread(
            target=start_checkout.startCheckout, args=(sku, ))
        thr.start()
    else:
        bestbuy_scan_logger.info(
            "Bestbuy: {} - Proxy: {} |  Product not available".format(sku, proxy_host))

    return is_in_stock


def _scanForInternationalPrompt(sku, soup, proxy_host):
    result_list = soup(text=re.compile(r'Choose a country'))
    if len(result_list) > 0:
        bestbuy_scan_logger.warning(
            "Bestbuy: {} - Proxy: {} | Choose a country prompt found".format(sku, proxy_host))
        return True

    return False


def _scanProductForTitle(soup):
    title_selector = "div.sku-title"
    return soup.select(title_selector)[0].text if len(
        soup.select(title_selector)) > 0 else "Title not found"


if __name__ == '__main__':
    sku = sys.argv[1]
    proxy_hash_list = helpers.getProxyHash()

    while True:
        scanProduct(sku, proxy_hash_list, PRODUCT_STATUS.OUT_OF_STOCK)
