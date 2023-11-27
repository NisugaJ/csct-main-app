import datetime
import hashlib
import logging
from datetime import datetime
from random import Random

import scrapy
from requests import HTTPError
from scrapy_playwright.page import PageMethod
from twisted.internet.error import DNSLookupError

from supermarketscraper.supermarketscraper.other_settings import DEFAULT_REQUEST_META
from utils.supermarkets import UKSupermarkets, supermarket_prefix
from utils.utils import get_a_unique_image_name, val


class AsdaSpider(
    scrapy.Spider
    ):
    name = "asda-spider"

    asda_base_url = "https://groceries.asda.com"
    allowed_domains = ["asda.com"]
    url_with_page_attr = f"{asda_base_url}/search/meat-poultry-fish/products?page="

    def start_requests(self):
        yield scrapy.Request(
            f"{self.asda_base_url}/search/meat-poultry-fish/products?page=1",
            # "https://api.ipify.org/?format=json",
            # headers={"User-Agent": "None"},
            meta=DEFAULT_REQUEST_META | dict(
                playwright_page_methods=[
                    PageMethod(
                    "wait_for_selector",
                    "div.co-product",
                        timeout=40000
                    ),
                    PageMethod(
                        "evaluate",
                        "window.scrollBy(0, document.body.scrollHeight)",
                    ),
                    # PageMethod(
                    #     "wait_for_selector",
                    #     "div.co-product:nth-child(50)",
                    #     timeout=50000
                    # ),
                ],
            ),
            callback=self.parse,
            errback=self.on_error
        )

    async def parse(self, response):

        logging.info(f"headers: {response.request.headers}")

        page = response.meta["playwright_page"]
        await page.screenshot(path=f"/main-app/app/public/images/{get_a_unique_image_name()}", full_page=True)
        await page.close()

        for product_anchor in response.css("h3.co-product__title"):
            logging.info(f"product_anchor: {product_anchor}")
            link = product_anchor.css("a.co-product__anchor::attr(href)").get()
            product_id = supermarket_prefix(UKSupermarkets.ASDA) + val(link.rsplit("/", 1)[1])
            product_link = val(f"{self.asda_base_url}{link}")
            product_name = product_anchor.css("a.co-product__anchor::text").get()

            item = dict()
            item["product_id"] = product_id
            item["product_link"] = product_link
            item["product_name"] = product_name
            logging.info(f"yield_item: {item}")

            yield item

            # yield scrapy.Request(
            #     f"{self.asda_base_url}{link.get()}",
            #     # headers={"User-Agent": "None"},
            #     meta=DEFAULT_REQUEST_META | dict(
            #         playwright_page_methods=[PageMethod(
            #             "wait_for_selector",
            #             "div.product-detail-page__main-cntr",
            #             timeout=40000
            #         )]
            #     ),
            #     callback=self.product_parse
            # )


        maxPages = int(
            response.css(
                "div.co-pagination__max-page a::text"
                ).get()
            )
        logging.info(f"maxPages: {maxPages}")

        for page_num in range(2, maxPages):
            logging.info(f"Next page_num: {page_num}")
            yield scrapy.Request(
                f"{self.url_with_page_attr}{page_num}",
                # headers={"User-Agent": "None"},
                meta=DEFAULT_REQUEST_META | dict(
                    playwright_page_methods=[PageMethod(
                        "wait_for_selector",
                        "div.co-product",
                        timeout=40000
                    ),
                        PageMethod(
                            "evaluate",
                            "window.scrollBy(0, document.body.scrollHeight)"
                        ),
                        # PageMethod(
                        #     "wait_for_selector",
                        #     "div.co-product:nth-child(50)"
                        # ),
                    ], ),
                callback=self.parse,
                errback=self.on_error
            )


    def product_parse(self, response):
        product_id = val(response.url.rsplit("/", 1)[1])

        if len(response.css("div.pdp-main-details")) == 0:
            logging.info(f"div.pdp-main-details is unavailable. Skipping the product: {product_id}")
            return

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

            "product_id": product_id,
            "product_name": val(response.css("div.pdp-main-details div[data-auto-id='titleRating'] h1::text").get()),

            "price": {
                "selling_price": val(response.css("div.pdp-main-details__price-container strong::text").get())[1:] or "#not-found#",
                "weight": val(response.css("div.pdp-main-details__weight::text").get()).strip() or "#not-found#",
            },
            "ingredients": "".join(val(response.xpath("(//div[@class = 'pdp-description-reviews__product-details-content'])[5]/text()").getall())),
            "nutrients": nutrients or [],
            "customer_rating": val(
                float(
                    val(
                        val(
                            val(
                                response.xpath("//div[contains(@class, 'rating-stars__stars') and contains(@class, 'rating-stars__stars--top')]/@style").get()
                            )
                            .rsplit(": ", 1)[1]
                        )
                        .rsplit("%", 1)[0],
                        ""
                    )
                )/20,
                -99
            ),
            "product_link": response.url,
            # "meat_alternative": False,
            # "meat_taste": False,
            # "meat_look": False,
            # "plant_based": False,
            # "dairy": False
        }


    def on_error(self, failure):

        logging.error(f"failure: {failure}")

        # if isinstance(failure.value, HttpError):
        if failure.check(
                HTTPError
                ):
            # you can get the response
            response = failure.value.response
            logging.error(
                'HttpError on %s',
                response.url
                )

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(
                DNSLookupError
                ):
            # this is the original request
            request = failure.request
            logging.error(
                'DNSLookupError on %s',
                request.url
                )

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(
                TimeoutError
                ):
            request = failure.request
            logging.error(
                'TimeoutError on %s',
                request.url
                )

        yield scrapy.Request(
            failure.response.request.url,
            # "https://api.ipify.org/?format=json",
            # headers={"User-Agent": "None"},
            meta=DEFAULT_REQUEST_META.update() | dict(
                playwright_page_methods=[
                    PageMethod(
                    "wait_for_selector",
                    "div.co-product",
                        timeout=40000
                    ),
                    PageMethod(
                        "evaluate",
                        "window.scrollBy(0, document.body.scrollHeight)",
                    ),
                    # PageMethod(
                    #     "wait_for_selector",
                    #     "div.co-product:nth-child(50)",
                    #     timeout=50000
                    # ),
                ],
            ),
            callback=self.parse,
            errback=self.on_error
        )

