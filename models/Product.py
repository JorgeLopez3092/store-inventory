from .database import Base, Column, Integer, String, Date


class Product(Base):
    __tablename__: str = 'product'

    product_id: Column = Column(Integer, primary_key=True)
    product_name: Column = Column('product_name', String)
    product_quantity: Column = Column('product_quantity', Integer)
    product_price: Column = Column('product_price', Integer)
    date_updated: Column = Column('date_updated', Date)

    def __repr__(self) -> str:
        return f'<Product, {self.product_name}, {self.product_quantity}, {self.product_price}, {self.date_updated}>'
