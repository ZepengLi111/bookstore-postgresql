# import sqlite3 as sqlite

from be.model import error
from be.model import db_conn
import sqlalchemy
import json

class A:
    def __init__(self, **kwargs):
        print(kwargs)

class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_non_exist_user_id(user_id)
            store = self.fetch_store(store_id)
            if store is None:
                return error.error_non_exist_store_id(store_id)
            book = self.fetch_book(book_id)
            if book is not None:
                return error.error_exist_book_id(book_id)            
            
            book_dict = json.loads(book_json_str)

            # TODO store picture & content
            # TODO tags table
            new_book = db_conn.Book(id=book_id, 
                            store_id=store_id, 
                            stock=stock_level, 
                            title=book_dict.get('title', ''),
                            author=book_dict.get('author', ''),
                            publisher=book_dict.get('publisher', ''),
                            original_title=book_dict.get('original_title', ''),
                            translator=book_dict.get('translator', ''),
                            pub_year=book_dict.get('pub_year', ''),
                            pages=book_dict.get('pages', ''),
                            price=book_dict.get('price', ''),
                            binding=book_dict.get('binding', ''),
                            isbn=book_dict.get('isbn', ''),
                            author_intro=book_dict.get('author_intro', ''),
                            book_intro=book_dict.get('book_intro', ''),
                            )

            self.session.add(new_book)
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_non_exist_user_id(user_id)
            store = self.fetch_store(store_id)
            if store is None:
                return error.error_non_exist_store_id(store_id)
            book = self.fetch_book(book_id)
            if book is None:
                return error.error_non_exist_book_id(book_id)

            # TODO check stock level
            # if add_stock_level < 0:
            #     return error.error_stock_level_low(book_id)

            book.stock += add_stock_level
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_non_exist_user_id(user_id)
            temp_store = self.fetch_store(store_id)
            if temp_store is not None:
                return error.error_exist_store_id(store_id)
            self.session.add(db_conn.Store(id=store_id, seller_id=user_id))
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def send(self, user_id:str, order_id:str, store_id: str, token: str) -> (int, str):
        try:
            code, message = self.User.check_token(user_id, token)
            if code != 200:
                return code, message
            # if not self.user_id_exist(user_id):
            #     return error.error_non_exist_user_id(user_id)
            result_store = self.store.find_one({"store_id": store_id})
            if result_store is None:
                return error.error_non_exist_store_id(store_id)
            elif result_store['seller_id'] != user_id:
                return error.error_store_ownership(user_id)
            result_order = self.order.find_one({"order_id": order_id})
            if result_order is None:
                return error.error_non_exist_order_id(order_id)
            elif result_order['state'] != 1:
                return error.error_order_state(result_order['state'])
            else:
                result = self.order.update_one({"order_id": order_id, "seller_store_id": store_id}, {"$set": {"state": 2}})
            
        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"
