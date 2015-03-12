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


node_desc = dict(id = E.e_nid,
                 name = E.e_name,
                 info = E.e_info,
                 value = E.e_val,
                 type = E.e_nt)

def _eval_dict(item, desc):
    d = {}
    for k, v in desc.items():
        d[k] = v(item) if callable(v) else v
    return d

def mk_node(nid, **kw):
    d = _eval_dict(nid, node_desc)
    d.update(_eval_dict(nid, kw))
    return d

def walk_nodes(nid, direction):
    res = []
    for nid, eid, lvl in E.nb.walk(nid, [(direction, 1, 1, [])]):
        res.append(mk_node(nid, edge=lambda *a: E.e_name(eid)))
    return res

@E.tx_abort_encaps
def _node_info(nid):
    return (mk_node(nid), walk_nodes(nid, E.UP), walk_nodes(nid, E.DOWN))

@app.task
def node_info(node_id=None):
    import time
    s = time.time()
    try:
        node, parents, children = _node_info(node_id)
        return dict(node=node, parents=parents, children=children)
    finally:
        print "took %s for pid %s" % (time.time() - s, node_id)
