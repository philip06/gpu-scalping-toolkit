from discord import Webhook, RequestsWebhookAdapter, Embed

my_id = '<@119889394470617088>'


def alertBestbuyDrop(sku, message, title):
    discord_webhook = "https://discordapp.com/api/webhooks/926904611082739733/H1ofplv4PUp_JVXhnao134nFiVBkK9wsWccvySIaF_BRsvJb2TU8a8RMcm4D9UHCjwhz"
    product_url = "https://www.bestbuy.com/site/%s.p?skuId=%s" % (
        sku, sku)
    bestbuy_drops_role = '<@&926967141922660352>'

    message = "%s: %s" % (message, product_url)

    alertDrop(discord_webhook=discord_webhook,
              mention_role=bestbuy_drops_role, message=message, title=title)


def alertEVGADrop(sku, message, title):
    discord_webhook = "https://discordapp.com/api/webhooks/926980924577574984/NXn-79-XlKLWbM8f1UWAs5SN_A044QQSuZ6eFs-HcaKEpVKFiKefiHpU-aCzUu6hj2Lc"
    product_url = "https://www.evga.com/products/productlist.aspx?type=8"

    evga_drops_role = '<@&926967536115908638>'

    message = "%s: %s" % (message, product_url)

    alertDrop(discord_webhook=discord_webhook,
              mention_role=evga_drops_role, message=message, title=title)


def alertDrop(discord_webhook, mention_role, message, title):
    webhook = Webhook.from_url(
        discord_webhook, adapter=RequestsWebhookAdapter())

    embed = Embed()
    embed.description = "%s" % title

    webhook.send("{} {}".format(mention_role, message), embed=embed)
