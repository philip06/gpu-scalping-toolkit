import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time
import sys
import logging

from requests.exceptions import ProxyError, Timeout

import discord_bot
import helpers

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RESCAN_TIMEOUT = 10
logging.basicConfig(level=logging.INFO)


def scanProduct(sku, proxy_hash_list):
    product_url = "https://www.evga.com/products/productlist.aspx?type=8"
    random_proxy = helpers.getRandomValidProxy(proxy_hash_list)
    proxy_url = "{}:{}".format(random_proxy["host"], random_proxy["port"])

    logging.info("EVGA: {} - Proxy: {}:{} | Scanning for product".format(sku,
                 random_proxy["host"], random_proxy["port"]))

    headers = {
        "User-Agent": helpers.getUserAgent(),
        "cache-control": "max-age=0"
    }
    try:
        response = requests.get(product_url, proxies={
            "https": "http://{}:{}@{}:{}/".format(random_proxy["user"], random_proxy["password"], random_proxy["host"], random_proxy["port"])
        },
            headers=headers, verify=False)

        html_string = response.content

        if response.status_code == 403:
            logging.warning(
                "EVGA: {} - 403 Proxy burned: {}".format(sku, proxy_url))
            return False

        if sku == "high_demand_local":
            with open('evga_b_stock.html', 'r') as f:
                html_string = f.read()

        return _scanProduct(sku, html_string, proxy_url)
    except (ProxyError, Timeout) as e:
        logging.warning(
            "EVGA: {} - Proxy timed out: {}".format(sku, proxy_url))
        logging.debug(e)
        random_proxy["valid"] = False
        return False


def _scanProduct(sku, html_string, proxy_url):
    soup = BeautifulSoup(html_string, 'html.parser',
                         from_encoding="iso-8859-1")

    for product in soup.select('.pl-list-pn'):
        product_number = product.text.replace("P/N: ", "")
        if product_number == sku:
            logging.info(
                "EVGA: {} - Proxy: {} | Sending alert to discord".format(sku, proxy_url))
            discord_bot.alertEVGADrop(
                sku, "The following product is now available:", sku)

            # if we find this product, sleep for 30 mins before notifying again
            logging.info(
                "EVGA: {} - Proxy: {} | Sleeping for {} minutes".format(sku, proxy_url, RESCAN_TIMEOUT))
            time.sleep(60 * RESCAN_TIMEOUT)
            return True

    logging.info(
        "EVGA: {} - Proxy: {} | Product not found".format(sku, proxy_url))
    return False


test_sku = "01G-P3-1313-RX"

if __name__ == '__main__':
    sku = sys.argv[1]
    proxy_hash_list = helpers.getProxyHash()
    while True:
        scanProduct(sku, proxy_hash_list)
        # break
