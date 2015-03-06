import time
import pika

s = time.time()
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue', auto_delete=True)

def on_request(ch, method, props, body):
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=body)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    if "last" in body:
        channel.stop_consuming()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
print time.time() - s
