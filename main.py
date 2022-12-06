from epubutils import *
from task_process import tasks
from celery import group
import json
import time
import datetime


import pickle


def sync(book):
    lista_ids = []
    for index, item in enumerate(list(book.get_items())[:30]):
        new_item = pickle.dumps(item)
        result = tasks.parse_epub.delay(new_item, index)
        lista_ids.append(result.id)
        print(f"Item: {index} enviado para processamento.")

    with open("task_process/lista_ids_sync.json", "w") as f:
        json.dump(lista_ids, f, indent=4)


def create_chunks(iter, len_iter, chunk_size):
    return [
        list(book.get_items())[pos : pos + chunk_size]
        for pos in range(0, len_iter, chunk_size)
    ]


def assync(book):
    chunks_size = 10
    len_itens = len(list(book.get_items()))
    chunks = create_chunks(book, len_itens, chunks_size)
    lista_results = []
    for index_chunk, chunk in enumerate(chunks):
        print(
            f"Start group {index_chunk + 1} - ({datetime.datetime.now().strftime('%H:%M:%S')})"
        )
        group_task = group(
            tasks.parse_epub.s(
                pickle.dumps(item), (index_item + (index_chunk * chunks_size))
            )
            for index_item, item in enumerate(chunk)
        ).apply_async()
        lista_results += [result.id for result in group_task]
        with open(
            f"./task_process/id_tasks/tasks_registradas_{index_chunk}.json",
            "w",
        ) as f:
            json.dump(lista_results, f, indent=4)

        print(f"\tNumero de tarefas a serem executadas {len(group_task)}")

        group_task_waiting = True
        while group_task_waiting:
            time.sleep(1)
            group_task_waiting = group_task.waiting()
            print(
                f"\r\tTarefas concluidas {group_task.completed_count()}",
                end="",
            )
        print()


def sync_by_index(book, index):
    item = list(book.get_items())[index]
    tasks.parse_epub.delay(pickle.dumps(item), index)
    print(f"Item: {index} enviado para processamento.")


if __name__ == "__main__":
    book = reader_epub("data/Lord_of_the_Mysteries.epub")
    sync_by_index(book, 1222)
    sync_by_index(book, 1419)
    # assync(book)
