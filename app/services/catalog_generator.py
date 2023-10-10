from app.services.catalog_faker import CatalogItemGenerator
from app.repository.sqlite import SQLiteRepository
from app.repository.base import BaseRepository


class CatalogGenerator:
    CHUNK_SIZE = 1000

    def __init__(self, repository: BaseRepository) -> None:
        self.gen = CatalogItemGenerator()
        self.repo = repository

    def seed_data(self, num_objects: int) -> None:
        objs = []
        all_objs = []
        for _ in range(num_objects):
            e = self.gen.get_catalog_entity()
            all_objs.append(e)
            objs.append(e)
            if len(objs) == self.CHUNK_SIZE:
                self.repo.create_catalog_entities(objs)
                objs = []
        if objs:
            self.repo.create_catalog_entities(objs)
        return all_objs

    def mutate_data(self, num_objects: int) -> None:
        for entity in self.repo.list_entities(limit=num_objects):
            e_new = self.gen.alter_catalog_entity(entity)
            self.repo.update_catalog_entity(e_new)
