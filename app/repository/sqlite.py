from app.models.base import CatalogItem
from typing import List, Any, Tuple
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

CREATE_ITEM_SQL = """
INSERT INTO catalogitem (
    id,
    title,
    link,
    description,
    price,
    image_link,
    inventory_policy,
    inventory_quantity
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

GET_ITEM_SQL = """SELECT * FROM catalogitem WHERE id=?"""
GET_ITEMS_SQL = """SELECT * FROM catalogitem WHERE id in (?)"""

UPDATE_ITEM_SQL = """
UPDATE catalogitem SET (
    title = ?,
    description = ?,
    inventory_quantity = ?
) WHERE id = ?
"""

################################################################################
################################# VARIANT SQL ##################################
################################################################################

CREATE_VARIANT_SQL = """
INSERT INTO catalogvariant (
    id,
    catalog_item_id,
    title,
    link,
    description,
    price,
    image_link,
    inventory_policy,
    inventory_quantity
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

GET_VARIANT_SQL = """SELECT * FROM catalogvariant WHERE id=?"""
GET_VARIANTS_SQL = """SELECT * FROM catalogvariant WHERE id in (?)"""

UPDATE_VARIANT_SQL = """
UPDATE catalogvariant SET (
    title = ?,
    description = ?,
    inventory_quantity = ?
) WHERE id = ?
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
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self._init_tables()

    def _init_tables(self) -> bool:
        self.cursor.execute(ITEM_SCHEMA)
        self.cursor.execute(VARIANT_SCHEMA)
        self.cursor.execute(CATEGORY_SCHEMA)
        self.cursor.execute(MEMBERSHIP_SCHEMA)
        self.conn.commit()

    def get_item(self, pk: str) -> CatalogItem:
        self.cursor.execute(GET_ITEM_SQL, [pk])
        res = self.cursor.fetchone()
        return CatalogItem(**res)

    def get_items(self, pks: List[str]) -> List[CatalogItem]:
        self.cursor.execute(GET_ITEMS_SQL, [pks])
        return [CatalogItem(**r) for r in self.cursor.fetchall()]

    def update_item(self, pk: str, record: CatalogItem) -> int:
        self.cursor.execute(
            """
            UPDATE catalogitem SET (
                title = ?,
                description = ?,
                inventory_quantity = ?
            ) WHERE id = ?
            """,
            [record.title, record.description, record.inventory_quantity, record.id],
        )
        self.conn.commit()
        return 1

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

    def get_categories(self, pk: str) -> List[CatalogCategory]:
        ...

    def update_category(self, pk: str, record: CatalogCategory) -> int:
        ...

    def update_categories(self, pk: str, records: List[CatalogCategory]) -> int:
        ...

    def list_categories(self, cursor: Optional[str]) -> List[CatalogCategory]:
        ...
