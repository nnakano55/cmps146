#!/usr/bin/python3

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(this, threadID, name, counter):
      threading.Thread.__init__(this)
      this.threadID = threadID
      this.name = name
      this.counter = counter
   def run(this):
      print ("Starting " + this.name)
      print_time(this.name, this.counter, 5)
      print ("Exiting " + this.name)

def print_time(threadName, delay, counter):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("Exiting Main Thread")