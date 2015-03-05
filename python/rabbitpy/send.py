import sys
import time
import threading
import rabbitpy

try:
    count = int(sys.argv[1])
except IndexError:
    count = 1

all_messages = set()
init = threading.Event()
started = threading.Event()

def callback(conn, queue_name):
    with conn.channel(True) as channel:
        exchange = rabbitpy.DirectExchange(channel, "BACK-exchange", auto_delete=True)
        exchange.declare()
        queue = rabbitpy.Queue(channel, "BACKBACK", exclusive=True)
        queue.declare()
        queue.bind(exchange, "BACKBACK")
        init.set()
        started.wait()
        for m in queue.consume_messages(): #prefetch=1):
            print "MMM", m
            print len(all_messages)
            if not m:
                break
            all_messages.remove(m.properties["message_id"])
            if not all_messages:
                break
    print "leaving", all_messages

s = time.time()
with rabbitpy.Connection("amqp://localhost:5672/") as conn:
    with conn.channel(True) as channel:
        #channel.enable_publisher_confirms()
        #queue = rabbitpy.Queue(channel, exclusive=True)
        #queue.declare()
        #exchange = rabbitpy.DirectExchange(channel, "backback", auto_delete=True)
        #exchange.declare()
        #queue.bind(exchange, queue.name)
        exchange = rabbitpy.FanoutExchange(channel, 'test-exchange')
        exchange.declare(passive=True)

        callback_thread = threading.Thread(target=callback, kwargs=dict(conn=conn, queue_name=""))#queue.name))
        callback_thread.start()

        init.wait()
        started.set()
        for i in xrange(count):
            m = rabbitpy.Message(channel, "Message #%s." % i,
                                 properties = dict(reply_to="BACKBACK"),#queue.name),
                                 opinionated=True)
            all_messages.add(m.properties["message_id"])
            started.set()
            m.publish(exchange)
        print "Sent %s messages" % count

        m = rabbitpy.Message(channel, "last")
        m.publish(exchange)

callback_thread.join()
print time.time() - s
