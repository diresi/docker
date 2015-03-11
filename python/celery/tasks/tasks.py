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

@app.task
def list():
    pass

def test():
    reqs = [list.delay() for x in range(1)]
    print "a list will follow"
    for r in reqs:
        print r.get()

if __name__ == "__main__":
    app.worker_main()
