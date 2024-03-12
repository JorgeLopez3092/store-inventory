from models.database import (Base, session, engine)
from models.Product import Product
import csv
from datetime import datetime, date


def menu() -> str:
    while True:
        print('''
                \n****** Product Management ******
                \rv) View Product
                \ra) Add Product
                \rb) Backup Database''')
        choice = input('What would you like to do? ')
        if choice in ['v', 'a', 'b']:
            return choice
        else:
            input('''
                    \rPlease choose one of the options above.
                    \rA number from 1-5.
                    \rPress enter to try again.''')


def clean_price(price: str) -> int:
    try:
        product_price: float = float(price)
    except ValueError:
        input('''
        \n****** PRICE ERROR ******
        \rThe price should be a number without a currency symbol
        \rEx: 10.99
        \rPress enter to try again...
        \r**************************''')
    else:
        return int(product_price * 100)


def clean_quantity(quantity: str) -> int:
    try:
        quantity: int = int(quantity)
    except ValueError:
        input('''
            \n****** PRICE ERROR ******
            \rThe price should be a number.
            \rPress enter to try again.
            \r**************************''')
    else:
        return quantity


def display_product_by_id(product_id: str) -> str:
    product: Product = session.query(Product).filter(Product.product_id == int(product_id)).first()
    return f'''
            \nProduct Name: {product.product_name}
            \rPrice: {product.product_price}
            \rQuantity: {product.product_price}'''


def add_product():
    product_name: str = input('Enter product name: ')
    product_quantity_valid: bool = False
    while not product_quantity_valid:
        product_quantity: str = input('Enter product quantity: ')
        product_quantity: int = clean_quantity(product_quantity)
        if type(product_quantity) is int:
            product_quantity_valid = True

    product_price_valid: bool = False
    while not product_price_valid:
        product_price: str = input('Enter product price (Ex: 9.99): ')
        product_price: int = clean_price(product_price)
        if type(product_price) is int:
            product_price_valid = True

    new_product: Product = Product(product_name=product_name, product_quantity=product_quantity,
                                   product_price=product_price, date_updated=date.today())
    session.add(new_product)
    session.new()


def add_product_csv(product_csv_file_path: str) -> None:
    with open(product_csv_file_path, newline='') as csvfile:
        data: csv.reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(data)
        row: list[str]
        for row in data:
            product_in_db: bool = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if not product_in_db:
                product_name: str = row[0]
                product_price_string: str = row[1].replace('$', '').strip()
                product_price: int = int(float(product_price_string) * 100)
                product_quantity: int = int(row[2])
                date_updated = datetime.strptime(row[3], '%m/%d/%Y')
                product: Product = Product(product_name=product_name, product_quantity=product_quantity,
                                           product_price=product_price, date_updated=date_updated)
                session.add(product)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_product_csv('inventory.csv')
    choice = menu()
    match choice:
        case 'v':
            print(display_product_by_id('1'))
        case 'a':
            add_product()
        case _:
            print('test test test test nothing valid picked')
