import fs from 'fs';

export class AsdaScraper {

    constructor(browser) {
        this.start_url = "https://groceries.asda.com/search/meat-poultry-fish/products?page=1";
        this.browser = browser;
        this.page = null;

        this.baseUrl = "https://groceries.asda.com"
        this.searchResultSelector = '.co-product';

        this.productListData = [];

        this.detailPageCount = 0;

        this.isPageInUse = false;

        this.scrapedProductUrls = []
    }

    async prepare() {
        
        this.page = await this.browser.newPage();

        // Navigate the page to a URL
        await this.page.goto(this.start_url);

        // Set screen size
        await this.page.setViewport({width: 1080, height: 1024});

        // Wait and click on first result
        await this.page.waitForSelector(this.searchResultSelector, {timeout:20000});
    }

    async scrape() {
        this.productListData = await this.page.$$eval(this.searchResultSelector, elements => elements.map( element => {
            const productItem = {
                product_url: `${this.baseUrl}${element.querySelector('.co-product__anchor').href}`.trim().replace('undefined',''),
                product_name: element.querySelector('.co-product__anchor').innerText
            }

            return productItem
        }));

        console.log('productListData', this.productListData);
        await this.closePage(this.page)

        while (this.detailPageCount < 10) {
            this.productListData.map(async product => {
                if (product.product_url && !this.scrapedProductUrls.includes(product.product_url) && !this.isPageInUse) {
                    console.log("calling parseDetailsPage", product.product_url);
                    this.isPageInUse = true
                    await this.parseDetailsPage(product.product_url)
                 }
            });
        }
    }

    async parseDetailsPage(url) {
        console.log("inside parseDetailsPage", url)
        this.page = await this.browser.newPage()
        await this.page.goto(url)

        await this.page.waitForSelector('.pdp-main-details')

        const details = await this.page.$$eval('.pdp-main-details', elements => elements.map(element => {
            return element.innerHTML
        }))

        console.log("scraped ", url)
        console.log(details)

        fs.writeFileSync(`${this.detailPageCount}.html`, details)

        this.detailPageCount++
        this.scrapedProductUrls.push(url)

        this.page.close()

        this.isPageInUse = true
    }

    async closePage(page) {
        await page.close();
    }
}

