from abc import ABC
from typing import List, Optional
from app.services.catalog_faker import CatalogItem, CatalogVariant, CatalogCategory


class BaseRepository(ABC):
    ################################################################################
    ################################# CatalogItem ##################################
    ################################################################################

    def create_item(self, record: CatalogItem) -> bool:
        ...

    def create_items(self, records: List[CatalogItem]) -> bool:
        ...

    def get_item(self, pk: str) -> CatalogItem:
        ...

    def get_items(self, pks: List[str]) -> List[CatalogItem]:
        ...

    def update_item(self, record: CatalogItem) -> int:
        ...

    def update_items(self, records: List[CatalogItem]) -> int:
        ...

    def list_items(self, cursor: Optional[str]) -> List[CatalogItem]:
        ...

    ################################################################################
    ################################ CatalogVariant ################################
    ################################################################################

    def create_variant(self, record: CatalogVariant) -> bool:
        ...

    def create_variants(self, records: List[CatalogVariant]) -> bool:
        ...

    def get_variant(self, pk: str) -> CatalogVariant:
        ...

    def get_variants(self, pks: List[str]) -> List[CatalogVariant]:
        ...

    def update_variant(self, record: CatalogVariant) -> int:
        ...

    def update_variants(self, records: List[CatalogVariant]) -> int:
        ...

    def list_variants(self, cursor: Optional[str]) -> List[CatalogVariant]:
        ...

    ################################################################################
    ############################### CatalogCategory ################################
    ################################################################################

    def create_category(self, record: CatalogCategory) -> bool:
        ...

    def create_categories(self, records: List[CatalogCategory]) -> bool:
        ...

    def get_category(self, pk: str) -> CatalogCategory:
        ...

    def get_categories(self, pks: List[str]) -> List[CatalogCategory]:
        ...

    def update_category(self, record: CatalogCategory) -> int:
        ...

    def update_categories(self, records: List[CatalogCategory]) -> int:
        ...

    def list_categories(self, cursor: Optional[str]) -> List[CatalogCategory]:
        ...
