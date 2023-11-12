import scrapy
from playwright.async_api import async_playwright


class AsdaSpider(
    scrapy.Spider
    ):
    name = "asda-spider"
    start_urls = [
        "data:,"
        # "https://quotes.toscrape.com/tag/humor/",
        # "https://groceries.asda.com/search/meat-poultry-fish/products?page=1"
    ]

    async def parse(self, response):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            page = await browser.new_page()
            await page.goto(
                "https://groceries.asda.com/search/meat-poultry-fish/products?page=1"
            )

            page_content = await page.content()

            # for quote in page.content().("div.co-product"):
            #     yield {
            #         "product_link": quote.xpath("div[2]/div[1]/h3/a/text()").get(),
            #         # "text": quote.css("span.text::text").get(),
            #     }
            #
            # next_page = response.css('li.next a::attr("href")').get()
            # if next_page is not None:
            #     yield response.follow(next_page, self.parse)

            title = await page.title()
            return {"title": title}
