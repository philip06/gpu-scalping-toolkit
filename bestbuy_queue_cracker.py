import logging
import json
import base64
import time


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

    if old_queue_time < new_queue_time:
        # new queue time sucks, restore old session
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
