from pydantic import BaseModel
from typing import List
import mmh3


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


class CatalogVariant(BaseModel):
    id: str
    catalog_item_id: str
    title: str
    link: str
    description: str
    price: float
    image_link: str
    inventory_policy: int
    inventory_quantity: int


class CatalogCategory(BaseModel):
    id: str
    name: str


class CategoryMembership(BaseModel):
    id: int
    catalog_item_id: str
    category_id: str


class CatalogEntity:
    key: str
    item: CatalogItem
    variants: List[CatalogVariant]
    categories: List[CatalogCategory]
    memberships: List[CategoryMembership]

    def __init__(
        self,
        item: CatalogItem,
        variants: List[CatalogVariant],
        categories: List[CatalogCategory],
    ):
        self.key = item.id
        self.item = item
        self.variants = variants
        self.categories = categories
        self.memberships = [
            CategoryMembership(
                id=mmh3.hash(f"{self.key}::{cat.id}", signed=False),
                catalog_item_id=self.item.id,
                category_id=cat.id,
            )
            for cat in self.categories
        ]
