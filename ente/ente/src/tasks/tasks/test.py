import threading

def bubu(self):
    print "BUUB"
    return self.xrun()


threading.Thread.xrun = threading.Thread.run
threading.Thread.run = bubu

def func():
    print "inner"

t = threading.Thread(target=bubu)
t.start()
t.join()
