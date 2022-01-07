from discord import Webhook, RequestsWebhookAdapter, Embed

my_id = '<@119889394470617088>'


def alertBestbuyDrop(sku, message, title):
    discord_webhook = "https://discordapp.com/api/webhooks/928735106607251537/_quj1kj1I_s21_3HnooY1_Fe7lqG4U_SdC9GeOcA_MviNJkYaHIKDmOqc3LsOKPsr4Pu"
    product_url = "https://www.bestbuy.com/site/%s.p?skuId=%s" % (
        sku, sku)
    bestbuy_drops_role = '<@&928733174157176843>'

    message = "%s: %s" % (message, product_url)

    alertDrop(discord_webhook=discord_webhook,
              mention_role=bestbuy_drops_role, message=message, title=title)


def alertEVGADrop(sku, message, title):
    discord_webhook = "https://discordapp.com/api/webhooks/928735356021530655/iQLi-UMFLvjvj7nO76_Y9pPeAgHUF7JTl6Hj8fGBh0haMoM4lssdPgnVb1UOOcIB7fvN"
    product_url = "https://www.evga.com/products/productlist.aspx?type=8"

    evga_drops_role = '<@&928733240037101578>'

    message = "%s: %s" % (message, product_url)

    alertDrop(discord_webhook=discord_webhook,
              mention_role=evga_drops_role, message=message, title=title)


def alertEbayDrop(message, title):
    discord_webhook = "https://discordapp.com/api/webhooks/928839319211343982/2GiSQyHfh6uJAeGn-2rDwwtaahKw3qUW23e6tF7qwMlYfrRfrPQIfpuJWgA5noUf-qF1"
    product_url = "https://www.ebay.com/sch/asus/m.html?item=403313960596&rt=nc&_trksid=p2047675.m3561.l2562"

    ebay_drops_role = '<@&928839535406772224>'

    message = "%s: %s" % (message, product_url)

    alertDrop(discord_webhook=discord_webhook,
              mention_role=ebay_drops_role, message=message, title=title)


def alertDrop(discord_webhook, mention_role, message, title):
    webhook = Webhook.from_url(
        discord_webhook, adapter=RequestsWebhookAdapter())

    embed = Embed()
    embed.description = "%s" % title

    webhook.send("{} {}".format(mention_role, message), embed=embed)
