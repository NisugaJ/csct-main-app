import logging
from datetime import datetime
from pprint import pprint

import scrapy
from scrapy.utils.reactor import install_reactor
from scrapy_playwright.page import PageMethod


class AsdaSpider(scrapy.Spider):
    name = "asda-spider"

    allowed_domains = ["asda.com"]



    def start_requests(self):
        # GET request
        yield scrapy.Request(
            "https://groceries.asda.com/search/meat-poultry-fish/products?page=1",
            headers={
               "User-Agent": "None"
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
            # errback=self.errback
        )

    async def parse(self, response):
        open(
            "response.html",
            "w"
            ).write(
            response.text
        )

        page = response.meta["playwright_page"]
        await page.screenshot(path=f"/main-app/app/public/images/example-.png", full_page=True)
        await page.close()

        for quote in response.css("div.co-product"):
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

    # async def errback(self, failure):
    #     pprint(failure)
    #     pprint(failure.request.meta)
