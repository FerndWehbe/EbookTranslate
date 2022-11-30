from translator import Translate
from ebooklib import epub
from create_epub import parse_text


book = epub.read_epub("./data/Lord_of_the_Mysteries.epub")

new_book = epub.EpubBook()

new_book.metadata = book.metadata
new_book.set_language("pt-br")

trans = Translate()


def set_itens(item):
    new_book.add_item(item)


def set_html_item(item: epub.EpubHtml):
    new_page = epub.EpubHtml(title=item.title, file_name=item.file_name)
    new_content = parse_text(item.content, trans)
    if not new_content:
        new_book.add_item(item)


def get_item():
    for index, item in enumerate(book.get_items()):
        if isinstance(item, epub.EpubHtml):
            set_html_item(item)
            if index > 5:
                break
        else:
            set_itens(item)


if __name__ == "__main__":
    get_item()
    epub.write_epub("teste.epub", new_book, {})
