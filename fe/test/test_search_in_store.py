import pytest
from fe.access.buyer import Buyer
from fe.access.seller import Seller
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
import uuid
import random

class TestSearchGlobal:
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_global_seller_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_global_buyer_id_{}".format(str(uuid.uuid1()))
        # self.password = self.seller_id
        b = register_new_buyer(self.buyer_id, self.buyer_id)
        self.store_id = "test_search_global_store_id_{}".format(str(uuid.uuid1()))
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.buyer = b
        self.keyword = "三毛 中国"
        yield

    def test_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        code, _ = self.buyer.search_in_store(self.keyword, self.store_id, self.buyer_id)
        assert code == 200
    
    def test_non_exist_user_id(self):
        self.buyer_id = self.buyer_id + "_x"
        code, _ = self.buyer.search_in_store(self.keyword, self.store_id, self.buyer_id)
        assert code != 200

    def test_page_2(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        page = 2
        code, page = self.buyer.search_in_store(self.keyword, self.store_id, self.buyer_id, page)
        assert code == 200
        assert page == 2

    def test_non_exist_store_id(self):
        self.store_id = self.store_id + "_x"
        code, _ = self.buyer.search_in_store(self.keyword, self.store_id, self.buyer_id)
        assert code != 200
