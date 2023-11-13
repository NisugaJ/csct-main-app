import logging

import scrapy
from playwright.async_api import async_playwright


class AsdaSpider(
    scrapy.Spider
    ):
    name = "asda-spider"
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",
        "https://groceries.asda.com/search/meat-poultry-fish/products?page=1"
    ]

    def start_requests(self):
        # GET request
        yield scrapy.Request(
            self.start_urls[1],
            meta={"playwright": True}
        )

    def parse(self, response):
        for quote in response.css("div.co-product"):
            logging.info(
                "Response::::: \n " + quote.text
                )
            yield {
                "product_link": quote.xpath("div[2]/div[1]/h3/a/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
