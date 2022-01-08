(trap 'kill 0' INT; 
    python3 -m gpu_scalping_toolkit.gpu_checkout_bot.bestbuy_checkout SKU 2FA_TOKEN EMAIL GMAIL_PASSWORD BESTBUY_PASSWORD
    python3 -m gpu_scalping_toolkit.gpu_checkout_bot.bestbuy_checkout SKU2 2FA_TOKEN2 EMAIL2 GMAIL_PASSWORD2 BESTBUY_PASSWORD2
)