import sys
import time
import threading
import uuid
import pika

try:
    count = int(sys.argv[1])
except IndexError:
    count = 1

all_messages = set()
exit = threading.Event()

def on_response(ch, method, props, body):
    all_messages.remove(props.correlation_id)
    if not all_messages:
        exit.set()

s = time.time()
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
queue = channel.queue_declare(exclusive=True).method.queue
channel.basic_consume(on_response, no_ack=True, queue=queue)

for i in xrange(count):
    corr_id = str(uuid.uuid4())
    all_messages.add(corr_id)
    message = "#%s" % i
    if i == count - 1:
        message = message + " last"
    channel.basic_publish(exchange='',
                          routing_key='rpc_queue',
                          properties=pika.BasicProperties(
                              reply_to = queue,
                              correlation_id = corr_id,
                          ),
                          body=message)

print "all send", time.time() - s
while not exit.is_set():
    connection.process_data_events()
print "done", time.time() - s
