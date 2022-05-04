import os, sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import pandas as pd

DB_FILE_NAME = "/database.db"
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PARENT_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)

sys.path.append(PARENT_DIRECTORY)
from Models import *


engine = create_engine('sqlite://' + DB_FILE_NAME)

_SESSION = sessionmaker(bind=engine)

def createBook(bookInfo):
    session = getSession()
    bookInstance = Book(author=bookInfo["author"], publisher=bookInfo["publisher"], isbn=bookInfo["isbn"])    
    session.add(bookInstance)
    session.commit()

    book = session.query(Book).filter_by(isbn=bookInfo["isbn"]).first()
    itemInstance = InventoryItem(inv_quantity=bookInfo["quantity"], title=bookInfo["title"], description=bookInfo["description"], genre=bookInfo["genre"], price=bookInfo["price"], item_type="B", book_reference=book.id)
    session.add(itemInstance)
    session.commit()

def createMovie(movieInfo):
    session = getSession()
    movieInstance = Movie(director=movieInfo["director"], leading_actor=movieInfo["leading_actor"])    
    session.add(movieInstance)
    session.commit()

    session.refresh(movieInstance)

    itemInstance = InventoryItem(inv_quantity=movieInfo["quantity"], title=movieInfo["title"], description=movieInfo["description"], genre=movieInfo["genre"], price=movieInfo["price"], item_type="M", movie_reference=movieInstance.id)
    session.add(itemInstance)
    session.commit()

def createDatabase():
    dropTables()
    session = getSession()
    insp = inspect(engine)
    print(insp.get_table_names())

    books_df = pd.read_csv(CURRENT_DIRECTORY + "/Initial/Books.csv")
    books_df_dict = books_df.to_dict(orient='records')
    [createBook(book) for book in books_df_dict]

    movies_df = pd.read_csv(CURRENT_DIRECTORY + "/Initial/Movies.csv")
    movies_df_dict = movies_df.to_dict(orient='records')
    [createMovie(movie) for movie in movies_df_dict]

    print(session.query(Book).all())

def getSession():
    Base.metadata.create_all(bind=engine)
    return _SESSION()

def _objectToDict(object):
    return {col.key: getattr(object, col.key) for col in inspect(object).mapper.column_attrs}

def flattenEntries(entryTouples):
    if (entryTouples and len(entryTouples)>0):
        if (len(entryTouples[0]) == 3):
            return [{**_objectToDict(a), **_objectToDict(b), **_objectToDict(c)} for a, b, c in entryTouples]
        elif (len(entryTouples[0]) == 2):
            return [{**_objectToDict(a), **_objectToDict(b)} for a, b in entryTouples]

def dropTables():
    Base.metadata.drop_all(bind=engine)

def printTables(tables = ["Book", "Movie", "InventoryItem", "ShoppingCart", "CartItem", "Order", "OrderItem", "Customer", "PaymentInfo", "Address"]):
    [print (f"{table} \n{pd.read_sql_table(table_name=table, con=engine)}") for table in tables]


if __name__ == "__main__":
    createDatabase()
    printTables()
