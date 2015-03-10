from celery import Celery, group

app = Celery("tasks.tasks", backend="redis://localhost", broker="amqp://guest@localhost//")

class Config(object):
    CELERYD_POOL= "threads"

app.config_from_object(Config)

@app.task
def add(x, y):
    nyi

@app.task
def sub(x, y):
    nyi

@app.task
def e_name(nid):
    nyi

@app.task
def modify():
    pass

def test():
    pid_nids = group(modify.s() for i in xrange(10))().get()
    pids = set([x[0] for x in pid_nids])
    nids = sorted([x[1] for x in pid_nids])
    names = group(e_name.s(nid) for nid in nids)().get()
    print pid_nids
    print pids
    print nids
    print names

if __name__ == "__main__":
    app.worker_main()
