from fastapi import APIRouter, HTTPException
from app.services.catalog_faker import CatalogItemGenerator

router = APIRouter()


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.get("/random/{count}")
async def fake_catalogs(count: int):
    if count < 1:
        raise HTTPException(status_code=403, detail="Count must be positive")
    generator = CatalogItemGenerator()
    return [generator.catalog_item() for _ in range(count)]


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}
