
from gpu_scalping_toolkit.gpu_checkout_bot import bestbuy_checkout


def startCheckout(sku):
    BESTBUY_2FA_TOKEN = "4YQJH2QGRIDMXRPD"
    BESTBUY_EMAIL = "bbverify88@gmail.com"
    GMAIL_PASSWORD = "w9P4mfz7UY6N2S"
    BESTBUY_PASSWORD = "w9P4mfz7UY6N2S"
    account_info = {
        "email": BESTBUY_EMAIL,
        "password": BESTBUY_PASSWORD,
        "gmail_password": GMAIL_PASSWORD,
        "2fa_token": BESTBUY_2FA_TOKEN
    }
    bestbuy_checkout.addProductToCart(sku, account_info)
