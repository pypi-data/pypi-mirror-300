import uuid
from unittest import TestCase

from m_pyutil.mmongo import MongoCli
from m_pyutil.msqlite import create, save


class Test(TestCase):

    def test_import_sqlite(self):
        mongo_cli = MongoCli(host='192.168.233.129')
        f = 'input.db'
        table = 't_demo'
        collection = 'coll_demo'
        create(sql=f'create table if not exists {table} (id integer primary key, name text)',
               f=f)
        save(sql=f'insert into {table} (name) values (?)',
             params=[str(uuid.uuid4())],
             f=f)
        mongo_cli.import_sqlite(f=f,
                                table=table,
                                collection=collection)
