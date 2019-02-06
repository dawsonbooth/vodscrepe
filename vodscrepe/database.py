import sqlite3

from .vod import Vod

# TODO: Create new database (with params) if does not exist


class Database():

    def __init__(self, filename: str, table: str):
        self.filename = filename
        self.table = table

        self.conn = sqlite3.connect(self.filename)

    def contains(self, vod):
        c = self.conn.cursor()
        sql = "SELECT * FROM {table} WHERE vod_id=\"{value}\"".format(
            table=self.table, value=vod.vod_id)
        c.execute(sql)
        return c.fetchone() is not None

    def save(self, vod: Vod):
        values = [str(v) for v in vod.values()]
        sql = "INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(
            table=self.table)
        c = self.conn.cursor()
        try:
            c.execute(sql, values)
        except sqlite3.IntegrityError as e:
            print(e)
        self.conn.commit()

    def save_many(self, vods: list):
        for v in vods.copy():
            if self.contains(v):
                vods.remove(v)
        values = [[str(v) for v in dict(vod).values()] for vod in vods]
        sql = "INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(
            table=self.table)
        c = self.conn.cursor()
        try:
            c.executemany(sql, values)
        except sqlite3.IntegrityError as e:
            print(e)
        self.conn.commit()
