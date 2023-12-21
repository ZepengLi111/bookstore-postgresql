import uuid
import pytest
import random
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book


class TestCheckOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.buyer_id = "test_check_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_check_order_store_id_{}".format(str(uuid.uuid1()))
        self.seller_id = "test_check_order_seller_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.order_id = order_id

        yield

    def test_ok(self):
        code, _ = self.buyer.check_order(self.buyer_id, self.order_id)
        assert code == 200

    def test_non_exist_user_id(self):
        code, _ = self.buyer.check_order(self.buyer_id + '_x', self.order_id)
        assert code != 200

    def test_non_exist_order_id(self):
        code, _ = self.buyer.check_order(self.buyer_id, self.order_id + '_x')
        assert code != 200
