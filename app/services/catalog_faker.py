from faker import Faker
import ulid
import mmh3
import random
from typing import Dict, Any, Optional, List, Tuple, Union
from app.models.base import CatalogCategory, CatalogEntity, CatalogVariant, CatalogItem

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

    _MUTABLE_FIELDS: Tuple[Tuple[str, str], ...] = (
        ("title", "_product_title"),
        ("description", "_product_description"),
        ("inventory_quantity", "_inventory_quantity"),
        # ("categories", "_categories"),
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

    @property
    def _base_catalog_dict(self) -> Dict[str, Union[int, str, float]]:
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
            "inventory_policy": 0,  # default
            "inventory_quantity": self._inventory_quantity,
        }

    # create new provider class
    def catalog_item(
        self, *, with_address: bool = True, with_categories: bool = True
    ) -> Dict[str, Any]:
        return {
            **self._base_catalog_dict,
            **({"categories": self._categories} if with_categories else {}),
            **(self._address if with_address else {}),
        }

    ################################################################################
    ########################## Full Object Manipulations ###########################
    ################################################################################

    def get_categories(
        self, names: Optional[List[str]] = None
    ) -> List[CatalogCategory]:
        cat_names = self._categories if names is None else names
        return [
            CatalogCategory(id=f"{mmh3.hash(cat,signed=False)}", name=cat)
            for cat in cat_names
        ]

    def get_variants(self, item_pk: str, variant_ids=None) -> List[CatalogVariant]:
        num_variants = random.randint(0, 100)
        return [
            CatalogVariant(catalog_item_id=item_pk, **self._base_catalog_dict)
            for _ in range(num_variants)
        ]

    def get_catalog_item(self) -> CatalogItem:
        return CatalogItem(
            **self.catalog_item(with_address=False, with_categories=False)
        )

    def get_catalog_entity(self) -> CatalogEntity:
        item = self.get_catalog_item()
        categories = self.get_categories()
        return CatalogEntity(
            item=item,
            variants=self.get_variants(item.id),
            categories=categories,
        )

    ################################################################################
    ############################### Mutation Helpers ###############################
    ################################################################################

    def alter_catalog_dict(self) -> Dict[str, Any]:
        updated_props: List[Tuple[str, str]] = random.sample(
            self._MUTABLE_FIELDS, random.randint(0, len(self._MUTABLE_FIELDS))
        )
        return {attr: getattr(self, method) for attr, method in updated_props}

    def alter_catalog_item(self, catalog_item: CatalogItem):
        update_dict = self.alter_catalog_dict()

        for attr, value in update_dict.items():
            setattr(catalog_item, attr, value)

        return catalog_item
