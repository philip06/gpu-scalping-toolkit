const jsdom = require("jsdom");
const { JSDOM } = jsdom;


const checkoutObject = {
    url: `https://www.evga.com/Products/ProductList.aspx?type=8`,
    async scraper(browser) {
        const productNumber = "100-W1-0500-RX";
        // this.url = this.url.replace("SKU", sku).replace("SKU", sku);
        const page = await browser.newPage();
        await page.authenticate({
            username: 'coiaacye',
            password: 'kkul1ixr4jnp',
        });
        // const cartPage = await browser.newPage();
        // const buttonSelector = ".ctl00_LFrame_prdList_rlvProdList_ctrl0_ctrl1_btnAddCart";

        // // set user agent (override the default headless User Agent)
        // await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36');

        // // login first and we can go straight to /payment
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url, {
            waitUntil: 'domcontentloaded',
            timeout: 120000
        });

        const listContainerSelector = "#ctl00_LFrame_prdList_rlvProdList_ctrl0_pnlGroupContainer";
        await page.waitForSelector(listContainerSelector);

        const products = await page.evaluate(() => {
            const css = 'div.list-item';
            const products = [...document.querySelectorAll(css)];
            return products.map(p => p.textContent.match(/P\/N:\s(\S{3}-\S{2}-\S{4}-\S{2})/gm)[0].replace("P/N: ", ""));
        });

        const addToCartBtns = await page.$$('input.btnBigAddCart')

        for (let i = 0; i < products.length; i++) {
            const product = products[i];
            if (product === productNumber) {
                console.log(product);
                await addToCartBtns[i].click();
            }
        }



        await sleep(20000);

        // let selectorExists = null;
        // await page.$(buttonSelector);
        // let i = 0;
        // while (selectorExists === null) {
        //     await page.reload({ waitUntil: 'domcontentloaded' });
        //     console.log('reload');
        //     selectorExists = await page.$(buttonSelector);
        //     await page.screenshot({ path: `evga_bstock${i}.png` });
        //     i++;
        //     await sleep(15000);
        // }



        // await page.click(buttonSelector);

        // console.log('added to cart, loading cartPage');

        // await cartPage.reload({ waitUntil: 'domcontentloaded' });

        // console.log('finished loading cartPage');

        // await new Promise(r => setTimeout(r, 20000));

        // // await cartPage.waitForSelector('#checkoutApp > div.page-spinner.page-spinner--out > div:nth-child(1) > div.checkout.large-view > main > div.checkout__container > div.checkout__col.checkout__col--primary > form > section > div > div:nth-child(2) > div > div > button > span');

        // await cartPage.screenshot({ path: 'bestbuy_cart.png' });

        // await cartPage.click('#checkoutApp > div.page-spinner.page-spinner--out > div:nth-child(1) > div.checkout.large-view > main > div.checkout__container > div.checkout__col.checkout__col--primary > form > section > div > div:nth-child(2) > div > div > button > span');



        // await page.goto("https://www.bestbuy.com/cart", {
        //   waitUntil: 'domcontentloaded'
        // });

        // await cartPage.screenshot({ path: 'bestbuy_checkout.png' });

    }
};

// function checkForCards(page, rankedModels) {
//   rankedModels.forEach((model) => {
//     const selectorExists = await page.$(buttonSelector);

//     if (selectorExists) {

//     }
//   });
// }

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

module.exports = checkoutObject;