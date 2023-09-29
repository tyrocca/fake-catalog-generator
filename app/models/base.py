from pydantic import BaseModel
from typing import List

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
    id: str
    catalog_item_id: str
    category_id: str
