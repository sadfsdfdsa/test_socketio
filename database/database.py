from database.models import *

from werkzeug.utils import secure_filename
import psycopg2

class Database:
    def __init__(self, db_name):
        # self.conn = psycopg2.connect(dbname='d6g6k3varr52qg',
        #                              user='wggvgxdohnaeas',
        #                              password='43cacabc41795e6d2c2aff8db96092e7c192e36a550732c1d2825b4e2fe2bfe7',
        #                              host='ec2-54-217-204-34.eu-west-1.compute.amazonaws.com')
        # self.cursor = self.conn.cursor()

        import sqlite3
        self.__conn = sqlite3.connect(db_name, check_same_thread=False)
        self.__cursor = self.__conn.cursor()

        self.User = User(self.__cursor, self.__conn)

    def create_tables(self):
        try:
            pass
        except Exception:
            pass
