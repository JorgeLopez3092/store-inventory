from models.database import (Base, session, engine)
import csv

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    with open('inventory.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')