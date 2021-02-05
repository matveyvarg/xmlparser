import sqlite3

from typing import Iterable
from xmlparser.settings import DB_HOST, PAGE_SIZE


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=Singleton):
    """
    Databse Class
    """

    def __init__(self):
        """
        Get settings from settings.py
        """
        self.conn = sqlite3.connect(DB_HOST)
        self.cursor = self.conn.cursor()
        self.fields = [
            ('filename', 'TEXT'),
            ('InstanceMetadataId', 'TEXT'),
            ('StartOfAvailability', 'TEXT'),
            ('EndOfAvailability', 'TEXT'),
            ('Title', 'TEXT'),
            ('EpisodeTitle', 'TEXT'),
        ]
        # Create table for keeping info
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS info
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {}
            );
            '''.format(",".join([" ".join(fields) for fields in self.fields]))
        )

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS oth_id
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            value TEXT,
            info_id INTEGER,
            FOREIGN KEY(info_id) REFERENCES info(id)
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS geners
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            href TEXT,
            defenition TEXT,
            info_id INTEGER,
            FOREIGN KEY(info_id) REFERENCES info(id)
        );
        ''')

    def save(self, info: dict):
        """
        Save to db
        """
        query = {}

        for field, field_type in self.fields:
            value = info.pop(field, None)
            if value and not isinstance(value, str):
                if len(value) == 1:
                    value = str(value[0])
                else:
                    value = str(value)
            query[field] = value
        keys = ",".join(query.keys())
        values = ",".join(f":{key}" for key in query.keys())
        self.cursor.execute("INSERT INTO info ({}) VALUES ({});".format(keys, values), query)

        other_ids = info.get('OtherIdentifier')
        last_id = self.cursor.lastrowid
    
        if other_ids:
            keys = ['type', 'value', 'info_id']
            for entry in other_ids:
                for key in keys:
                    value = entry.setdefault(key)
                    if value and not isinstance(value, str):
                        if len(value) == 1:
                            value = str(value[0])
                        else:
                            value = str(value)
                    entry[key] = value


            value_keys = ",".join([f":{key}" for key in keys])

            self.cursor.executemany(
                f'INSERT INTO oth_id ({",".join(keys)}) VALUES ({value_keys});',
                [dict(**entry, info=lastrowid) for entry in other_ids]
            )

        genres = info.get('Geners')
        if genres:
            keys = ['type, href, defenition, info_id']
            for entry in genres:
                for key in keys:
                    value = entry.setdefault(key)
                    if value and not isinstance(value, str):
                        if len(value) == 1:
                            value = str(value[0])
                        else:
                            value = str(value)
                    entry[key] = value

            value_keys = ",".join([f":{key}" for key in keys])

            self.cursor.executemany(
                f'INSERT INTO geners ({",".join(keys)}) VALUES ({value_keys});',
                [dict(**entry, info=lastrowid) for entry in genres]
            )

        self.conn.commit()

    def fetch(self, offset: int = 0, sort_by='id'):
        """
        Fetch data from db
        """
        query = "SELECT * FROM info LEFT JOIN oth_id ON oth_id.info_id = info.id ORDER BY :sort_by ASC LIMIT :page_size OFFSET :offset ;"
        print(query, {"page_size": PAGE_SIZE, "sort_by": sort_by, 'offset': offset})
        self.cursor.execute(
            query,
            {"page_size": PAGE_SIZE, "sort_by": sort_by, 'offset': offset}
        )

        return self.cursor.fetchall()

