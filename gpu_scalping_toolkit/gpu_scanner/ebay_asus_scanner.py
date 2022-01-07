from gpu_scalping_toolkit.gpu_scanner import discord_bot, helpers
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, Timeout
import logging
import requests
import re
import time

EBAY_RESCAN_TIMEOUT = 30
ebay_scan_logger = logging.getLogger(__name__)


def scanProduct(proxy_hash_list):
    product_url = "https://www.ebay.com/sch/asus/m.html?item=403313960596&rt=nc&_trksid=p2047675.m3561.l2562"

    random_proxy = helpers.getRandomValidProxy(proxy_hash_list)

    ebay_scan_logger.info(
        "Ebay: Proxy: {}:{} | Scanning for products".format(random_proxy["host"], random_proxy["port"]))

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
            random_proxy["valid"] = False
            return False

        html_string = response.content

        product_available = _scanProduct(
            html_string=html_string, proxy_host=f"{random_proxy['host']}:{random_proxy['port']}")

        if product_available:
            ebay_scan_logger.info(
                f"Ebay: Proxy: {random_proxy['host']}:{random_proxy['port']} | Sleeping for {EBAY_RESCAN_TIMEOUT} minutes")

            time.sleep(60 * EBAY_RESCAN_TIMEOUT)

        return product_available
    except (ProxyError, Timeout) as e:
        ebay_scan_logger.warning(
            "Ebay: Proxy timed out | {}:{}".format(random_proxy["host"], random_proxy["port"]))
        ebay_scan_logger.debug(e)
        random_proxy["valid"] = False
        return False
    except ConnectionError as e:
        ebay_scan_logger.warning(
            "Ebay: Proxy connection error | {}:{}".format(random_proxy["host"], random_proxy["port"]))
        ebay_scan_logger.debug(e)
        return False
    except Exception as e:
        ebay_scan_logger.warning(
            "Ebay: Proxy unknown error: {}:{}".format(random_proxy["host"], random_proxy["port"]))
        ebay_scan_logger.debug(e)
        return False


def _scanProduct(html_string, proxy_host):
    soup = BeautifulSoup(html_string, 'html.parser')
    product_found = False

    for product in soup.select(".lvtitle"):
        if re.match(r"^.*?30\d\d.*?$", product.text):
            ebay_scan_logger.info(
                f"Ebay: Proxy: {proxy_host} | Found 30 series GPU")
            discord_bot.alertEbayDrop(
                "The following ASUS refurbished product is now available", product.text)
            product_found = True

    return product_found


if __name__ == '__main__':
    proxy_hash_list = helpers.getProxyHash()

    while True:
        scanProduct(proxy_hash_list)
