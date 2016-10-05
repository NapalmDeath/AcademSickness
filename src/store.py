import pymongo


class Store:

    def __init__(self, conf):
        self.conf = conf
        self.host = self.conf.get('host', '127.0.0.1')
        self.port = self.conf.get('port', '27017')
        self.dbname = self.conf.get('dbname', 'avito')
        self.client = None
        self.db = None

    @property
    def collection(self):
        return self.db['textfiles'] if self.db else None

    def connect(self):
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[self.dbname]

    def close(self):
        if self.client:
            self.client.close()