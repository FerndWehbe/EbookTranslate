from ebooklib.epub import EpubBook
from ebooklib import epub
from .epubdict import DICT


def reader_epub(path: str) -> EpubBook | None:
    try:
        return epub.read_epub(path, options={"ignore_ncx": True})
    except FileNotFoundError:
        return


def clone_metadata_book(base_book: EpubBook) -> EpubBook:
    new_book = epub.EpubBook()
    new_book.set_identifier(base_book.IDENTIFIER_ID)
    new_book.set_title(base_book.title)
    new_book.set_language(base_book.language)
    new_book.add_author("Eu")
    return new_book


def travel_epub(book: EpubBook, max_run: int = 10):
    for item in list(book.get_items())[:max_run]:
        yield DICT[item.__class__](item)


def copy_itens_books(old_book: EpubBook, new_book: EpubBook) -> EpubBook:
    num_elements = len(list(old_book.get_items()))
    elements_old_book = travel_epub(old_book, num_elements)
    index = 0
    for element in elements_old_book:
        print(f"Elemento {index + 1}")
        new_book.add_item(element)
        index += 1
    return new_book


def run():
    book = reader_epub("data/Lord_of_the_Mysteries.epub")
    new_book = clone_metadata_book(book)
    new_book = copy_itens_books(book, new_book)
    epub.write_epub("test.epub", new_book, {})


if __name__ == "__main__":
    book = reader_epub("data/Lord_of_the_Mysteries.epub")
    new_book = clone_metadata_book(book)
    new_book = copy_itens_books(book, new_book)
    epub.write_epub("test.epub", new_book, {})
