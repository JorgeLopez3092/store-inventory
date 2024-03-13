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
            \n****** QUANTITY ERROR ******
            \rThe quantity should be a number.
            \rPress enter to try again.
            \r**************************''')
    else:
        return quantity


def display_product_by_id(product_id: int) -> str:
    product: Product = session.query(Product).filter(Product.product_id == product_id).first()
    return f'''
            \nProduct ID: {product.product_id}
            \rProduct Name: {product.product_name}
            \rPrice: ${product.product_price / 100}
            \rQuantity: {product.product_quantity}
            \rLast Updated: {product.date_updated}
            \nPress enter to continue....'''


def view_product() -> None:
    product_options: list = []
    for product in session.query(Product):
        product_options.append(product)
    print(type(product_options[0]))
    product_id_valid: bool = False
    while not product_id_valid:
        try:
            print('\n****** OPTIONS ******')
            for product in product_options:
                print(f'{product.product_id}) {product.product_name}')
            id_choice: int = int(input('Which product number would you like to view? '))
            if id_choice not in [product.product_id for product in product_options]:
                raise ValueError()
        except ValueError:
            input(f'''\n****** ID ERROR ******
                      \rThe id should be a listed number.
                      \rPress enter to try again.''')
        else:
            product_id_valid = True
    input(display_product_by_id(id_choice))


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

    product_in_db: bool = session.query(Product).filter(Product.product_name == product_name).one_or_none()
    if product_in_db:
        existing_product = session.query(Product).filter(Product.product_name == product_name).first()
        existing_product.product_quantity = product_quantity
        existing_product.product_price = product_price
        existing_product.date_updated = date.today()
    else:
        new_product: Product = Product(product_name=product_name, product_quantity=product_quantity,
                                       product_price=product_price, date_updated=date.today())
        session.add(new_product)
    confirm: None = None
    collection = session.dirty if product_in_db else session.new
    for product in collection:
        confirm: str = input(f'''\nProduct Name: {product.product_name}
                            \rProduct Price: ${product.product_price / 100}
                            \rProduct Quantity: {product.product_quantity}
                            \nEnter Y to confirm entry: ''')
    if confirm.upper() == 'Y':
        session.commit()
        return input('\nInventory updated!\nPress enter to continue...')
    else:
        session.rollback()
        return input('\nProduct aborted.\nPress enter to continue...')


def add_product_csv(product_csv_file_path: str) -> None:
    with open(product_csv_file_path, newline='') as csvfile:
        data: csv.reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(data)
        row: list[str]
        for row in data:
            product_name: str = row[0]
            product_price_string: str = row[1].replace('$', '').strip()
            product_price: int = int(float(product_price_string) * 100)
            product_quantity: int = int(row[2])
            date_updated: datetime = datetime.strptime(row[3], '%m/%d/%Y')
            date_obj: date = date_updated.date()
            product_in_db: bool = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db:
                existing_product = session.query(Product).filter(Product.product_name == row[0]).first()
                if date_obj > existing_product.date_updated:
                    existing_product.product_price = product_price
                    existing_product.product_quantity = product_quantity
                    existing_product.date_updated = date_obj
            else:
                product: Product = Product(product_name=product_name, product_quantity=product_quantity,
                                           product_price=product_price, date_updated=date_obj)
                session.add(product)
        session.commit()


def backup_database_to_csv():
    path = 'backup.csv'
    with open(path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['product_name', 'product_price', 'product_quantity', 'date_updated'])
        for product in session.query(Product):
            price: str = f'${product.product_price / 100}'
            date_string: str = f'{product.date_updated}'
            print(date_string, type(date_string))
            updated_date: str = datetime.strptime(date_string, '%Y-%m-%d').strftime('%m/%d/%Y')
            csvwriter.writerow([product.product_name, price, product.product_quantity, updated_date])


def app():
    app_running: bool = True
    while app_running:
        choice: str = menu()
        match choice:
            case 'v':
                view_product()
            case 'a':
                add_product()
            case 'b':
                bac6kup_database_to_csv()
            case _:
                print('test test test test nothing valid picked')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_product_csv('inventory.csv')
    app()
