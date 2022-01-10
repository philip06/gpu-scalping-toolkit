

from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_checkout
from multiprocessing import Process, Queue, Manager
from multiprocessing.pool import ThreadPool, Pool

from gpu_scalping_toolkit.gpu_checkout_bot.account import ACCOUNT_REGION, AccountDTO


def startCheckout(sku):
    accounts: list = [{
        "email": "bbverify88@gmail.com",
        "password": "w9P4mfz7UY6N2S",
        "gmail_password": "w9P4mfz7UY6N2S",
        "2fa_token": "4YQJH2QGRIDMXRPD",
        "region": ACCOUNT_REGION.DMV,
        "proxy_user": "coiaacye",
        "proxy_password": "kkul1ixr4jnp",
        "proxy_host": "23.230.25.103",
        "proxy_port": 20000
    },
        {
        "email": "hkapperbb@gmail.com",
        "password": "EyujcSv8FbuP6ASs",
        "gmail_password": "EyujcSv8FbuP6ASs",
        "2fa_token": "MI64KYY5QLQH62X3",
        "region": ACCOUNT_REGION.DMV,
        "proxy_user": "coiaacye",
        "proxy_password": "kkul1ixr4jnp",
        "proxy_host": "23.230.25.104",
        "proxy_port": 20000
    },
        {
        "email": "kapsakcjvv@gmail.com",
        "password": "6y8B7^y!C4$7",
        "gmail_password": "U7d7#xCVL4Qe0!pu",
        "2fa_token": "O5FK557TKTLZCSOJ",
        "region": ACCOUNT_REGION.ATL,
        "proxy_user": "coiaacye",
        "proxy_password": "kkul1ixr4jnp",
        "proxy_host": "23.230.25.105",
        "proxy_port": 20000
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
