from abc import ABCMeta
from typing import List, Optional
from app.services.catalog_faker import CatalogItem, CatalogVariant, CatalogCategory


class BaseRepository(ABCMeta):
    ################################################################################
    ################################# CatalogItem ##################################
    ################################################################################

    def get_item(self, pk: str) -> CatalogItem:
        ...

    def get_items(self, pk: str) -> List[CatalogItem]:
        ...

    def update_item(self, pk: str, record: CatalogItem) -> int:
        ...

    def update_items(self, pk: str, records: List[CatalogItem]) -> int:
        ...

    def list_items(self, cursor: Optional[str]) -> List[CatalogItem]:
        ...

    ################################################################################
    ################################ CatalogVariant ################################
    ################################################################################

    def get_variant(self, pk: str) -> CatalogVariant:
        ...

    def get_variants(self, pk: str) -> List[CatalogVariant]:
        ...

    def update_variant(self, pk: str, record: CatalogVariant) -> int:
        ...

    def update_variants(self, pk: str, records: List[CatalogVariant]) -> int:
        ...

    def list_variants(self, cursor: Optional[str]) -> List[CatalogVariant]:
        ...


    ################################################################################
    ############################### CatalogCategory ################################
    ################################################################################

    def get_category(self, pk: str) -> CatalogCategory:
        ...

    def get_categorys(self, pk: str) -> List[CatalogCategory]:
        ...

    def update_category(self, pk: str, record: CatalogCategory) -> int:
        ...

    def update_categories(self, pk: str, records: List[CatalogCategory]) -> int:
        ...

    def list_categories(self, cursor: Optional[str]) -> List[CatalogCategory]:
        ...


