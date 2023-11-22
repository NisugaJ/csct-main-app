import datetime
import hashlib
import logging
from datetime import datetime
from random import Random

import scrapy
from scrapy_playwright.page import PageMethod

from supermarketscraper.supermarketscraper.other_settings import DEFAULT_REQUEST_META


class AsdaSpider(
    scrapy.Spider
    ):
    name = "asda-spider"

    asda_base_url = "https://groceries.asda.com"
    allowed_domains = ["asda.com"]
    url_with_page_attr = f"{asda_base_url}/search/meat-poultry-fish/products?page="

    def start_requests(self):
        yield scrapy.Request(
            f"{self.asda_base_url}/search/meat-poultry-fish/products?page=2",
            # headers={"User-Agent": "None"},
            meta=DEFAULT_REQUEST_META | dict(
                playwright_page_methods=[PageMethod(
                    "wait_for_selector",
                    "div.co-product",
                    timeout=40000
                ),  # PageMethod(
                    #     "evaluate",
                    #     "window.scrollBy(0, document.body.scrollHeight)"
                    # ),
                    # PageMethod(
                    #     "wait_for_selector",
                    #     "div.co-product:nth-child(50)"
                    # ),
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        logging.info(f"headers: {response.request.headers}")

        page = response.meta["playwright_page"]
        await page.screenshot(path=f"/main-app/app/public/images/example-{hashlib.md5(datetime.now())}.png", full_page=True)
        await page.close()

        for link in response.css("a.co-product__anchor::attr(href)"):
            print(f"link: {link.get()}")

            yield scrapy.Request(
                f"{self.asda_base_url}{link.get()}",
                # headers={"User-Agent": "None"},
                meta=DEFAULT_REQUEST_META | dict(
                    playwright_page_methods=[PageMethod(
                        "wait_for_selector",
                        "div.product-detail-page__main-cntr",
                        timeout=40000
                    )]
                ),
                callback=self.product_parse
            )

        # for request in self.search_page_request(f"{self.url_with_page_attr}{page_num}"):

        maxPages = int(
            response.css(
                "div.co-pagination__max-page a::text"
                ).get()
            )
        print(f"maxPages: {maxPages}")
        # for page_num in range(2, maxPages):
        #     for request in self.search_page_request(f"{self.url_with_page_attr}{page_num}"):
        #         yield request

    def product_parse(self, response):

        nutrient_rows = response.xpath("//div[contains(@class, 'pdp-description-reviews__nutrition-row') and contains(@class, 'pdp-description-reviews__nutrition-row--details')]")
        nutrients = []
        for row in nutrient_rows:
            nutrients.append(dict(
                name_raw=row.xpath("div[1]/text()").get(),
                portion_raw=row.xpath("div[2]/text()").get(),
                # portion_unit=row.xpath("div[1]/text()").get().rsplit(" ", 1)[1] or row.xpath("div[2]/text()").get()[-1] or "",
            ))

        yield {

            # E.g. extracting from 'https://ui.assets-asda.com/dm/asdagroceries/5054781686002_T1?defaultImage=asdagroceries/noImage&resMode=sharp2&id=YAbSt2&fmt=jpg&dpr=off&fit=constrain,1&wid=288&hei=288&qlt=5
            # 0'
            # "product_id": response.xpath("//div[@class = 'product-detail-page__zoomed-image-container']/div/picture/source/img/@src").get().split("dm/asdagroceries/")[1].split("_T1")[0],

            "product_id": response.url.rsplit("/", 1)[1] or "",
            "product_name": response.css("div.pdp-main-details div[data-auto-id='titleRating'] h1::text").get() or "",

            "price": {
                "selling_price": response.css("div.pdp-main-details__price-container strong::text").get()[1:] or "",
                "weight": response.css("div.pdp-main-details__weight::text").get().strip() or "",
            },
            "ingredients": "".join(response.xpath("(//div[@class = 'pdp-description-reviews__product-details-content'])[5]/text()").getall()) or None,
            "nutrients": nutrients or None,
            "customer_rating": float(response.xpath("//div[contains(@class, 'rating-stars__stars') and contains(@class, 'rating-stars__stars--top')]/@style").get().rsplit(": ", 1)[1].rsplit("%", 1)[0])/20 or None,
            "product_link": response.url,
            # "meat_alternative": False,
            # "meat_taste": False,
            # "meat_look": False,
            # "plant_based": False,
            # "dairy": False
        }

    def search_page_request(self, search_page_url):
        yield scrapy.Request(
            search_page_url,
            headers={"User-Agent": "None"},
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[PageMethod(
                    "wait_for_selector",
                    "div.co-product"
                ),  # PageMethod(
                    #     "evaluate",
                    #     "window.scrollBy(0, document.body.scrollHeight)"
                    # ),
                    # PageMethod(
                    #     "wait_for_selector",
                    #     "div.co-product:nth-child(50)"
                    # ),
                ]
            ),
            callback=self.parse
        )

