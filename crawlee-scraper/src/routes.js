import { createPuppeteerRouter } from 'crawlee';

export const router = createPuppeteerRouter();

const productListItemSelector = 'div.co-item__title-container.co-item__title-container--rest-in-shelf > .co-product__title > .co-product__anchor'

router.addDefaultHandler(async ({page, enqueueLinks, log, proxyInfo }) => {
    log.info(`proxy: ${JSON.stringify(proxyInfo)}`);

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

router.addHandler('detail', async ({ request, page, pushData }) => {
    await page.waitForSelector('.pdp-main-details');
    await page.waitForNetworkIdle();

    const product_id = request.loadedUrl.split('/').pop();
    const product_name = await page.$eval(".pdp-main-details > div[data-auto-id='titleRating'] > h1", el => el.textContent);

    const price = {
        raw_selling_price: await page.$eval(".pdp-main-details__price-container > strong", el =>el.textContent.trim()),
        raw_weight: await page.$eval(".pdp-main-details__weight", el => el.textContent.trim()),
        raw_uom: await page.$eval(".co-product__price-per-uom", el => el.textContent.trim()),
    }

    const ingredients = (await page.$$eval(".pdp-description-reviews__product-details-cntr", elements => elements.map(el => {
        let ingredientsText = null
        if (el.children[0].innerHTML.toLowerCase().includes("ingredients") && el.children[1].innerHTML.length > 0){
            ingredientsText = el.children[1].innerHTML.trim().replace(/<\/?(span|strong)>/g, '')
        }
        return ingredientsText
    }))).filter(el => el != null)[0];

    const nutrients = await page.$$eval(".pdp-description-reviews__nutrition-row.pdp-description-reviews__nutrition-row--details", elements => elements.map(el => {
            const data = {}
            data.name_raw = el.children[0].innerHTML
            data.portion_raw = el.children[1].innerHTML
            return data;
        }),
    )

    const customer_rating = await page.$eval(".rating-stars__stars.rating-stars__stars--top", element => {
        let rating = -9
        if (element.getAttribute('style').includes("width")) 
            rating = Number(element.getAttribute('style').match(/width:\s*([0-9]+%)/)[1].split('%')[0]) / 20
        return rating
    })

    const product_type = "MEAT"
    await pushData({
        product_url: request.loadedUrl,
        product_id,
        product_name,
        price,
        ingredients,
        nutrients,
        customer_rating,
        product_type
    });
});


router.addHandler('next-page',   async ({ page, enqueueLinks }) => {
    await page.waitForSelector(productListItemSelector);
    await enqueueLinks({
        label: 'detail',
        selector: productListItemSelector,
    });
})