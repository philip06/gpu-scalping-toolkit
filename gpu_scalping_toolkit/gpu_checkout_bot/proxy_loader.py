import zipfile

from selenium.webdriver.chrome.options import Options


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""


def get_chromedriver(use_proxy=False, user_agent=None, account_info={}):
    chrome_options = Options()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'
        background_js = f"""
var config = {{
    mode: "fixed_servers",
    rules: {{
        singleProxy: {{
        scheme: "http",
        host: "{account_info['proxy_host']}",
        port: parseInt({account_info['proxy_port']})
        }},
        bypassList: ["localhost"]
    }}
}};

chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{account_info['proxy_user']}",
            password: "{account_info['proxy_password']}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
);
"""

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    return chrome_options
