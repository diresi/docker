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

def test():
    print group(add.s(i, i) for i in xrange(10))().get()
    print e_name.delay(7).wait()

if __name__ == "__main__":
    app.worker_main()
