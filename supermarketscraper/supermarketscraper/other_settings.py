from supermarketscraper.supermarketscraper.playwright.playwright_helpers import init_page

# Below settings should be imported and applied appropriately

DEFAULT_REQUEST_META = dict(
    playwright=True,
    playwright_include_page=True,
    playwright_page_init_callback=init_page
)