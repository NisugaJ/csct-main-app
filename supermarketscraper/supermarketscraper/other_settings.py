import os
from pathlib import Path

from dotenv import load_dotenv

from supermarketscraper.supermarketscraper.playwright.playwright_helpers import init_page
from utils.proxy import ProxyList

# Below settings should be imported and applied appropriately
load_dotenv()
DEFAULT_REQUEST_META = {
    "playwright": True,
    "playwright_include_page": True,
    "playwright_page_init_callback": init_page,
}

if os.getenv("PROXY_MODE") == "IP_ROYAL_PROXY":
    ip_royal_proxy = {
        "proxy": {
            "server": f"{os.getenv('PROXY_HOST')}:{os.getenv('PROXY_PORT')}",
            "username": os.getenv("PROXY_USERNAME"),
            "password": os.getenv("PROXY_PASSWORD"),
        }
    }
    DEFAULT_REQUEST_META["playwright_context_kwargs"] = ip_royal_proxy

elif os.getenv("PROXY_MODE") == "PROXY_LIST":
    new_proxy = {
            "proxy": {
                "server": ProxyList(f"{Path.cwd()}/proxy-list.txt").pick_random_proxy()
            }
    }
    DEFAULT_REQUEST_META["playwright_context_kwargs"] = new_proxy


print(DEFAULT_REQUEST_META)