from celery import Celery

app = Celery("tasks.tasks", backend="redis://redis", broker="amqp://guest@rabbitmq")

@app.task
def add(x, y):
    pass

@app.task
def sub(x, y):
    pass

@app.task
def e_name(nid):
    pass

@app.task
def modify():
    pass

@app.task
def list_node(node_id):
    pass
