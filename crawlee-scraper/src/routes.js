import { createPuppeteerRouter } from 'crawlee'

import { productExists } from './db/products.js'
import { supermarketPrefix, SupermarketType } from './utils/supermarkets.js'

export const router = createPuppeteerRouter()
router.use(async ({ log, request, proxyInfo, session }) => {
    log.info(`router: ${request.label}`);
    log.info(`proxy: ${JSON.stringify(proxyInfo)}`);
    log.info(`session: ${session.id}`);
})

const productListItemSelector = "ul.co-product-list__main-cntr > li.co-item > div > div.co-product div.co-item__col2 > div.co-item__title-container > .co-product__title > .co-product__anchor"

router.addDefaultHandler(async ({ page, enqueueLinks, log }) => {


    log.info(`enqueueing new URLs`);

    await page.waitForSelector(productListItemSelector);
    await enqueueLinks({
        label: 'detail',
        selector: productListItemSelector,
    });

    const nextBtnSelector = "a[data-auto-id='btnright']";
    const nextBtn = await page.$(nextBtnSelector);
    if (nextBtn) {
        await enqueueLinks({
            label: 'next-page',
            selector: nextBtnSelector,
        });
    }
});

router.addHandler('detail', async ({ request, page, pushData, log }) => {

    const productItem = {}

    productItem.product_url = request.loadedUrl
    productItem.product_type = "MEAT"

    await page.waitForSelector('.pdp-main-details');

    productItem.product_id = supermarketPrefix(SupermarketType.ASDA) + request.loadedUrl.split('/').pop();
    productItem.product_name = await page.$eval(".pdp-main-details > div[data-auto-id='titleRating'] > h1", el => el.textContent);

    const alreadyAvailable = await productExists(productItem.product_id);
    if(alreadyAvailable){
        const errorMessage = `Product(${productItem.product_id}): ${productItem.product_name} is already available.`
        log.error(errorMessage)
        await page.close();
        return
    }

    const sellingPriceSelector = ".pdp-main-details__price-container > strong"
    const rawWeightSelector = ".pdp-main-details__weight"
    const uomPriceSelector = ".co-product__price-per-uom"

    productItem.price = {}
    if((await page.$(sellingPriceSelector))){
        productItem.price.raw_selling_price = await page.$eval(sellingPriceSelector, el => el.textContent.trim())
    }
    if((await page.$(rawWeightSelector))){
        productItem.price.raw_weight = await page.$eval(rawWeightSelector, el => el.textContent.trim())
    }
    if((await page.$(uomPriceSelector))){
        productItem.price.raw_uom = await page.$eval(uomPriceSelector, el => el.textContent.trim())
    }

    const ingredientsSelector = ".pdp-description-reviews__product-details-cntr"
    if((await page.$(ingredientsSelector))){
        productItem.ingredients = (await page.$$eval(ingredientsSelector, elements => elements.map(el => {
            let ingredientsText = null
            if (el.children[0].innerHTML.toLowerCase().includes("ingredients") && el.children[1].innerHTML.length > 0) {
                ingredientsText = el.children[1].innerHTML.trim().replace(/<\/?(span|strong)>/g, '')
            }
            return ingredientsText
        }))).filter(el => el != null)[0];
    }

    const nutrientsSelector = ".pdp-description-reviews__nutrition-row.pdp-description-reviews__nutrition-row--details"
    if((await page.$(nutrientsSelector))){
        productItem.nutrients = await page.$$eval(nutrientsSelector, elements => elements.map(el => {
            const data = {}
            data.name_raw = el.children[0].innerHTML
            data.portion_raw = el.children[1].innerHTML
            return data;
        })
        )
    }

    const customerRatingSelector = ".rating-stars__stars.rating-stars__stars--top"
    if((await page.$(customerRatingSelector))){
        productItem.customer_rating = await page.$eval(customerRatingSelector, element => {
            let rating = -9
            if (element.getAttribute('style').includes("width"))
                rating = Number(element.getAttribute('style').match(/width:\s*([+]?[0-9]*\.?[0-9]+%)/)[1].split('%')[0]) / 20
            return rating
        })
    }

    
    await pushData(productItem);
});


router.addHandler('next-page', async ({ page, enqueueLinks }) => {
    await page.waitForSelector(productListItemSelector);
    await enqueueLinks({
        label: 'detail',
        selector: productListItemSelector,
    });
})