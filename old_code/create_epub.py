from translator import Translate
from bs4 import BeautifulSoup
from bs4.element import Tag
import re


def parse_text(content, tradutor: Translate):
    soup = BeautifulSoup(content, "html.parser")
    ps: list[Tag] = soup.find_all("p")
    if not ps:
        return None
    for p in ps:
        new_p = soup.new_tag("p")

        en_text = p.string
        if en_text:
            tokens = tradutor.tokenizer(en_text)
            # new_text = tradutor.parallel(tokens, 2)
            new_text = tradutor.translator(tokens)
            new_p.string = "".join(new_text)  # type: ignore
            p.insert_after(new_p)
        else:
            new_p.string = ""
            p.insert_after(new_p)

        p.string = ""
        p.unwrap()
    return soup
