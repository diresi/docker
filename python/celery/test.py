#!/usr/bin/env python2
import tasks.tasks
import time

tt = []
for x in range(1):
    s = time.time()
    tasks.tasks.test()
    tt.append(time.time() -s)

print min(tt), max(tt), sum(tt)/len(tt)
