# import sqlite3 as sqlite
import sqlalchemy
import uuid
import json
import logging
from be.model import db_conn
from be.model import error
import datetime


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(
        self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_non_exist_user_id(user_id) + (order_id,)
            store = self.fetch_store(store_id)
            if store is None:
                return error.error_non_exist_store_id(store_id) + (order_id,)

            order_id = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            order = db_conn.Order(id=order_id, 
                                    store_id=store_id, 
                                    buyer_id=user_id, 
                                    state=0, 
                                    total_price=0,
                                    create_time=datetime.datetime.now(),
                                    )    

            self.session.add(order) 
            
            for book_id, count in id_and_count:
                book = self.fetch_book(book_id)

                if book is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                stock_level = book.stock
                price = book.price
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)
                book.stock -= count
                order_book = db_conn.OrderBook(
                    order_id=order_id, book_id=book_id, quantity=count
                )
                self.session.add(order_book)
                order.total_price += count * price
                
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)), ""
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            order = self.fetch_order(order_id)
            if order is None:
                return error.error_invalid_order_id(order_id)
            if user_id != order.buyer_id:
                return error.error_authorization_fail()
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_non_exist_user_id(user_id)
            if password != user.password:
                return error.error_authorization_fail()
            # store = self.fetch_store(store_id)
            # if store is None:
            #     return error.error_non_exist_store_id(store_id)
            if user.balance < order.total_price:
                return error.error_not_sufficient_funds(order_id)
            user.balance -= order.total_price
            order.state = 1
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_authorization_fail()
            if user.password != password:
                return error.error_authorization_fail()
            user.balance += add_value            
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def receive(self, buyer_id:str, order_id:str) -> (int, str):
        try:
            # code, message = self.User.check_token(user_id, token)
            # if code != 200:
                # return code, message
            user = self.fetch_user(buyer_id)
            if not user:
                return error.error_non_exist_user_id(buyer_id)

            order = self.fetch_order(order_id)
            if not order:
                return error.error_non_exist_order_id(order_id)

            print("order state: ", order.state)

            if order.state != 2:
                return error.error_order_state(order.state)

            order.state = 3
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"
