import logging
from sqlalchemy import create_engine


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

        # self.init_tables()

    # def init_tables(self):
    #     try:
    #         # conn = self.get_db_conn()
            
    #     except sqlite.Error as e:
    #         logging.error(e)
    #         conn.rollback()

    # def get_db_conn(self) -> sqlite.Connection:
    #     return sqlite.connect(self.database)


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_engine():
    global database_instance
    return database_instance.engine
