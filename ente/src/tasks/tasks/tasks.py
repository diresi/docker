from celery import Celery
import ente_common as E

# monkeypatch threadpool threads
import threadpool
from __main__ import bootstrap_thread

try:
    threadpool._WorkerThread
except AttributeError:
    threadpool._WorkerThread = threadpool.WorkerThread

class WorkerThread(threadpool._WorkerThread):
    def run(self):
        return bootstrap_thread(lambda: threadpool._WorkerThread.run(self))
threadpool.WorkerThread = WorkerThread

class Config(object):
    CELERYD_POOL = "threads"
    CELERYD_ACCEPT_CONTENT = ["pickle", "json", "msgpack", "yaml"]

app = Celery("tasks.tasks", backend="redis://redis", broker="amqp://guest@rabbitmq//")
app.config_from_object(Config)

@app.task
def add(x, y):
    return x + y

@app.task
def sub(x, y):
    return x - y

@app.task
def e_name(nid):
    return _e_name(nid)

@E.tx_abort_encaps
def _e_name(nid):
    return E.e_name(nid)
