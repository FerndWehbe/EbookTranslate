from epubutils.parser import reader_epub, clone_metadata_book
from bookfromdb.read_data_db import read_next_id
from ebooklib.epub import EpubBook
from ebooklib import epub
import pickle


def populate_new_book_from_db(book: EpubBook, id_data_db: int):
    data = read_next_id(id_data_db)
    while data:
        result = pickle.loads(data[3])
        print(f"\rItem numero {result[0]} - id {data[0]} adicionado no livro.")
        book.add_item(result[1])
        id_data_db += 1
        data = read_next_id(id_data_db)
    return book


def create_book():
    book = reader_epub("data/Lord_of_the_Mysteries.epub")
    new_book = clone_metadata_book(book)
    new_book = populate_new_book_from_db(new_book, 237)
    epub.write_epub("EpubParcial.epub", new_book, {})
