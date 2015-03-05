import sys
import time
import rabbitpy

try:
    count = int(sys.argv[1])
except IndexError:
    count = 10

s = time.time()
with rabbitpy.Connection("amqp://localhost:5672/") as conn:
    with conn.channel() as channel:
        #channel.enable_publisher_confirms()
        exchange = rabbitpy.FanoutExchange(channel, 'test-exchange')
        exchange.declare()

        for i in xrange(count):
            m = rabbitpy.Message(channel, "Message #%s." % i)
            m.publish(exchange, "test-key")
        print "Sent %s messages" % count

        m = rabbitpy.Message(channel, "Message #%s ist the last one." % i)
        m.publish(exchange, "test-key")

print time.time() - s
