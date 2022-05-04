from Helpers import getSession
from Models import Book, InventoryItem, Movie

def getAllBooks():
    session = getSession()
    return session.query(InventoryItem, Book).filter_by(item_type="B").join(Book, InventoryItem.book_reference == Book.id).order_by(InventoryItem.title).all()

def getAllMovies():
    session = getSession()
    return session.query(InventoryItem, Movie).filter_by(item_type="M").join(Movie, InventoryItem.movie_reference == Movie.id).order_by(InventoryItem.title).all()
