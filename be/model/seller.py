# import sqlite3 as sqlite

from be.model import error
from be.model import db_conn
import sqlalchemy
import json
from be.utils.segment_book_words import generate_book_kwords

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

            # TODO store picture & content ##### finished
            # TODO tags table ##### finished
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
            for tag in book_dict.get('tags', []):
                new_tag = db_conn.Tag(book_id=book_id, tag_name=tag)
                self.session.add(new_tag)
            
            self.session.add(new_book)
            self.session.commit()
            segment_words = generate_book_kwords(book_dict)
            book_info = {
                "id": book_id,
                "content": book_dict.get('content', ''),
                "picture": book_dict.get('pictures', ''),
                "searchable_words": segment_words,
                "store_id": store_id,
            }
            self.mongodb.insert_one(book_info)
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

    def send(self, seller_id:str, store_id:str, order_id: str) -> (int, str):
        try:
            # TODO check all tokens
            # code, message = self.User.check_token(user_id, token)
            # if code != 200:
                # return code, message

            user = self.fetch_user(seller_id)
            if user is None:
                return error.error_non_exist_user_id(seller_id)
            store = self.fetch_store(store_id)
            if store is None:
                return error.error_non_exist_store_id(store_id)
            if seller_id != store.seller_id:
                return error.error_store_ownership(store.seller_id)
            order = self.fetch_order(order_id)
            if order is None:
                return error.error_non_exist_order_id(order_id)
            if order.state != 1:
                return error.error_order_state(order.state)
            else:
                order.state = 2
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"
