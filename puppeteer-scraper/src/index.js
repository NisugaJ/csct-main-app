import puppeteer from "puppeteer";

import {AsdaScraper} from "./scrapers/AsdaScraper.js"

const browser = await puppeteer.launch({headless: "new"});

const asdaScraper = new AsdaScraper(browser)

await asdaScraper.prepare()
await asdaScraper.scrape()

await browser.close()