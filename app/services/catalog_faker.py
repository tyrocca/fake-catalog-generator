from faker import Faker
import ulid
import random
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from .cities import ADDRESS_DICT
from .data import CATEGORIES


ALTERABLE_FIELDS = {
    "id": "Unique Identifier -- A net new item will be created",
    "title": "Title Fields",
    "link": "Url",
    "description": "Description",
    "price": "Price, must be positive",
    "image_link": "Url of the Image",
    "inventory_policy": "Inventory Policy (Allow - 0, Deny - 1, Unknown - 2)",
    "inventory_quantity": "Inventory Quantity",
    "categories": "Category association - list of cataegories",
}

FIELD_OPTIONS = list(ALTERABLE_FIELDS.keys())


class CatalogItem(BaseModel):
    id: str
    title: str
    link: str
    description: str
    price: float
    image_link: str
    inventory_policy: int
    inventory_quantity: int
    categories: List[str]


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
    def _address(self) -> Dict[str, Any]:
        address = random.choice(ADDRESS_DICT["addresses"])
        return {
            "$address1": address["address1"],
            "$city": address.get("city", ""),
            "$region": address["state"],
            "$country": "US",
            "$zip": address["postalCode"],
        }

    @property
    def _product_title(self) -> str:
        color = self.color_name()
        career = self.job()
        name = self.name()
        return f"{color} {self._product} for a {career} | Designed by: {name}"

    @property
    def _product_description(self) -> str:
        return f"A {self.catch_phrase()} by {self.company()}. It will {self.bs()}!"

    @property
    def _inventory_quantity(self) -> int:
        """Return 0 33% or a random int"""
        return random.randint(0, 3) or random.randint(1, 999)

    @property
    def _categories(self) -> List[str]:
        return random.sample(CATEGORIES, random.randint(0, len(CATEGORIES)))

    # create new provider class
    def catalog_item(self, *, inventory_policy: int = 0) -> Dict[str, Any]:
        product_id = str(ulid.new())
        url = f"{self.url()}{product_id}"
        imgsize = random.randint(128, 1080)
        image = f"https://picsum.photos/{imgsize}"
        return {
            "id": product_id,
            "title": self._product_title,
            "link": url,
            "description": self._product_description,
            "price": random.randint(1, 2000) / 100,
            "image_link": image,
            "inventory_policy": inventory_policy,
            "inventory_quantity": self._inventory_quantity,
            "categories": self._categories,
            **self._address,
        }

    def alter_catalog_item(self, catalog_item: CatalogItem):
        attr = random.choice(("product_description", "inventory_quantity", "title"))

        # new_prop = getattr(catalog_item

        # catalog_item.

        return
