from tinydb import TinyDB
from tinydb.table import Document
import json


class GeneriqueDao:

    def __init__(self, item_type):
        """
            Constructeur du DAO

            @param item_type: Model pydantic
        """
        # Init TinyDB
        self.db = TinyDB('echecs.json', sort_keys=True, indent=4)
        self.table = self.db.table(item_type.__name__.lower()+'s')
        self.item_type = item_type

        self.items = {}
        self.max_id = 0

        for item_data in self.table:
            self.create_item(**item_data)

    def create_item(self, *args, **kwargs):
        """
            Créé un item dans le dictionnaire

            @param args/kwargs: Prends tous les paramètres possibles
            @return: item instancié
        """
        if 'id' not in kwargs:
            kwargs['id'] = self.max_id + 1

        # instance
        item = self.item_type(*args, **kwargs)
        self.items[item.id] = item
        self.max_id = max(self.max_id, item.id)
        return item

    def save_item(self, id):
        """
            Sauvegarde le document par son doc_id
        """
        item = self.find_by_id(id)
        self.table.upsert(Document(json.loads(item.json()), doc_id=id))

    def all(self):
        """
            Liste des valeurs

            @return: Une liste des valeurs du dictionnaire
        """
        return list(self.items.values())

    def find_by_id(self, id):
        """
            Cherche un item par son ID

            @return: instance pydandic
        """
        return self.items[id]
