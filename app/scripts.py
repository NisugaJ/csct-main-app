from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.display import pprint
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
from twisted.internet import reactor

from supermarketscraper.supermarketscraper.spiders.scraper import AsdaSpider

def start_process():
    install_reactor(
        'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
    )
    pprint([{'key': i, 'value': get_project_settings().copy_to_dict()[i]} for i in get_project_settings().copy_to_dict()])
    process = CrawlerProcess(
        get_project_settings()
    )
    process.crawl(
        AsdaSpider
    )
    process.start()


def start_runner():
    install_reactor(
        'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
    )

    # TODO: Fix   File "/scraper/.venv/lib/python3.10/site-packages/playwright/async_api/_context_manager.py", line 31, in __aenter__
    #     loop = asyncio.get_running_loop()
    #     RuntimeError: no running event loop

    # configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    runner = CrawlerRunner(get_project_settings())
    runner.crawl(AsdaSpider)
    # runner.crawl(<Onother-Spider>) # Another spider

    d = runner.join()
    d.addBoth(
        lambda _: reactor.stop()
    )

    reactor.run()

def start_crawler_process():
    start_process()

start_crawler_process()