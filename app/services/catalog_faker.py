from faker import Faker
import ulid
import random


class CatalogItemGenerator(Faker):

    _FAKE_PRODUCTS = (
        "t-shirt",
        "pants",
        "shirt",
        "coffee mug",
        "sticker",
        "plush toy",
        "bobble head",
        "water bottle",
        "pjs",
        "desk lamp",
        "pot",
        "chariot",
    )

    @property
    def _product(self) -> str:
        return random.choice(self._FAKE_PRODUCTS)

    @property
    def _product_title(self) -> str:
        color = self.color()
        career = self.job()
        name = self.name()
        return f"{color} {self._product} for a {career} | Designed by: {name}"

    @property
    def _product_description(self) -> str:
        return f"A {self.catch_phrase()} by {self.company()}. It will {self.bs()}!"

    # create new provider class
    def catalog_item(self, *, inventory_policy=0):
        product_id = str(ulid.new())
        url = f"{self.url()}{product_id}"
        image = f"{url}.jpg"
        return {
            "id": product_id,
            "title": self._product_title,
            "link": url,
            "description": self._product_description,
            "price": random.randint(1, 2000) / 100,
            "image_link": image,
            "inventory_policy": inventory_policy,
            "inventory_quantity": random.choice([0, random.randint(1, 999)]),
            "categories": [],
        }

