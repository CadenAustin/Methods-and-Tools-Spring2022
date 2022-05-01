import os, sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import pandas as pd

DB_FILE_NAME = "/database.db"
PARENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(PARENT_DIRECTORY)
from Models import *


engine = create_engine('sqlite://' + DB_FILE_NAME)

_SESSION = sessionmaker(bind=engine)

def createDatabase():
    dropTables()
    session = getSession()
    insp = inspect(engine)
    print(insp.get_table_names())

    bookInstance = Book(author="John Doe", publisher="Wholehouse", isbn="10928901")    
    session.add(bookInstance)
    session.commit()

    book = session.query(Book).filter_by(author="John Doe").first()
    itemInstance = InventoryItem(quantity=7, title="Generic Title", description="Generic Description", genre="Generic Genre", price=20.70, item_type="B", book_reference=book.id)
    session.add(itemInstance)
    session.commit()

    print(session.query(Book).all())

def getSession():
    Base.metadata.create_all(bind=engine)
    return _SESSION()

def dropTables():
    Base.metadata.drop_all(bind=engine)

def printTables():
    books = pd.read_sql_table(table_name="Book", con=engine)
    items = pd.read_sql_table(table_name="InventoryItem", con=engine)
    carts = pd.read_sql_table(table_name="ShoppingCart", con=engine)
    customers = pd.read_sql_table(table_name="Customer", con=engine)

    print(books)
    print(items)
    print(carts)
    print(customers)

if __name__ == "__main__":
    createDatabase()
    printTables()