from celery import Celery
from .epub_new_dict import DICT_EPUB_ITEM
import pickle

app = Celery(
    "tasks",
    broker="redis://localhost:6379/3",
    backend="db+postgresql://postgres:postgres@localhost/celery_data"
    # backend="db+sqlite:///task_process/celery.sqlite",
)
app.conf.update(
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["application/json", "application/x-python-serialize"],
    ignore_result=False,
)


@app.task
def sum(x, y):
    return x + y


@app.task(name="Epub Task")
def parse_epub(epub_item, index):
    item = pickle.loads(epub_item)
    return DICT_EPUB_ITEM[item.__class__](item, index)
