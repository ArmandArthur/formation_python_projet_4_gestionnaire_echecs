from tinydb import TinyDB
from tinydb.table import Document
import json


class GeneriqueDao:

    def __init__(self, item_type):
        # Init TinyDB
        self.db = TinyDB('datas/echecs.json', sort_keys=True, indent=4)
        self.table = self.db.table(item_type.__name__.lower()+'s')
        self.item_type = item_type

        self.items = {}
        self.max_id = 0

        for item_data in self.table:
            self.create_item(**item_data)

    def create_item(self, *args, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = self.max_id + 1

        # instance
        item = self.item_type(*args, **kwargs)
        self.items[item.id] = item
        self.max_id = max(self.max_id, item.id)
        return item

    def save_item(self, id):
        item = self.find_by_id(id)
        self.table.upsert(Document(json.loads(item.json()), doc_id=id))

    def all(self):
        return list(self.items.values())

    def find_by_id(self, id):
        return self.items[id]
