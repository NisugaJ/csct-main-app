import logging
from pprint import pprint

import scrapy
from scrapy_playwright.page import PageMethod


class AsdaSpider(scrapy.Spider):
    name = "asda-spider"

    allowed_domains = ["groceries.asda.com"]

    custom_settings = dict(
        PLAYWRIGHT_LAUNCH_OPTIONS={
            "timeout": 200 * 1000,  # 50 seconds
        }
    )

    def start_requests(self):
        # GET request
        yield scrapy.Request(
            "https://groceries.asda.com/search/meat-poultry-fish/products?page=1",
            headers={
               "User-Agent": None
            },
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        "wait_for_selector",
                        "div.co-product"
                        ),
                    # PageMethod(
                    #     "evaluate",
                    #     "window.scrollBy(0, document.body.scrollHeight)"
                    # ),
                    # PageMethod(
                    #     "wait_for_selector",
                    #     "div.co-product:nth-child(50)"
                    # ),
                ]
            ),
            errback=self.errback
        )

    async def parse(self, response):
        open(
            "response.html",
            "w"
            ).write(
            response.text
        )

        page = response.meta["playwright_page"]
        await page.screenshot(path="example.png", full_page=True)
        await page.close()


        for quote in response.css("div.co-product"):
            logging.info(
                "product::::: \n " + quote.text
            )
            yield {
                "product_link": quote.xpath(
                    "div[2]/div[1]/h3/a/text()"
                    ).get(),
                "text": quote.css(
                    "span.text::text"
                    ).get(),
            }

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

    async def errback(self, failure):
        pprint(failure)
        page = failure.request.meta["playwright_page"]
        await page.close()
