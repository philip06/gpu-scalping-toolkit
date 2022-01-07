import logging
import json
import base64
import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueDTO:
    def __init__(self, queue_length, queue_start_time, queue_end_time):
        self.queue_length = queue_length
        self.queue_start_time = queue_start_time
        self.queue_end_time = queue_end_time

    def __str__(self):
        return f'''
            {{
                "queue_length": {self.queue_length},
                "queue_start_time": {self.queue_start_time},
                "queue_end_time": {self.queue_end_time}
            }}
        '''


def getQueueTime(driver, sku) -> QueueDTO:
    purchase_tracker = driver.execute_script(
        "return localStorage.getItem(\"purchaseTracker\");")

    a2c_transaction_code = json.loads(
        base64.b64decode(purchase_tracker))[sku][2]

    queue_length = _getQueueTime(a2c_transaction_code)
    queue_start_time = datetime.datetime.now()
    queue_end_time = queue_start_time + \
        datetime.timedelta(seconds=queue_length)

    # logger.info(
    #     f"BESTBUY - Found queue time: {queue_end_time} - {getRemainingTime(queue_end_time)}")
    return QueueDTO(queue_length, queue_start_time, queue_end_time)


def _getQueueTime(a2ctransactioncode) -> int:
    content = a2ctransactioncode.split("-")
    saveContextMenuId = [int(x, 16) for x in content]

    v1 = int(content[2] + content[3], 16)
    v2 = saveContextMenuId[1]
    v3 = v1 / v2

    return int(1e3 * v3 / 1000)


def getRemainingTime(queue_end_time) -> datetime:
    return queue_end_time - datetime.datetime.now()


def saveQueueTime(driver):
    backup_cookies = driver.get_cookies()
    backup_purchaseTracker = driver.execute_script(
        "return localStorage.getItem('purchaseTracker')")
    return backup_cookies, backup_purchaseTracker


def restoreQueueTime(driver, backup_cookies, backup_purchaseTracker):
    for cookie in backup_cookies:
        driver.add_cookie(cookie)
        driver.execute_script(
            "localStorage.setItem('purchaseTracker', arguments[0])", backup_purchaseTracker)

# returns queue completion datetime


def reduceQueueTime(driver, sku, old_queue_end_time) -> datetime:
    backup_cookies, backup_purchaseTracker = saveQueueTime(driver)
    clearSoftBan(driver)
    new_queue_end_time = old_queue_end_time

    # keep retrying until it finds purchaseTracker. minimizing time in between rerolls
    while True:
        try:
            new_queue_dto = getQueueTime(driver, sku)
            new_queue_end_time = new_queue_dto.queue_end_time
            logger.info(
                f"BESTBUY - Successfully pulled purchaseTracker")
            break
        except:
            # logger.info(
            #     f"BESTBUY - Failed to pull purchaseTracker. Retrying...")
            time.sleep(0.1)

    if old_queue_end_time < new_queue_end_time:
        # new queue time sucks, restore old session
        restoreQueueTime(driver, backup_cookies, backup_purchaseTracker)
        logger.info(
            f"BESTBUY - Current queue time: {getRemainingTime(old_queue_end_time)} seconds. Found slower queue time at: {getRemainingTime(new_queue_end_time)}")
        return old_queue_end_time
    else:
        logger.info(
            f"BESTBUY - Current queue time: {getRemainingTime(new_queue_end_time)} seconds. Reduced time from {getRemainingTime(old_queue_end_time)} to {getRemainingTime(new_queue_end_time)}")
        return new_queue_end_time


def clearSoftBan(driver):
    logger.info("BESTBUY - Clearing soft bans for session")
    driver.delete_all_cookies()
    driver.execute_script('localStorage.clear();')

    add_to_cart = driver.find_element_by_css_selector(
        "button[data-button-state=\"ADD_TO_CART\"]")

    driver.execute_script("arguments[0].click();", add_to_cart)
