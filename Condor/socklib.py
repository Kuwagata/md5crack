import sys, os, socket, pickle, math

def send(sock, data = ""):
   s = sock
   # Package data
   toSend = pickle.dumps(data)
   # Calculate number of sends, rounded up to nearest integer
   packets = int(math.ceil(len(toSend) / 1024.0))
   # Send result
   s.send(str(packets))
   # Wait for acknowledgement
   s.recv(8)
   # Proceed to send
   s.sendall(toSend)

def recv(sock)
   s = sock
   temp = s.recv(8)
   packets = int(temp)
   s.send("ack")
   data = ""
   for i in xrange(packets):
      data = data + s.recv(1024)
   return pickle.loads(data)
