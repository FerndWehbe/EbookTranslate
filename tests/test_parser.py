from epubutils import reader_epub
from ebooklib.epub import EpubBook


def test_reader_epub_path_valido():
    epub = reader_epub("data/Lord_of_the_Mysteries.epub")
    assert isinstance(epub, EpubBook)


def test_reader_epub_path_invalido():
    epub = reader_epub("")
    assert epub is None
