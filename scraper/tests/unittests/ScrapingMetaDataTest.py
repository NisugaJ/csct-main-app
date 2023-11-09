import unittest
from bson import ObjectId

from scraper.src.data.prepare import get_scraping_meta_data
from scraper.src.models.scraping.ListPageMeta import ListPageMeta
from scraper.src.models.scraping.SupermarketMeta import SuperMarketMeta


class TestGetScrapingMetaData(
    unittest.TestCase
    ):
    def test_get_scraping_meta_data(self):
        data = get_scraping_meta_data()
        self.assertEqual(
            len(
                data
                ),
            1
            )
        self.assertIsInstance(
            data[0],
            SuperMarketMeta
            )

        supermarket = data[0]
        self.assertEqual(
            supermarket._id,
            ObjectId(
                "5f3e9a4f5b7d3d4c4c4c4c4c"
                )
            )
        self.assertEqual(
            supermarket.name,
            "ASDA"
            )
        self.assertEqual(
            supermarket.main_link,
            "https://groceries.asda.com"
            )
        self.assertEqual(
            len(
                supermarket.pages
                ),
            32
            )

        meat_page = supermarket.pages[0]
        self.assertIsInstance(
            meat_page,
            ListPageMeta
            )
        self.assertEqual(
            meat_page._id,
            ObjectId(
                "653406c5a0a41bf70329ee57"
                )
            )
        self.assertEqual(
            meat_page.link,
            "https://groceries.asda.com/search/meat-poultry-fish/products?page=1"
            )
        self.assertEqual(
            meat_page.product_type,
            "meat"
            )

        dairy_pages = [page for page in supermarket.pages if page.product_type == "dairy"]
        self.assertEqual(
            len(
                dairy_pages
                ),
            14
            )

        plant_based_pages = [page for page in supermarket.pages if page.product_type == "plant_based"]
        self.assertEqual(
            len(
                plant_based_pages
                ),
            17
            )


if __name__ == "__main__":
    unittest.main()