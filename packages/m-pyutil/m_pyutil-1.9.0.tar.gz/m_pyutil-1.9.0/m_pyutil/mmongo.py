import json

from pymongo import MongoClient

from m_pyutil.msqlite import get_conn
from m_pyutil.mtmp import read


class MongoCli(MongoClient):

    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 27017,
                 username: str = 'root',
                 password: str = '123',
                 database: str = 'db_demo'):
        super().__init__(f'mongodb://{username}:{password}@{host}:{port}')
        self.database = self[database]

    def import_json_file(self,
                         f: str = 'input',
                         collection: str = 'coll_demo'):
        self.database[collection].insert_many(json.loads(read(f)))

    def import_sqlite(self,
                      f='input.db',
                      table: str = 't_demo',
                      sql: str = None,
                      params: list = None,
                      collection: str = 'coll_demo'):
        with get_conn(f) as conn:
            sqlite_cursor = conn.execute(sql or f'select * from {table}', params or [])
            rows = sqlite_cursor.fetchall()
            columns = [column[0] for column in sqlite_cursor.description]

            documents = []
            for row in rows:
                document = dict(zip(columns, row))
                documents.append(document)
                if len(documents) >= 1000:
                    self.database[collection].insert_many(documents)
                    documents.clear()

            if len(documents) > 0:
                self.database[collection].insert_many(documents)
