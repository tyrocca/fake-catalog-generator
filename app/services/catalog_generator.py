from app.services.catalog_faker import CatalogItemGenerator
from app.repository.sqlite import SQLiteRepository
from app.repository.base import BaseRepository



class CatalogGenerator:



    def __init__(self, repository: BaseRepository) -> None:
        self.gen = CatalogItemGenerator()
        self.repo = repository

    def seed_data(self, num_objects: int) -> None:
        pass





