// For more information, see https://crawlee.dev/
import { BrowserName, DeviceCategory, OperatingSystemsName, ProxyConfiguration, PuppeteerCrawler} from 'crawlee';
import { router } from './routes.js';
import pushFileToBlobStorage from './utils/azure-blob-storage.js';
import fs from 'fs';
import { configDotenv } from 'dotenv';
import { env } from 'process';

configDotenv()

const startUrls = ['https://groceries.asda.com/search/meat-poultry-fish/products?page=1'];
const proxtUrlList = [
    env.IP_ROYAL_PROXY_URL,
].concat(
    //JSON.parse(fs.readFileSync('proxy-list.json')).proxy_list
)

const crawler = new PuppeteerCrawler({
    // proxy
    proxyConfiguration: new ProxyConfiguration({ proxyUrls: proxtUrlList}),

    // session
    useSessionPool: true,
    sessionPoolOptions: { maxPoolSize: 100 },
    persistCookiesPerSession: true,

    // requests
    requestHandler: router,
    maxRequestsPerCrawl: 20,
    retryOnBlocked: true,
    maxRequestRetries: 2,

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
