import socket

#setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

#try connection with server
try:
	s.connect((host, port))
	msg = s.recv(1024) 
	s.close()
	print(msg.decode('ascii'))
except:
	print("Error: connection not found")

