from itertools import product

from bson import ObjectId

from scraper.src.models.scraping.ListPageMeta import ListPageMeta
from scraper.src.models.scraping.SupermarketMeta import SuperMarketMeta


def get_scraping_meta_data():
    data = [
        SuperMarketMeta(
            _id=ObjectId("5f3e9a4f5b7d3d4c4c4c4c4c"),
            name="ASDA",
            main_link="https://groceries.asda.com",
            pages=[
                # Meat
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee57"),
                    link='https://groceries.asda.com/search/meat-poultry-fish/products?page=1',
                    product_type="meat"
                ),

                # Dairy
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee67"),
                    link='https://groceries.asda.com/search/milk/products?page=1',
                    product_type="dairy",
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee77"),
                    link="https://groceries.asda.com/search/milk/products?page=2",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee77"),
                    link="https://groceries.asda.com/search/milk/products?page=3",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee87"),
                    link="https://groceries.asda.com/search/milk/products?page=4",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329ee97"),
                    link="https://groceries.asda.com/search/milk/products?page=5",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e107"),
                    link="https://groceries.asda.com/search/milk/products?page=6",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e117"),
                    link="https://groceries.asda.com/search/milk/products?page=7",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e127"),
                    link="https://groceries.asda.com/search/milk/products?page=8",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e137"),
                    link="https://groceries.asda.com/search/milk/products?page=9",
                    product_type="dairy"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e147"),
                    link="https://groceries.asda.com/search/milk/products?page=10",
                    product_type="dairy"),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e157"),
                    link="https://groceries.asda.com/search/milk/products?page=11",
                    product_type="dairy"),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e167"),
                    link="https://groceries.asda.com/search/milk/products?page=12",
                    product_type="dairy"),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e177"),
                    link="https://groceries.asda.com/search/milk/products?page=13",
                    product_type="dairy"),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e177"),
                    link="https://groceries.asda.com/search/milk/products?page=14",
                    product_type="dairy"),

                # Plant Based
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e187"),
                    link="https://groceries.asda.com/search/plant-based/products?page=1",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e197"),
                    link="https://groceries.asda.com/search/plant-based/products?page=2",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e207"),
                    link="https://groceries.asda.com/search/plant-based/products?page=3",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e217"),
                    link="https://groceries.asda.com/search/plant-based/products?page=4",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e227"),
                    link="https://groceries.asda.com/search/plant-based/products?page=5",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e237"),
                    link="https://groceries.asda.com/search/plant-based/products?page=6",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e247"),
                    link="https://groceries.asda.com/search/plant-based/products?page=7",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e257"),
                    link="https://groceries.asda.com/search/plant-based/products?page=8",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e267"),
                    link="https://groceries.asda.com/search/plant-based/products?page=9",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e277"),
                    link="https://groceries.asda.com/search/plant-based/products?page=10",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e287"),
                    link="https://groceries.asda.com/search/plant-based/products?page=11",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e297"),
                    link="https://groceries.asda.com/search/plant-based/products?page=12",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e307"),
                    link="https://groceries.asda.com/search/plant-based/products?page=13",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e317"),
                    link="https://groceries.asda.com/search/plant-based/products?page=14",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e327"),
                    link="https://groceries.asda.com/search/plant-based/products?page=15",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e337"),
                    link="https://groceries.asda.com/search/plant-based/products?page=16",
                    product_type="plant_based"
                ),
                ListPageMeta(
                    _id=ObjectId("653406c5a0a41bf70329e347"),
                    link="https://groceries.asda.com/search/plant-based/products?page=17",
                    product_type="plant_based"
                )
            ]
        ),

    ]

    return data
