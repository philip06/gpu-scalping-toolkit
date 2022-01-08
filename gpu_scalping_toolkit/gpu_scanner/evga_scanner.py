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
evga_scan_logger = logging.getLogger(__name__)

ranked_product_numbers = [
    [""]
    # ["10G-P5-3897-RX", "08G-P5-3667-RX", "10G-P5-3885-RX"],
    # ["08G-P5-3665-RX", "08G-P5-3663-RX", "10G-P5-3895-RX",
    #     "10G-P5-3883-RX", "10G-P5-3881-RX"],
    # ["08G-P5-3767-RX", "08G-P5-3755-RX", "08G-P5-3753-RX", "08G-P5-3751-RX",
    #     "10G-P5-3898-RX", "10G-P5-3888-RX", "10G-P5-3899-RX", "10G-P5-3889-RX"],
    # ["24G-P5-3987-RX", "24G-P5-3985-RX", "24G-P5-3975-RX", "24G-P5-3973-RX", "24G-P5-3971-RX", "24G-P5-3988-RX",
    #     "24G-P5-3989-RX", "24G-P5-3978-RX", "24G-P5-3998-RX", "24G-P5-3999-RX", "24G-P5-3979-RX"],
    # ["10G-P5-3897-RL", "10G-P5-3885-RL", "10G-P5-3895-RL", "10G-P5-3883-RL", "10G-P5-3881-RL", "10G-P5-3898-RL", "10G-P5-3888-RL", "10G-P5-3899-RL",
    #     "10G-P5-3889-RL", "08G-P5-3767-RL", "08G-P5-3755-RL", "08G-P5-3751-RL", "08G-P5-3753-RL", "12G-P5-3657-RX", "12G-P5-3655-RX"],
    # ["08G-P5-3667-RL", "08G-P5-3663-RL", "08G-P5-3665-RL", "08G-P5-3797-RX", "08G-P5-3785-RX", "08G-P5-3783-RX",
    #     "12G-P5-3967-RX", "12G-P5-3953-RX", "12G-P5-3968-RX", "12G-P5-3958-RX", "12G-P5-3969-RX", "12G-P5-3959-RX"],
    # ["06G-P4-1061-RX", "06G-P4-1066-RX", "06G-P4-1068-RX"]
]


def findBestProduct(product_number_list):
    for tier in ranked_product_numbers:
        for product_number in product_number_list:
            if product_number in tier:
                return product_number


def findValuableProducts(product_number_list):
    valuable_products = []
    for tier in ranked_product_numbers:
        for product_number in product_number_list:
            if product_number in tier:
                valuable_products.append(product_number)
    return valuable_products


def scanProduct(sku, proxy_hash_list):
    product_url = "https://www.evga.com/products/productlist.aspx?type=8"
    random_proxy = helpers.getRandomValidProxy(proxy_hash_list)
    proxy_url = "{}:{}".format(random_proxy["host"], random_proxy["port"])

    evga_scan_logger.info(
        f"EVGA: {sku} - Proxy: {random_proxy['host']}:{random_proxy['port']} | Scanning for product")

    headers = {
        "User-Agent": helpers.getUserAgent(),
        "cache-control": "max-age=0"
    }
    try:
        response = requests.get(product_url, proxies={
            "https": f'http://{random_proxy["user"]}:{random_proxy["password"]}@{random_proxy["host"]}:{random_proxy["port"]}/'
        },
            headers=headers, verify=False)

        html_string = response.content

        if response.status_code == 403:
            evga_scan_logger.warning(
                "EVGA: {} - 403 Proxy burned: {}".format(sku, proxy_url))
            return False

        if sku == "high_demand_local":
            with open('evga_b_stock.html', 'r') as f:
                html_string = f.read()

        return _scanProduct(sku, html_string, proxy_url)
    except (ProxyError, Timeout) as e:
        evga_scan_logger.warning(
            "EVGA: {} - Proxy timed out: {}".format(sku, proxy_url))
        evga_scan_logger.debug(e)
        random_proxy["valid"] = False
        return False


def _scanProduct(sku, html_string, proxy_url):
    soup = BeautifulSoup(html_string, 'html.parser',
                         from_encoding="iso-8859-1")

    product_numbers = []

    for product in soup.select('.pl-list-pn'):
        product_number = product.text.replace("P/N: ", "")
        product_numbers.append(product_number)
        # if product_number == sku:
        #     evga_scan_logger.info(
        #         "EVGA: {} - Proxy: {} | Sending alert to discord".format(sku, proxy_url))
        #     discord_bot.alertEVGADrop(
        #         sku, "The following product is now available:", sku)

        #     # if we find this product, sleep for 30 mins before notifying again
        #     evga_scan_logger.info(
        #         "EVGA: {} - Proxy: {} | Sleeping for {} minutes".format(sku, proxy_url, RESCAN_TIMEOUT))
        #     time.sleep(60 * RESCAN_TIMEOUT)
        #     return True

    valuable_products = findValuableProducts(product_numbers)
    best_product_number = findBestProduct(valuable_products)
    evga_scan_logger.info(
        "EVGA: {} - Proxy: {} | Found product: {}".format(sku, proxy_url, best_product_number))
    return False


if __name__ == '__main__':
    proxy_hash_list = helpers.getProxyHash()
    while True:
        scanProduct(proxy_hash_list)
        break
