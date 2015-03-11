import os

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
    CELERYD_POOL = "prefork"
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

@app.task
def modify():
    pid = os.getpid()
    nid = E.tx_encaps(E.e_create_node)("NVAL", E.nb.root(), "H", name=str(pid))
    return (pid, nid)

@E.tx_abort_encaps
def _list_children(nid=None):
    if nid is None:
        nid = E.nb.root()
    return nid, E.e_walk(nid, (E.DOWN, 1))

@app.task
def list_children(node_id=None):
    import time
    s = time.time()
    try:
        return _list_children(node_id)
    finally:
        print "took %s for pid %s" % (time.time() - s, node_id)
