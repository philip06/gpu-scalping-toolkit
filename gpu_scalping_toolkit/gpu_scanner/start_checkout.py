
from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_checkout


def startCheckout(sku):
    BESTBUY_2FA_TOKEN = "4YQJH2QGRIDMXRPD"
    BESTBUY_USER = "pcrilley06@gmail.com"
    BESTBUY_PASSWORD = "4w31d2EJGMCq"
    account_info = {
        "user": BESTBUY_USER,
        "password": BESTBUY_PASSWORD,
        "2fa_token": BESTBUY_2FA_TOKEN
    }
    bestbuy_checkout.addProductToCart(sku, account_info)
