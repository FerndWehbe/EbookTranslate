from ebooklib import epub
from translator import translator
from bs4 import BeautifulSoup

translator = translator.Translate()


def item_analiser(item: epub.EpubItem):
    return item


def nav_analiser(nav: epub.EpubNav):
    return nav


def cover_analiser(cover: epub.EpubCover):
    return cover


def html_analiser(html: epub.EpubHtml):
    soup = BeautifulSoup(html.content, "html.parser")
    p_tags = soup.find_all("p")
    for p in p_tags:
        en_text = p.string
        if en_text:
            tokens = translator.tokenizer(en_text)
            translated_text = " ".join(translator.translator(tokens))
            p.string = translated_text
    aside_tags = soup.find_all("aside")
    for aside in aside_tags:
        en_text = aside.string
        if en_text:
            tokens = translator.tokenizer(en_text)
            translated_text = " ".join(translator.translator(tokens))
            aside.string = translated_text
    html.content = soup.encode()
    return html


DICT = {
    epub.EpubItem: item_analiser,
    epub.EpubNav: nav_analiser,
    epub.EpubCover: cover_analiser,
    epub.EpubHtml: html_analiser,
}
