from app.models.base import (
    CatalogItem,
    CatalogVariant,
    CatalogCategory,
    CatalogEntity,
    CategoryMembership,
)
from typing import Dict, Iterable, List, Any, ParamSpec, Tuple, Optional, Type, Union
from .base import BaseRepository, QueryCursor, Sort
import sqlite3


ITEM_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalogitem (
    id TEXT PRIMARY KEY,
    title TEXT,
    link TEXT,
    description TEXT,
    price NUMERIC,
    image_link TEXT,
    inventory_policy INT,
    inventory_quantity INT
)
"""

VARIANT_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalogvariant (
    id TEXT PRIMARY KEY,
    catalog_item_id TEXT,
    title TEXT,
    link TEXT,
    description TEXT,
    price NUMERIC,
    image_link TEXT,
    inventory_policy INT,
    inventory_quantity INT
)"""

VARIANT_INDEX = """
CREATE INDEX IF NOT EXISTS variantbyitem
ON catalogvariant (catalog_item_id)
"""

CATEGORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalogcategory (
    id TEXT PRIMARY KEY,
    name TEXT
)
"""

MEMBERSHIP_SCHEMA = """
CREATE TABLE IF NOT EXISTS categorymembership (
    id TEXT PRIMARY KEY,
    catalog_item_id TEXT,
    category_id TEXT
)
"""

ITEM_CATEGORY_INDEX = """
CREATE INDEX IF NOT EXISTS memberbyitem
ON categorymembership (catalog_item_id)
"""

CATEGORY_MEMBER_INDEX = """
CREATE INDEX IF NOT EXISTS memberbycategory
ON categorymembership (category_id)
"""

################################################################################
################################### ITEM SQL ###################################
################################################################################

ITEM_COLS = (
    "id",
    "title",
    "link",
    "description",
    "price",
    "image_link",
    "inventory_policy",
    "inventory_quantity",
)
CREATE_ITEM_SQL = f"""
INSERT INTO catalogitem ({', '.join(ITEM_COLS)})
VALUES ({  ", ".join(f':{c}' for c in ITEM_COLS) })
"""

GET_ITEM_SQL = """SELECT * FROM catalogitem WHERE id=?"""
GET_ITEMS_SQL = """SELECT * FROM catalogitem WHERE id IN"""

UPDATE_ITEM_SQL = """
UPDATE catalogitem SET
    title = :title,
    description = :description,
    inventory_quantity = :inventory_quantity
WHERE id = :id
"""

################################################################################
################################# VARIANT SQL ##################################
################################################################################

VARIANT_COLS = (
    "id",
    "catalog_item_id",
    "title",
    "link",
    "description",
    "price",
    "image_link",
    "inventory_policy",
    "inventory_quantity",
)

CREATE_VARIANT_SQL = f"""
INSERT INTO catalogvariant ({', '.join(VARIANT_COLS)})
VALUES ({  ", ".join(f':{c}' for c in VARIANT_COLS) })
"""

GET_VARIANT_SQL = """SELECT * FROM catalogvariant WHERE id=?"""
GET_VARIANTS_SQL = """SELECT * FROM catalogvariant WHERE id IN"""
GET_VARIANTS_BY_ITEM_SQL = """SELECT * FROM catalogvariant WHERE catalog_item_id IN"""

UPDATE_VARIANT_SQL = """
UPDATE catalogvariant SET
    title = :title,
    description = :description,
    inventory_quantity = :inventory_quantity
WHERE id = :id
"""

################################################################################
################################# Category SQL #################################
################################################################################

CREATE_CATEGORY_SQL = """
INSERT INTO catalogcategory (id, name) VALUES (:id, :name)
ON CONFLICT DO NOTHING
"""
GET_CATEGORY_SQL = """SELECT * FROM catalogcategory WHERE id=?"""
GET_CATEGORIES_SQL = """SELECT * FROM catalogcategory WHERE id IN"""

################################################################################
################################ MEMBERSHIP SQL ################################
################################################################################

CREATE_MEMBERSHIP_SQL = """
INSERT INTO categorymembership (id, catalog_item_id, category_id)
VALUES (:id, :catalog_item_id, :category_id)
ON CONFLICT DO NOTHING
"""

DELETE_MEMBERSHIP_SQL = """DELETE FROM categorymembership WHERE id IN"""

GET_ITEM_MEMBERSHIPS_SQL = """
SELECT * FROM categorymembership WHERE catalog_item_id IN
"""

GET_CATEGORY_MEMBERSHIP_SQL = """
SELECT * FROM categorymembership WHERE category_id IN
"""

CatalogType = Union[CatalogCategory, CatalogItem, CatalogVariant, CatalogCategory]


class SQLiteRepository(BaseRepository):
    PAGE_SIZE = 1000

    def __init__(self, dbname: str = ":memory:"):
        self._db_name = dbname
        self._cursor = None
        self._conn = None
        self._init_tables()

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_name)
            self._conn.row_factory = sqlite3.Row

        return self._conn

    @property
    def cursor(self) -> sqlite3.Cursor:
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    def close_cursor(self) -> bool:
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        return True

    def close_conn(self) -> bool:
        self.close_cursor()
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        return True

    def _init_tables(self) -> bool:
        self.cursor.execute(ITEM_SCHEMA)
        self.cursor.execute(VARIANT_SCHEMA)
        self.cursor.execute(CATEGORY_SCHEMA)
        self.cursor.execute(MEMBERSHIP_SCHEMA)
        # Indexes
        self.cursor.execute(VARIANT_INDEX)
        self.cursor.execute(ITEM_CATEGORY_INDEX)
        self.cursor.execute(CATEGORY_MEMBER_INDEX)
        self.conn.commit()

    ################################################################################
    ################################# SQL Helpers ##################################
    ################################################################################

    def _create_helper(self, statement: str, record: CatalogType) -> int:
        self.cursor.execute(statement, record.dict())
        self.conn.commit()
        return 1

    def _creates_helper(self, statement: str, records: List[CatalogType]) -> int:
        self.cursor.executemany(statement, tuple(r.dict() for r in records))
        self.conn.commit()
        return len(records)

    def _get_helper(
        self, statement: str, out_type: CatalogType, pk: str
    ) -> CatalogType:
        self.cursor.execute(statement, [pk])
        res = self.cursor.fetchone()
        return out_type(**res)

    def _in_builder(self, statement: str, params: List[str]) -> str:
        return f"{statement} ({','.join('?'*len(params))})"

    def _gets_helper(
        self, statement: str, out_type: CatalogType, pks: List[str]
    ) -> List[CatalogType]:
        in_clause = self._in_builder(statement, pks)
        self.cursor.execute(in_clause, pks)
        return [out_type(**r) for r in self.cursor.fetchall()]

    def _update_helper(self, statement: str, record: CatalogType) -> int:
        self.cursor.execute(statement, record.dict())
        self.conn.commit()
        return 1

    def _updates_helper(self, statement: str, records: List[CatalogType]) -> int:
        self.cursor.executemany(
            statement,
            tuple(r.dict() for r in records),
        )
        return len(records)

    def _delete_helper(self, statement: str, pks: List[Any]) -> int:
        self.cursor.execute(self._in_builder(statement, pks), pks)
        self.conn.commit()
        return len(pks)

    def _list_helper(
        self, table: str, out_type: Type, cursor: QueryCursor, limit: Optional[int]
    ) -> Iterable[Type]:
        num_returned = 0
        while True:
            request_size = min(limit or self.PAGE_SIZE, self.PAGE_SIZE)
            self.cursor.execute(
                f"""SELECT * FROM {table} WHERE id > ? {cursor.sort.value} LIMIT ?""",
                [cursor.next_id, request_size],
            )
            results = [out_type(**r) for r in self.cursor.fetchall()]
            if not results:
                break

            for r in results:
                num_returned += 1
                yield r
                if limit and num_returned == limit:
                    return
            cursor = QueryCursor(sort=cursor.sort, next_id=results[-1].id)

    ################################################################################
    ################################### Item Ops ###################################
    ################################################################################
    def create_item(self, record: CatalogItem) -> int:
        return self._create_helper(CREATE_ITEM_SQL, record)

    def create_items(self, records: CatalogItem) -> int:
        return self._creates_helper(CREATE_ITEM_SQL, records)

    def get_item(self, pk: str) -> CatalogItem:
        return self._get_helper(GET_ITEM_SQL, CatalogItem, pk)

    def get_items(self, pks: List[str]) -> List[CatalogItem]:
        return self._gets_helper(GET_ITEMS_SQL, CatalogItem, pks)

    def update_item(self, record: CatalogItem) -> int:
        return self._update_helper(UPDATE_ITEM_SQL, record)

    def update_items(self, records: List[CatalogItem]) -> int:
        return self._updates_helper(UPDATE_ITEM_SQL, records)

    def list_items(
        self,
        cursor: Optional[QueryCursor] = QueryCursor(sort=Sort.ID_ASC, next_id=""),
        limit: Optional[int] = None,
    ) -> Iterable[CatalogItem]:
        return self._list_helper(
            table="catalogitem",
            out_type=CatalogItem,
            cursor=cursor,
            limit=limit,
        )

    ################################################################################
    ################################ CatalogVariant ################################
    ################################################################################
    def create_variant(self, record: CatalogVariant) -> int:
        return self._create_helper(CREATE_VARIANT_SQL, record)

    def create_variants(self, records: List[CatalogVariant]) -> int:
        return self._creates_helper(CREATE_VARIANT_SQL, records)

    def get_variant(self, pk: str) -> CatalogVariant:
        return self._get_helper(GET_VARIANT_SQL, CatalogVariant, pk)

    def get_variants(self, pks: List[str]) -> List[CatalogVariant]:
        return self._gets_helper(GET_VARIANTS_SQL, CatalogVariant, pks)

    def get_item_variants(self, item_pk: str) -> List[CatalogVariant]:
        return self._gets_helper(GET_VARIANTS_BY_ITEM_SQL, CatalogVariant, [item_pk])

    def update_variant(self, record: CatalogVariant) -> int:
        return self._update_helper(UPDATE_VARIANT_SQL, record)

    def update_variants(self, records: List[CatalogVariant]) -> int:
        return self._updates_helper(UPDATE_VARIANT_SQL, records)

    def list_variants(
        self,
        cursor: Optional[QueryCursor] = QueryCursor(sort=Sort.ID_ASC, next_id=""),
        limit: Optional[int] = None,
    ) -> Iterable[CatalogVariant]:
        return self._list_helper(
            table="catalogvariant",
            out_type=CatalogVariant,
            cursor=cursor,
            limit=limit,
        )

    ################################################################################
    ############################### CatalogCategory ################################
    ################################################################################

    def create_category(self, record: CatalogCategory) -> bool:
        return self._create_helper(CREATE_CATEGORY_SQL, record)

    def create_categories(self, records: CatalogCategory) -> bool:
        return self._creates_helper(CREATE_CATEGORY_SQL, records)

    def get_category(self, pk: str) -> CatalogCategory:
        return self._get_helper(GET_CATEGORY_SQL, CatalogCategory, pk)

    def get_categories(self, pks: List[str]) -> List[CatalogCategory]:
        return self._gets_helper(GET_CATEGORIES_SQL, CatalogCategory, pks)

    def update_category(self, record: CatalogCategory) -> int:
        raise NotImplementedError()

    def update_categories(self, records: List[CatalogCategory]) -> int:
        raise NotImplementedError()

    def list_categories(
        self,
        cursor: Optional[QueryCursor] = QueryCursor(sort=Sort.ID_ASC, next_id=""),
        limit: Optional[int] = None,
    ) -> Iterable[CatalogCategory]:
        return self._list_helper(
            table="catalogcategory",
            out_type=CatalogCategory,
            cursor=cursor,
            limit=limit,
        )

    def patch_categories(self, categories: List[CatalogCategory]) -> int:
        cat_dict = {c.id: c for c in categories}
        cur_cats = self.get_categories(list(cat_dict.keys()))
        cat_exists = {c.id for c in cur_cats}
        to_create = [c for pk, c in cat_dict.items() if pk not in cat_exists]
        self.create_categories(to_create)
        return len(to_create)

    ################################################################################
    ################################# Memberships ##################################
    ################################################################################

    def create_membership(self, record: CategoryMembership) -> bool:
        return self._create_helper(CREATE_MEMBERSHIP_SQL, record)

    def create_memberships(self, records: List[CategoryMembership]) -> bool:
        return self._creates_helper(CREATE_MEMBERSHIP_SQL, records)

    def get_item_memberships(self, item_pk: str) -> List[CategoryMembership]:
        return self._gets_helper(
            GET_ITEM_MEMBERSHIPS_SQL, CategoryMembership, [item_pk]
        )

    def get_item_categories(self, item_pk: str) -> List[CatalogCategory]:
        memberships = self.get_item_memberships(item_pk)
        return self.get_categories([m.category_id for m in memberships])

    def get_category_memberships(self, category_pk: str) -> List[CategoryMembership]:
        return self._get_helper(
            GET_CATEGORY_MEMBERSHIP_SQL, CategoryMembership, [category_pk]
        )

    def get_category_items(self, category_pk: str) -> List[CatalogItem]:
        memberships = self.get_category_memberships(category_pk)
        return self.get_items([m.catalog_item_id for m in memberships])

    def delete_memberships(self, pks: List[int]) -> int:
        return self._delete_helper(DELETE_MEMBERSHIP_SQL, pks)

    def patch_membership(
        self, item_pk: str, memberships: List[CategoryMembership]
    ) -> Tuple[int, int]:
        # TODO (tyrocca 2023-10-06): hit members directly
        mems = {m.id for m in memberships}
        cur_mems = {m.id: m for m in self.get_item_memberships(item_pk)}

        delete_mem_ids = list(cur_mems.keys() - mems)
        new_mems = [m for m in memberships if m.id not in cur_mems]

        deleted = self.delete_memberships(delete_mem_ids)
        added = self.create_memberships(new_mems)

        return added, deleted

    ################################################################################
    ################################ CatalogEntity #################################
    ################################################################################

    def _hydrate_entity(self, item: CatalogItem) -> CatalogEntity:
        variants = self.get_item_variants(item.id)
        categories = self.get_item_categories(item.id)
        return CatalogEntity(item=item, variants=variants, categories=categories)

    def get_catalog_entity(self, pk: str) -> CatalogEntity:
        item = self.get_item(pk)
        return self._hydrate_entity(item)

    def get_catalog_entities(self, pks: List[str]) -> List[CatalogEntity]:
        # TODO (tyrocca 2023-10-06): bulk retrieve
        return [self._hydrate_entity(item) for item in self.get_items(pks)]

    def create_catalog_entity(self, catalog_entity: CatalogEntity) -> bool:
        self.create_item(catalog_entity.item)
        self.create_variants(catalog_entity.variants)
        self.patch_categories(catalog_entity.categories)
        self.patch_membership(catalog_entity.key, catalog_entity.get_memberships())
        return True

    def update_catalog_entity(self, catalog_entity: CatalogEntity) -> int:
        self.update_item(catalog_entity.item)
        self.update_variants(catalog_entity.variants)
        self.patch_categories(catalog_entity.categories)
        self.patch_membership(catalog_entity.key, catalog_entity.get_memberships())
        return 1

    def update_catalog_entities(self, catalog_entities: List[CatalogEntity]) -> int:
        items = []
        variants = []
        categories: Dict[str, CatalogCategory] = {}
        for entity in catalog_entities:
            items.append(entity.item)
            variants += entity.variants
            for cat in entity.categories:
                categories[cat.id] = cat

        items_updated = self.update_items(items)
        variants_updated = self.update_variants(variants)
        self.patch_categories(list(categories.values()))

        return items_updated + variants_updated


"""

from app.repository.sqlite import *
from app.services.catalog_faker import *
g = CatalogItemGenerator()
r = SQLiteRepository()
i = g.get_catalog_item()
r.create_item(i)

g.alter_catalog_item(i)

r.update_item(i)

items = [g.get_catalog_item() for _ in range(1000)]

r.create_items(items)
r.get_items([i.id for i in items])

e = g.get_catalog_entity()
print('cats', len(e.categories))
r.create_catalog_entity(e)
e_read = r.get_catalog_entity(e.key)

print('cats', len(e_read.categories))

e_new = g.alter_catalog_entity(e)
r.update_catalog_entity(e_new)

"""
