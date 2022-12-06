from sqlalchemy import create_engine, text
from epubutils.parser import reader_epub, clone_metadata_book
from bookfromdb.read_data_db import read_next_id
from collections import OrderedDict
from ebooklib.epub import EpubBook
from ebooklib import epub
import pickle


def read_next_id(id):
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost/celery_data"
    )

    with engine.connect() as con:
        rs = con.execute(
            text(
                f"""SELECT id, task_id, status, result \
                    FROM celery_taskmeta \
                    WHERE date_done > '2022.12.04 00:11:45' \
                    AND ID > {id}
                    AND status = 'SUCCESS'
                    ORDER BY ID
                    LIMIT 30
                """
            )
        )
        data = rs.fetchall()
    return data


def get_data(id_data_db: int):
    result_data = {}
    data = read_next_id(id_data_db)
    while data:
        for i in data:
            decompress = pickle.loads(i[3])
            result_data[decompress[0]] = decompress[1]
        next_id = data[-1][0]
        data = read_next_id(next_id)
        print(
            f"\r Itens Processados {len(result_data)}\t Tamanho dos dados {result_data.__sizeof__() / 1024 /1024} Mbytes",
            end="",
        )
    return result_data


def create_book():
    book = reader_epub("data/Lord_of_the_Mysteries.epub")
    new_book = clone_metadata_book(book)
    dict_data = get_data(237)
    order_dict = OrderedDict(sorted(dict_data.items()))
    for key, item in order_dict.items():
        print(key)
        new_book.add_item(item)

    epub.write_epub("Result.epub", new_book, {})


if __name__ == "__main__":
    create_book()
