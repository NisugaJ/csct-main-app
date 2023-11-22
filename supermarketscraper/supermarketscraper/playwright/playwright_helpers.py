#  Helper functions for playwright
#  Copyright (c) 2023, Supermarketscraper

"""
Add page methods for playwright before initializing a page

Args:
    page (Page): The page object to initialize.
    request (Request): The request object.

Returns:
    None
"""
import logging


async def init_page(page, request):
    logging.info("Initializing playwright page")
    # Avoid loading images & videos
    await page.route("**/*.{png,jpg,jpeg,mp4}", lambda route: route.abort())

