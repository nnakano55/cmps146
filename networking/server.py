#import 
import socket 
import threading

#setup server 
print("run_setup")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
serversocket.bind((host, port))
serversocket.listen(5)

#server thread 
class server_thread (threading.Thread):
    def __init__(this, threadID, name, counter):
        threading.Thread.__init__(this)
        this.threadID = threadID
        this.name = name
        this.counter = counter
    def run(this):
        while True:
            #try connection with client
            try:
                clientsocket, addr = serversocket.accept()
                print("got a connection from %s" % str(addr))
                msg = 'Thank you for connecting' + "\r\n"
                clientsocket.send(msg.encode('ascii'))
                clientsocket.close()
            except:
                print("Error: socket.accept failed")
                break

#input thread to terminate connection 
class input_thread (threading.Thread):
    def __init__(this, threadID, name, counter):
        threading.Thread.__init__(this)
        this.threadID = threadID
        this.name = name
        this.counter = counter
    def run(this):
        input()
        serversocket.close()

#Create new threads
thread1 = server_thread(1, "Thread-1", 1)
thread2 = input_thread(2, "Thread-2", 2)

#Start new Threads
thread1.start()
thread2.start()
thread1.join()
thread2.join()

#End program
print ("Exiting Main Thread")

