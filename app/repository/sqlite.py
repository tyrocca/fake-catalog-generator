from app.models.base import (
    CatalogItem,
    CatalogVariant,
    CatalogCategory,
    CatalogEntity,
    CategoryMembership,
)
from typing import List, Any, Tuple, Optional
from .base import BaseRepository
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
)
"""

CATEGORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalogcategory (
    id TEXT PRIMARY KEY,
    name TEXT
)
"""

MEMBERSHIP_SCHEMA = """
CREATE TABLE IF NOT EXISTS catalogmembership (
    id INTEGER PRIMARY KEY,
    catalog_item_id TEXT,
    category_id TEXT
)
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
VALUES ({', '.join(('?',) * len(ITEM_COLS))})
"""

GET_ITEM_SQL = """SELECT * FROM catalogitem WHERE id=?"""
GET_ITEMS_SQL = """SELECT * FROM catalogitem WHERE id in (?)"""

UPDATE_ITEM_SQL = """
UPDATE catalogitem SET
    title = ?,
    description = ?,
    inventory_quantity = ?
WHERE id = ?
"""

################################################################################
################################# VARIANT SQL ##################################
################################################################################

VARIANT_COLS = (
    "id",
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
VALUES ({", ".join(('?',) * len(VARIANT_COLS))})
"""

GET_VARIANT_SQL = """SELECT * FROM catalogvariant WHERE id=?"""
GET_VARIANTS_SQL = """SELECT * FROM catalogvariant WHERE id in (?)"""

UPDATE_VARIANT_SQL = """
UPDATE catalogvariant SET
    title = ?,
    description = ?,
    inventory_quantity = ?
WHERE id = ?
"""

################################################################################
################################# Category SQL #################################
################################################################################

CREATE_CATEGORY_SQL = """INSERT INTO catalogcategory (id, name) VALUES (?, ?)"""
GET_CATEGORY_SQL = """SELECT * FROM catalogcategory WHERE id=?"""
GET_CATEGORIES_SQL = """SELECT * FROM catalogcategory WHERE id in (?)"""

################################################################################
################################ MEMBERSHIP SQL ################################
################################################################################

CREATE_MEMBERSHIP_SQL = """
INSERT INTO catalogmembership (id, catalog_item_id, category_id) VALUES (?, ?, ?)
"""

GET_ITEM_MEMBERSHIPS_SQL = """
SELECT * FROM catalogmembership WHERE catalog_item_id = ?
"""

GET_CATEGORY_MEMBERSHIP_SQL = """
SELECT * FROM catalogmembership WHERE category_id = ?
"""


class SQLiteRepository(BaseRepository):
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
        self.conn.commit()

    def create_item(self, record: CatalogItem) -> bool:
        self.cursor.execute(CREATE_ITEM_SQL, [getattr(record, f) for f in ITEM_COLS])
        self.conn.commit()
        return True

    def create_items(self, records: CatalogItem) -> bool:
        # TODO (tyrocca 2023-10-03): Add batching
        self.cursor.executemany(
            CREATE_ITEM_SQL, (tuple(getattr(r, f) for f in ITEM_COLS) for r in records)
        )
        self.conn.commit()
        return True

    def get_item(self, pk: str) -> CatalogItem:
        self.cursor.execute(GET_ITEM_SQL, [pk])
        res = self.cursor.fetchone()
        return CatalogItem(**res)

    def get_items(self, pks: List[str]) -> List[CatalogItem]:
        self.cursor.execute(GET_ITEMS_SQL, [pks])
        return [CatalogItem(**r) for r in self.cursor.fetchall()]

    def update_item(self, record: CatalogItem) -> int:
        self.cursor.execute(
            UPDATE_ITEM_SQL,
            [record.title, record.description, record.inventory_quantity, record.id],
        )
        self.conn.commit()
        return 1

    def update_items(self, records: List[CatalogItem]) -> int:
        self.cursor.execute(
            UPDATE_ITEM_SQL,
            tuple(
                tuple(r.title, r.description, r.inventory_quantity, r.id)
                for r in records
            ),
        )

    def list_items(self, cursor: Optional[str]) -> List[CatalogItem]:
        ...

    ################################################################################
    ################################ CatalogVariant ################################
    ################################################################################

    def create_variant(self, record: CatalogVariant) -> bool:
        self.cursor.execute(
            CREATE_VARIANT_SQL, [getattr(record, f) for f in VARIANT_COLS]
        )
        self.conn.commit()
        return True

    def create_variants(self, records: CatalogVariant) -> bool:
        # TODO (tyrocca 2023-10-03): Add batching
        self.cursor.executemany(
            CREATE_VARIANT_SQL,
            (tuple(getattr(r, f) for f in VARIANT_COLS) for r in records),
        )
        self.conn.commit()
        return True

    def get_variant(self, pk: str) -> CatalogVariant:
        self.cursor.execute(GET_VARIANT_SQL, [pk])
        res = self.cursor.fetchone()
        return CatalogVariant(**res)

    def get_variants(self, pks: List[str]) -> List[CatalogVariant]:
        self.cursor.execute(GET_VARIANTS_SQL, [pks])
        return [CatalogVariant(**r) for r in self.cursor.fetchall()]

    def update_variant(self, record: CatalogVariant) -> int:
        self.cursor.execute(
            UPDATE_VARIANT_SQL,
            [record.title, record.description, record.inventory_quantity, record.id],
        )
        self.conn.commit()
        return 1

    def update_variants(self, records: List[CatalogVariant]) -> int:
        self.cursor.execute(
            UPDATE_VARIANT_SQL,
            tuple(
                tuple(r.title, r.description, r.inventory_quantity, r.id)
                for r in records
            ),
        )

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


"""

from app.repository.sqlite import *
from app.services.catalog_faker import *
g = CatalogItemGenerator()
r = SQLiteRepository()
i = g.get_catalog_item()
r.create_item(i)

g.alter_catalog_item(i)

r.update_item(i)

# def function make_items(num):
#     for _ in range(num):
#         i = g.g
#         r.create_item(

"""
