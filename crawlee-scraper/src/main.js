// For more information, see https://crawlee.dev/
import { BrowserName, DeviceCategory, OperatingSystemsName, ProxyConfiguration, PuppeteerCrawler} from 'crawlee';
import { router } from './routes.js';
import pushFileToBlobStorage from './utils/azure-blob-storage.js';
import { configDotenv } from 'dotenv';
import { env } from 'process';
import { proxies } from '../proxy-list.js';

configDotenv()

const startContext = {
    MEAT: [
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/chicken-turkey/1215135760597-910000975206-910000975462",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/beef/1215135760597-910000975206-910000975528",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/bacon-sausages-gammon/1215135760597-910000975206-910000975529",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/pork/1215135760597-910000975206-910000975676",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/lamb/1215135760597-910000975206-910000975607",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/extra-special-meat-fish/1215135760597-910000975206-1215685061664",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/duck-game-venison/1215135760597-910000975206-1215661251845",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/simple-to-cook/1215135760597-910000975206-1215285178174",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/slow-cooked/1215135760597-910000975206-1215686351330",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/liver/1215135760597-910000975206-1215423349781",
        "https://groceries.asda.com/aisle/fresh-food-bakery/meat-poultry/microwavable-snacks/1215135760597-910000975206-1215686011630",

        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/extra-special-fish/1215135760597-1215337195095-1215685901158",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/breaded-fish-fishcakes/1215135760597-1215337195095-1215685462261",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/salmon-tuna-trout/1215135760597-1215337195095-1215685901159",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/smoked-salmon/1215135760597-1215337195095-1215685901160",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/cod-haddock-white-fish/1215135760597-1215337195095-1215685901161",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/cooked-smoked-fillets/1215135760597-1215337195095-1215685901162",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/seafood-sticks-cocktails/1215135760597-1215337195095-1215685901163",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/prawns-mussels/1215135760597-1215337195095-1215685901164",
        "https://groceries.asda.com/aisle/fresh-food-bakery/fish-seafood/view-all-fish/1215135760597-1215337195095-1215685901166",

        "https://groceries.asda.com/dept/meat-poultry-fish/cooked-meat/1215135760597-1215661243132",
    ],
    MEAT_ALTERNATIVE: [

    ],
    DAIRY: [
        "https://groceries.asda.com/aisle/drinks/milk-yogurt-drinks/milk-drinks/1215135760614-1215685911674-1215685911675"
    ],
    DAIRY_ALTERNATIVE: [
        "https://groceries.asda.com/shelf/dietary-lifestyle/free-from/dairy-free-food-drink/view-all-dairy-free-food-drink/1215686355606-1215686355607-1215686355615-1215686355620?sort=price%3Aasc",
        "https://groceries.asda.com/shelf/dietary-lifestyle/free-from/milk-free-food-drink/view-all-milk-free-food-drink/1215686355606-1215686355607-1215686355627-1215686355632"
    ]
}

const startUrls = [].concat(startContext.DAIRY)

// [
//     "https://groceries.asda.com/search/meat-poultry-fish/products?page=5",
//     // 'https://groceries.asda.com/search/plant-based/products?cmpid=ahc-_-ghs-_-asdacom-_-hp-_-search-plant-based&page=3',
// ]
const proxtUrlList = [
    // env.IP_ROYAL_PROXY_URL,
    // ...proxies.free_proxy_list,
    // ...proxies.free_proxy_list,
    // ...proxies.proxyscrape_list,
    // ...proxies.proxyscrape_free_uk_list
]

const crawler = new PuppeteerCrawler({
    // proxy
    proxyConfiguration: new ProxyConfiguration({ proxyUrls: proxtUrlList}),

    // session
    useSessionPool: true,
    sessionPoolOptions: { maxPoolSize: 100 },
    persistCookiesPerSession: true,

    // requests
    requestHandler: router,
    maxRequestsPerCrawl: 300,
    retryOnBlocked: true,
    maxRequestRetries: 3,
    requestHandlerTimeoutSecs: 30,

    // browser 
    headless: false,

    // pre scraping hooks
    preNavigationHooks: [
        async ({ page }) => {
            await page.setRequestInterception(true);
            page.on('request', async (request) => {
                const type = request.resourceType();
                // request.url.toString().includes("ui.assets-asda") ||
				if ( type === 'image' || type === 'font') {
                    request.abort();
                }
				else 
                    request.continue();
            });
        }
    ],

    // browser pool options
    browserPoolOptions: {
        useFingerprints: true, // this is the default
        fingerprintOptions: {
            fingerprintGeneratorOptions: {
                browsers: [
                    BrowserName.chrome,
                    BrowserName.firefox,
                ],
                devices: [
                    DeviceCategory.mobile,
                    DeviceCategory.desktop,
                ],
                locales: [
                    'en-GB',
                ],
                operatingSystems:[
                    OperatingSystemsName.android,
                    OperatingSystemsName.ios,
                    OperatingSystemsName.windows,
                    OperatingSystemsName.linux,
                ]
            },
        },
    },
});


await crawler.run(startUrls);

const exportFilePath = 'storage/exports.json'

await crawler.exportData(exportFilePath, 'json');
await pushFileToBlobStorage(exportFilePath);
