from be.model import store
from sqlalchemy.orm import sessionmaker,scoped_session, declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, VARCHAR, String, Time, create_engine, Integer, Text, Date
from sqlalchemy import Enum,ForeignKey,UniqueConstraint,PrimaryKeyConstraint
from sqlalchemy.orm import relationship
Base = declarative_base()

class User(Base):
    """用户"""
    __tablename__ = "user"
    id = Column(VARCHAR(64), primary_key=True, comment="主键")
    username = Column(VARCHAR(64), nullable=True, comment="用户名")
    token = Column(VARCHAR(256), nullable=True, comment="token")
    password = Column(VARCHAR(64), nullable=False, comment="密码")
    terminal = Column(VARCHAR(256), nullable=True, comment="终端")
    balance = Column(Integer, nullable=False, default=0, comment="余额")

class Store(Base):
    """商店"""
    __tablename__ = "store"
    id = Column(VARCHAR(64), primary_key=True, comment="主键")
    seller_id = Column(VARCHAR(64), 
                       ForeignKey(
                            "user.id",
                            ondelete="CASCADE",
                            onupdate="CASCADE",
                        ),
                        nullable=False,
                        comment="卖家id")
    owner = relationship("User", backref="stores")

class Order(Base):
    """订单"""
    __tablename__ = "order"
    id = Column(VARCHAR(64), primary_key=True, comment="主键")
    create_time = Column(Time, nullable=False, comment="创建时间")
    state = Column(Integer, nullable=False, comment="订单状态", default=0)
    total_price = Column(Integer, nullable=False, comment="总价格")
    store_id = Column(  VARCHAR(64),
                        ForeignKey(
                           "store.id",
                           ondelete="CASCADE",
                           onupdate="CASCADE", 
                        ),
                        nullable=False,
                        comment="商店id"
                    )
    buyer_id = Column(VARCHAR(64),
                      ForeignKey(
                          "user.id",
                          ondelete="CASCADE",
                          onupdate="CASCADE",
                      ),
                      nullable=False,
                      comment="买家id"
                      )
    buyer = relationship("User", backref="orders")
    belong_store = relationship("Store", backref="orders")

class OrderBook(Base):
    """订单和书籍关系表"""
    __tablename__ = "order_book"
    book_id = Column(VARCHAR(64),
                      ForeignKey(
                          "book.id",
                          ondelete="CASCADE",
                          onupdate="CASCADE",
                      ),
                      nullable=False
                    )
    order_id = Column(VARCHAR(64),
                      ForeignKey(
                          "order.id",
                          ondelete="CASCADE",
                          onupdate="CASCADE",
                      ),
                      nullable=False
                    )
    order = relationship("Order", backref="mid")
    book = relationship("Book", backref="mid")
    __table_args__ = (
        # 联合唯一约束
        UniqueConstraint("book_id", "order_id", name="unique_book_order"),
        # 联合主键
        PrimaryKeyConstraint(book_id, order_id),
    )
    quantity = Column(Integer, nullable=False, comment="数量")
    
class Book(Base):
    """书籍"""
    __tablename__ = "book"
    id = Column(VARCHAR(64), primary_key=True, comment="主键")
    title = Column(VARCHAR(64), nullable=False, comment="书名")
    author = Column(VARCHAR(64), nullable=False, comment="作者")
    publisher = Column(VARCHAR(64), nullable=True, comment="出版社")
    original_title = Column(VARCHAR(64), nullable=True, comment="原书名")
    translator = Column(VARCHAR(64), nullable=True, comment="译者")
    pub_year = Column(VARCHAR(64), nullable=True, comment="出版年")
    pages = Column(VARCHAR(64), nullable=True, comment="页数")
    price = Column(Integer, nullable=False, comment="价格")
    currency_unit = Column(VARCHAR(64), nullable=True, comment="货币单位")
    binding = Column(VARCHAR(64), nullable=True, comment="装帧")
    isbn = Column(VARCHAR(64), nullable=True, comment="ISBN")
    author_intro = Column(Text, nullable=True, comment="作者简介")
    book_intro = Column(Text, nullable=True, comment="书籍简介")
    content = Column(Text, nullable=True, comment="内容简介")
    picture = Column(Text, nullable=True, comment="图片")

class Tag(Base):
    """标签"""
    __tablename__ = "tag"
    book_id = Column(VARCHAR(64),
                      ForeignKey(
                          "book.id",
                          ondelete="CASCADE",
                          onupdate="CASCADE",
                      ),
                      nullable=False
                    )
    tag_name = Column(VARCHAR(64), comment="标签名")
    __table_args__ = (
        # 设置联合主键
        PrimaryKeyConstraint(book_id, tag_name),
    )
    book = relationship("Book", backref="tags")

class DBConn:
    def __init__(self):
        self.engine = store.get_db_engine()
        Base.metadata.create_all(self.engine)
        DbSession = sessionmaker(bind=self.engine)
        self.session = scoped_session(DbSession)

    def fetch_user(self, user_id) -> User | None:
        result = self.session.query(User).filter(User.id == user_id).first()
        return result

    def fetch_book(self, book_id) -> Book | None:
        result = self.session.query(Book).filter(Book.id == book_id).first()
        return result

    def fetch_store(self, store_id) -> Store | None: 
        result = self.session.query(Store).filter(Store.id == store_id).first()
        return result
    
    def fetch_order(self, order_id) -> Order | None:
        result = self.session.query(Order).filter(Order.id == order_id).first()
        return result
    

