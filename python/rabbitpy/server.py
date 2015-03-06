import time
import rabbitpy

s = time.time()
with rabbitpy.Connection("amqp://localhost:5672/") as conn:
    with conn.channel(True) as channel:
        exchange = rabbitpy.FanoutExchange(channel, "test-exchange", auto_delete=True)
        exchange.declare()

        #exchange2 = rabbitpy.DirectExchange(channel, "BACK-exchange", auto_delete=True)
        #exchange2.declare()

        queue = rabbitpy.Queue(channel)#, auto_delete=True)
        queue.declare()
        queue.bind(exchange)
        i = 0
        for m in queue.consume_messages(): #prefetch=1):
            i += 1
            message_id = m.properties["message_id"]
            r = rabbitpy.Message(channel, "R: %s" % message_id,
                                 properties = dict(message_id=message_id))
            r.publish("BACK-exchange", m.properties["reply_to"])

            m.ack() # ACKs are meaningless for exclusive queues, but I guess
                    # they're required in shared auto_delete queues
            if "last" in m.body:
                queue.stop_consuming()

        print "Received %s messages" % i
        print "Last message was: ", m.body
print time.time() - s
