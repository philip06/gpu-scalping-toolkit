

from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_checkout
from multiprocessing import Process, Queue, Manager
from multiprocessing.pool import ThreadPool, Pool

from gpu_scalping_toolkit.gpu_checkout_bot.account import ACCOUNT_REGION, AccountDTO


def startCheckout(sku):
    accounts: list = [{
        "email": "",
        "password": "",
        "gmail_password": "",
        "2fa_token": "",
        "region": ACCOUNT_REGION.DMV,
        "proxy_user": "",
        "proxy_password": "",
        "proxy_host": "",
        "proxy_port": 0
    }]

    pool = Pool()
    m = Manager()
    q = m.Queue()

    for thread_id, account in enumerate(accounts):
        pool.apply_async(bestbuy_checkout.addProductToCart,
                         args=(q, sku, account, thread_id,))

    pool.close()
    pool.join()

    # bestbuy_checkout.addProductToCart(q, sku, accounts[0], 0)


if __name__ == '__main__':
    import sys
    sku = sys.argv[1]

    startCheckout(sku)
