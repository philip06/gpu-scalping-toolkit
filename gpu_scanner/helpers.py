import random
import requests


def getUserAgent():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    ]
    return random.choice(user_agent_list)


def getProxyHash():
    response = requests.get(
        "https://proxy.webshare.io/proxy/list/download/fujbcavreomuaapgfhbbxewscntzpsiqrpehmoic/US/http/username/direct/")

    ret = []
    for x in response.text.split("\r\n"):
        if x != "":
            s = x.split(":")
            host, port, user, password = s
            ret.append({
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "valid": True
            })

    return ret


def getRandomValidProxy(proxy_hash_list: list):
    proxy_hash_list_valid = [x for x in proxy_hash_list if x["valid"]]
    return random.choice(proxy_hash_list_valid)
