import logging
from sqlalchemy import create_engine
from pymongo import MongoClient


class Store:

    def __init__(self):
        self.engine = create_engine("postgresql://postgres:187533@127.0.0.1:5433/bookstore2", 
                                    max_overflow=0,
                                    # 链接池大小
                                    pool_size=50,
                                    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
                                    pool_timeout=5,
                                    # 多久之后对链接池中的链接进行一次回收
                                    pool_recycle=1,
                                    # 不查看原生语句（未格式化）
                                    echo=False)

        self.mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
        self.mongodb = self.mongo_client['bookstore']
        try: 
            self.mongodb['book_info'].create_index([('id', 1)], unique=True)
            self.mongodb['book_info'].create_index([('searchable_words', 'text')])
            self.mongodb['book_info'].create_index([('store_id', 1)])
        except Exception as e:
            print(e)


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_engine():
    global database_instance
    return database_instance.engine, database_instance.mongodb['book_info']
