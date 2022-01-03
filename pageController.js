const evgaCheckout = require('./evgaCheckout');

async function scrapeAll(browserInstance) {
    let browser;
    try {
        browser = await browserInstance;
        await evgaCheckout.scraper(browser);

    } catch (err) {
        console.log("Could not resolve the browser instance => ", err);
    } finally {
        browser.close();
    }
}

module.exports = (browserInstance) => scrapeAll(browserInstance);