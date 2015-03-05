import time
import rabbitpy

s = time.time()
with rabbitpy.Connection("amqp://localhost:5672/") as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, "test-channel")
        queue.declare()
        queue.ha_declare()
        queue.bind("test-exchange", "test-key")
        i = 0
        m = None
        for m in queue.consume_messages(True, 1):
            if "last" in m.body:
                queue.stop_consuming()
            i += 1
            m.ack()
        print "Received %s messages" % i
        if m:
            print "Last message was: ", m.body
print time.time() - s
