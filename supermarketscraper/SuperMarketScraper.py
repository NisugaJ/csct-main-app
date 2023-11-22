import os

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor

from supermarketscraper.supermarketscraper.spiders.AsdaSpider import AsdaSpider

class SuperMarketScraper:

    def __init__(self, runner=False):

        # The path seen from root, i.e. from main.py
        settings_file_path = os.getenv("SCRAPY_SETTINGS_PATH", "supermarketscraper.supermarketscraper.settings")

        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

        if runner:
            self.runner = CrawlerRunner(get_project_settings())
        else:
            self.process = CrawlerProcess(get_project_settings())

        self.spiders = [
            AsdaSpider
        ]

    def run_spiders(self):
        if self.process:
            for spider in self.spiders:
                self.process.crawl(spider)
            self.process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

        else:
            print("Process not set")

    def start_runner(self):
        install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

        from twisted.internet import reactor

        if self.runner:
            for spider in self.spiders:
                self.runner.crawl(spider)

            d = self.runner.join()
            d.addBoth(
                lambda _: reactor.stop()
            )

            reactor.run()

        else:
            print("Runner not set")

