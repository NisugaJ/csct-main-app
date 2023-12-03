// For more information, see https://crawlee.dev/
import { Dataset, PuppeteerCrawler} from 'crawlee';
import { router } from './routes.js';

const startUrls = ['https://groceries.asda.com/search/meat-poultry-fish/products?page=1'];

const crawler = new PuppeteerCrawler({
    // proxyConfiguration: new ProxyConfiguration({ proxyUrls: ['...'] }),
    requestHandler: router,
    maxRequestsPerCrawl: 2,
    headless: false,
    retryOnBlocked: true,
    maxRequestRetries: 2,
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

    
});

 
await crawler.run(startUrls);
const data = await crawler.getData();
console.log(data)

