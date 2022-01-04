from helium import *
import chromedriver_autoinstaller
import pyotp

import proxy_loader

BESTBUY_2FA_TOKEN = "QW2LN7JNEHEVV65Y"
bestbuy_2fa_code = pyotp.TOTP(BESTBUY_2FA_TOKEN)

# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path
chromedriver_autoinstaller.install()


chrome_options = proxy_loader.get_chromedriver(use_proxy=True)
chrome_options.add_extension(
    '~/git_repos/bestbuy-queue-cracker.crx')
chrome_options.add_extension(
    'NerdSpeak_Stock_Helper_1.0.0.0.crx')

# chrome_options.add_argument(
#     "--proxy-server={}".format(PROXY))

"button.c-close-icon.c-modal-close-icon"

sku_page = "https://www.bestbuy.com/site/pny-nvidia-geforce-rtx-3060-12gb-xlr8-gaming-revel-epic-x-rgb-single-fan-graphics-card/6454318.p?skuId=6454318"

driver = start_chrome(sku_page, options=chrome_options)
