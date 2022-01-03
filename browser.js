const puppeteer = require('puppeteer');
const proxyChain = require('proxy-chain');

proxy_list = [
    "142.111.248.142:20000",
    "142.111.248.143:20000",
    "142.111.248.144:20000",
    "142.111.248.145:20000",
    "142.111.248.146:20000",
    "142.111.248.147:20000",
    "142.111.248.148:20000",
    "142.111.248.149:20000",
    "142.111.248.150:20000",
    "142.111.248.151:20000",
    "142.111.248.152:20000",
    "142.111.248.153:20000",
    "142.111.248.154:20000",
    "142.111.248.155:20000",
    "142.111.248.156:20000",
    "142.111.248.157:20000",
    "142.111.248.158:20000",
    "142.111.248.159:20000",
    "142.111.248.160:20000",
    "142.111.248.161:20000",
    "142.111.248.162:20000",
    "142.111.248.163:20000",
    "142.111.248.164:20000",
    "142.111.248.165:20000",
    "142.111.248.166:20000"
]

async function startBrowser() {
    let browser;
    try {
        const random_proxy = proxy_list[Math.floor(Math.random() * proxy_list.length)];
        console.log("Opening the browser......");
        browser = await puppeteer.launch({
            headless: false,
            args: [`--proxy-server=${random_proxy}`],
            'ignoreHTTPSErrors': true
        });
    } catch (err) {
        console.log("Could not create a browser instance => : ", err);
    }
    return browser;
}

module.exports = {
    startBrowser
};